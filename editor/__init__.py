from collections import defaultdict
from itertools import chain
from typing import Union, List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import petnetsim.json_io as json_io
from petnetsim import PetriNet
from petnetsim.elements import Place, Transition, \
    TransitionPriority, TransitionTimed, TransitionStochastic, \
    Arc
from .graphics_items import PlaceItem, TransitionItem, ArcItem, Port
from .mode import Mode

PlaceTransitionUnion = Union[Place, Transition, TransitionPriority, TransitionTimed, TransitionStochastic]
TransitionUnion = Union[Transition, TransitionPriority, TransitionTimed, TransitionStochastic]


class Editor(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene())
        self.setMouseTracking(True)

        self.main_window = self.window()

        self.arc_lookup = defaultdict(list)
        self.arc_mode_tmp = None

        self.selected: Union[None, PlaceItem, TransitionItem, ArcItem] = None

        self.place_items: List[PlaceItem] = []
        self.transition_items: List[TransitionItem] = []
        self.arc_items: List[ArcItem] = []

        self.last_mouse_scene_pos = QPointF()

    def verified_petrinet(self, toggled=None, inform_success=True, include_item_lookups=False) -> Union[PetriNet, None]:
        try:
            pn = PetriNet([item.place for item in self.place_items],
                          [item.transition for item in self.transition_items],
                          [item.arc for item in self.arc_items])

            if include_item_lookups:
                pn.place_item_lookup = {item.place: item for item in self.place_items}
                pn.transition_item_lookup = {item.transition: item for item in self.transition_items}
                pn.arc_item_lookup = {item.arc: item for item in self.arc_items}


            msg = f'{len(pn.places)} places, {len(pn.transitions)} transitions, {len(pn.arcs)} arcs'
            if inform_success:
                QMessageBox.information(None, 'verification success', msg)
            return pn
        except Exception as e:
            msg = type(e).__name__ + ': ' + str(e)
            print(msg)
            QMessageBox.warning(None, 'verification failed', msg)
            return None

    def update_all_texts(self):
        for item in chain(self.place_items, self.transition_items, self.arc_items):
            item.update_texts()

    @property
    def mode(self):
        return self.main_window.mode

    @mode.setter
    def mode(self, new_mode):
        self.main_window.mode = new_mode

    def item_moved(self, assoc_obj: PlaceTransitionUnion):
        arc_item: ArcItem
        for arc_item in self.arc_lookup[assoc_obj]:
            arc_item.update_ports()

    def add_place(self, place=None):
        if place is None:
            place = Place()
        place_item = PlaceItem(place, self)
        place_item.setPos(self.last_mouse_scene_pos)
        self.scene().addItem(place_item)
        self.place_items.append(place_item)
        return place_item

    def delete_place_item(self, place_item):
        to_delete = self.arc_lookup[place_item.place].copy()
        for arc_item in to_delete:
            self.delete_arc_item(arc_item)
        self.arc_lookup.pop(place_item.place)
        self.place_items.remove(place_item)
        self.scene().removeItem(place_item)

    def add_transition(self, transition=None):
        if transition is None:
            transition = Transition(None)
        transition_item = TransitionItem(transition, self)
        transition_item.setPos(self.last_mouse_scene_pos)
        self.scene().addItem(transition_item)
        self.transition_items.append(transition_item)
        return transition_item

    def delete_transition_item(self, transition_item):
        to_delete = self.arc_lookup[transition_item.transition].copy()
        for arc_item in to_delete:
            self.delete_arc_item(arc_item)
        self.arc_lookup.pop(transition_item.transition)
        self.transition_items.remove(transition_item)
        self.scene().removeItem(transition_item)

    def add_arc(self, source_port: Port, target_port: Port, n_tokens=1, arc=None):
        if arc is None:
            arc = Arc(source_port.assoc_obj, target_port.assoc_obj, n_tokens)
        arc_item = ArcItem(arc, source_port, target_port, self)
        self.scene().addItem(arc_item)
        self.arc_items.append(arc_item)
        self.arc_lookup[source_port.assoc_obj].append(arc_item)
        self.arc_lookup[target_port.assoc_obj].append(arc_item)
        return arc_item

    def delete_arc_item(self, arc_item: ArcItem):
        self.arc_lookup[arc_item.source.assoc_obj].remove(arc_item)
        self.arc_lookup[arc_item.target.assoc_obj].remove(arc_item)
        self.scene().removeItem(arc_item)
        self.arc_items.remove(arc_item)

    def substitute_object(self, old_obj, new_obj):
        for arc_item in self.arc_items:
            added = False

            if arc_item.arc.source == old_obj:
                added = True
                arc_item.arc.source = new_obj
            if arc_item.arc.target == old_obj:
                added = True
                arc_item.arc.target = new_obj

            if added:
                self.arc_lookup[new_obj].append(arc_item)
        self.arc_lookup.pop(old_obj)

    def select(self, item):
        if self.mode in (Mode.Normal, Mode.Simulation):
            if self.selected == item:
                return
            if self.selected is not None:
                self.selected.set_selected(False)
            self.selected = item
            self.main_window.item_properties.item_selected(item)
            if item is not None:
                item.set_selected(True)

    def select_port(self, port: Port):
        if self.mode == Mode.ArcSource:
            self.arc_mode_tmp = ArcModeTemporary(port, self)
            self.mode = Mode.ArcTarget
        elif self.mode == Mode.ArcTarget:
            if self.arc_mode_tmp.connect_target(port):
                self.arc_mode_tmp = None
                self.mode = self.mode.ArcSource  # can make new arcs until A is pressed

    def mousePressEvent(self, event: QMouseEvent):
        if self.mode in (Mode.Normal, Mode.Simulation):
            super().mousePressEvent(event)

            if not event.isAccepted() and event.button() == Qt.LeftButton:
                self.select(None)
        elif self.mode == Mode.ArcSource:
            super().mousePressEvent(event)
        elif self.mode == Mode.ArcTarget:
            super().mousePressEvent(event)

    def cancel_arc_modes(self):
        for item in chain(self.place_items, self.transition_items):
            item.hide_ports()
        if self.arc_mode_tmp is not None:
            self.arc_mode_tmp.cancel()
            self.arc_mode_tmp = None

    def keyPressEvent(self, key_event: QKeyEvent):
        if key_event.isAutoRepeat():
            return  # no autorepeats!

        if key_event.key() == Qt.Key_Escape:
            self.select(None)
            if self.mode in (Mode.ArcSource, Mode.ArcTarget):
                self.mode = Mode.Normal
        elif key_event.key() == Qt.Key_Delete:
            if self.mode == Mode.Normal:
                if isinstance(self.selected, PlaceItem):
                    self.delete_place_item(self.selected)
                elif isinstance(self.selected, TransitionItem):
                    self.delete_transition_item(self.selected)
                elif isinstance(self.selected, ArcItem):
                    self.delete_arc_item(self.selected)
        elif key_event.key() == Qt.Key_P:
            if self.mode == Mode.Normal:
                place_item = self.add_place()
                self.select(place_item)
        elif key_event.key() == Qt.Key_T:
            if self.mode == Mode.Normal:
                transition_item = self.add_transition()
                self.select(transition_item)
        elif key_event.key() == Qt.Key_A:
            if self.mode == Mode.Normal:
                for item in chain(self.place_items, self.transition_items):
                    item.show_ports()
                self.mode = Mode.ArcSource
            elif self.mode in (Mode.ArcSource, Mode.ArcTarget):
                self.mode = Mode.Normal
        elif key_event.key() == Qt.Key_Plus:
            self.scale(1.15, 1.15)
        elif key_event.key() == Qt.Key_Minus:
            self.scale(0.869565217, 0.869565217)
        elif key_event.key() == Qt.Key_0:
            self.resetTransform()

    def keyReleaseEvent(self, key_event: QKeyEvent):
        if key_event.isAutoRepeat():
            return  # no autorepeats!

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.last_mouse_scene_pos = self.mapToScene(event.pos())
        if self.mode == Mode.Normal:
            super().mouseMoveEvent(event)
        elif self.mode == Mode.ArcSource:
            pass
        elif self.mode == Mode.ArcTarget:
            pass

    def save_petrinet(self, file):
        graphics = {}
        places = []
        for pi in self.place_items:
            places.append(pi.place)
            dsc = [pi.pos().x(), pi.pos().y()]
            graphics[pi.place] = dsc
        transitions = []
        for ti in self.transition_items:
            transitions.append(ti.transition)
            dsc = [ti.pos().x(), ti.pos().y()]
            graphics[ti.transition] = dsc
        arcs = []
        ai: ArcItem
        for ai in self.arc_items:
            arcs.append(ai.arc)
            dsc = [ai.source.number, ai.target.number]
            graphics[ai.arc] = dsc

        json_io.dump(file, places, transitions, arcs, graphics)

    def clear(self):
        to_delete = self.place_items.copy()
        for p in to_delete:
            self.delete_place_item(p)
        to_delete = self.transition_items.copy()
        for t in to_delete:
            self.delete_transition_item(t)
        self.arc_lookup.clear()

    def load_petrinet(self, file):
        self.clear()
        places, transitions, arcs, graphics = json_io.load(file)
        obj_item_lookup = {}
        names_lookup = {}
        obj_i = 0
        for p in places:
            names_lookup[p.name] = p
            item = self.add_place(p)
            obj_item_lookup[p] = item
            if graphics is not None:
                g = graphics[p]
            else:
                g = list(n*60 for n in divmod(obj_i, 10))
                g.reverse()
            item.setPos(g[0], g[1])
            obj_i += 1

        for t in transitions:
            names_lookup[t.name] = t
            item = self.add_transition(t)
            obj_item_lookup[t] = item
            if graphics is not None:
                g = graphics[t]
            else:
                g = list(n * 60 for n in divmod(obj_i, 10))
                g.reverse()
            item.setPos(g[0], g[1])
            obj_i += 1

        for a in arcs:
            a.connect(names_lookup)
            source_item = obj_item_lookup[a.source]
            target_item = obj_item_lookup[a.target]
            if graphics is not None:
                g = graphics[a]
            else:
                g = (0, 0)  # default ports
            source_port = source_item.ports[g[0]]
            target_port = target_item.ports[g[1]]

            item = self.add_arc(source_port, target_port, arc=a)


class ArcModeTemporary:
    def __init__(self, source_port: Port, editor: Editor):
        self.source_port = source_port
        self.editor = editor
        self.source_port.setBrush(Port.SelectedBrush)

    def connect_target(self, target_port: Port):
        target_is_place = isinstance(target_port.assoc_obj, Place)
        target_is_transition = isinstance(target_port.assoc_obj, Transition)
        source_is_place = isinstance(self.source_port.assoc_obj, Place)
        source_is_transition = isinstance(self.source_port.assoc_obj, Transition)
        if (target_is_place and source_is_place) or (target_is_transition and source_is_transition):
            print('ERROR: cannot connect two places or two transitions')
            return False

        for arc_item in self.editor.arc_items:
            # no duplicities
            same_source = arc_item.source.assoc_obj == self.source_port.assoc_obj
            same_target = arc_item.target.assoc_obj == target_port.assoc_obj
            if (same_source and same_target):
                print('ERROR: already connected')
                return False

        self.source_port.setBrush(Port.NormalBrush)
        self.editor.add_arc(self.source_port, target_port)
        return True

    def cancel(self):
        self.source_port.setBrush(Port.NormalBrush)
        self.source_port = None
