
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from petnetsim.elements import Place, Transition, TransitionPriority, TransitionTimed, TransitionStochastic, Arc, Inhibitor
from typing import Union
from itertools import chain
from collections import defaultdict
from .graphics_items import PlaceItem, TransitionItem, ArcItem, Port
import enum


class Editor(QGraphicsView):
    class Mode(enum.IntEnum):
        Normal = 0
        ArcSource = 1
        ArcTarget = 2

    ModeStrings = {Mode.Normal: 'Normal',
                   Mode.ArcSource: 'Arc source',
                   Mode.ArcTarget: 'Arc target'}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene())
        self.setMouseTracking(True)

        self._mode = Editor.Mode.Normal

        self.arc_lookup = defaultdict(list)
        self.arc_mode_tmp = None

        self.selected = None

        self.place_items = []
        self.transition_items = []
        self.arc_items = []

        self.last_mouse_scene_pos = QPointF()

    def after_init(self, main_window):
        self.main_window = main_window

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, v):
        self._mode = v
        self.main_window.mode_label.setText(Editor.ModeStrings[self._mode])

    def item_moved(self, assoc_obj):
        arc_item: ArcItem
        for arc_item in self.arc_lookup[assoc_obj]:
            arc_item.update_ports()

    def add_place(self):
        place = Place()
        place_item = PlaceItem(place, self)
        place_item.setPos(self.last_mouse_scene_pos)
        self.scene().addItem(place_item)
        self.place_items.append(place_item)
        self.select(place_item)

    def delete_place_item(self, place_item):
        to_delete = self.arc_lookup[place_item.place].copy()
        for arc_item in to_delete:
            self.delete_arc_item(arc_item)
        self.arc_lookup.pop(place_item.place)
        self.place_items.remove(place_item)
        self.scene().removeItem(place_item)

    def add_transition(self):
        transition = Transition(None)
        transition_item = TransitionItem(transition, self)
        transition_item.setPos(self.last_mouse_scene_pos)
        self.scene().addItem(transition_item)
        self.transition_items.append(transition_item)
        self.select(transition_item)

    def delete_transition_item(self, transition_item):
        to_delete = self.arc_lookup[transition_item.transition].copy()
        for arc_item in to_delete:
            self.delete_arc_item(arc_item)
        self.arc_lookup.pop(transition_item.transition)
        self.transition_items.remove(transition_item)
        self.scene().removeItem(transition_item)

    def add_arc(self, source_port: Port, target_port: Port, n_tokens=1):
        arc = Arc(source_port.assoc_obj, target_port.assoc_obj, n_tokens)
        arc_item = ArcItem(arc, source_port, target_port, self)
        self.scene().addItem(arc_item)
        self.arc_items.append(arc_item)
        self.arc_lookup[source_port.assoc_obj].append(arc_item)
        self.arc_lookup[target_port.assoc_obj].append(arc_item)

    def delete_arc_item(self, arc_item):
        self.arc_lookup[arc_item.source.assoc_obj].remove(arc_item)
        self.arc_lookup[arc_item.target.assoc_obj].remove(arc_item)
        self.scene().removeItem(arc_item)
        self.arc_items.remove(arc_item)

    def select(self, item):
        if self.mode == Editor.Mode.Normal:
            if self.selected == item:
                return
            if self.selected is not None:
                self.selected.set_selected(False)
            self.selected = item
            if item is not None:
                item.set_selected(True)

    def select_port(self, port: Port):
        if self.mode == Editor.Mode.ArcSource:
            self.arc_mode_tmp = ArcModeTemporary(port, self)
            self.mode = Editor.Mode.ArcTarget
        elif self.mode == Editor.Mode.ArcTarget:
            if self.arc_mode_tmp.connect_target(port):
                self.arc_mode_tmp = None
                self.mode = self.mode.ArcSource  # can make new arcs until A is pressed

    def mousePressEvent(self, event: QMouseEvent):
        if self.mode == Editor.Mode.Normal:
            super().mousePressEvent(event)
            print('editor mousePressEvent: event.isAccepted():', event.isAccepted())

            if not event.isAccepted() and event.button() == Qt.LeftButton:
                self.select(None)
        elif self.mode == Editor.Mode.ArcSource:
            super().mousePressEvent(event)
        elif self.mode == Editor.Mode.ArcTarget:
            super().mousePressEvent(event)

    def keyPressEvent(self, key_event: QKeyEvent):
        if key_event.isAutoRepeat():
            return  # no autorepeats!

        def cancel_arc_modes():
            for item in chain(self.place_items, self.transition_items):
                item.hide_ports()
            if self.arc_mode_tmp is not None:
                self.arc_mode_tmp.cancel()
                self.arc_mode_tmp = None

        if key_event.key() == Qt.Key_Escape:
            self.select(None)
            if self.mode in (Editor.Mode.ArcSource, Editor.Mode.ArcTarget):
                cancel_arc_modes()
                self.mode = Editor.Mode.Normal

        if key_event.key() == Qt.Key_Delete:
            if self.mode == Editor.Mode.Normal:
                if isinstance(self.selected, PlaceItem):
                    self.delete_place_item(self.selected)
                elif isinstance(self.selected, TransitionItem):
                    self.delete_transition_item(self.selected)
                elif isinstance(self.selected, ArcItem):
                    self.delete_arc_item(self.selected)

        if key_event.key() == Qt.Key_P:
            if self.mode == Editor.Mode.Normal:
                self.add_place()

        if key_event.key() == Qt.Key_T:
            if self.mode == Editor.Mode.Normal:
                self.add_transition()

        if key_event.key() == Qt.Key_A:
            if self.mode == Editor.Mode.Normal:
                for item in chain(self.place_items, self.transition_items):
                    item.show_ports()
                self.mode = Editor.Mode.ArcSource
            elif self.mode in (Editor.Mode.ArcSource, Editor.Mode.ArcTarget):
                cancel_arc_modes()
                self.mode = Editor.Mode.Normal

    def keyReleaseEvent(self, key_event: QKeyEvent):
        if key_event.isAutoRepeat():
            return  # no autorepeats!

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.last_mouse_scene_pos = self.mapToScene(event.pos())
        if self.mode == Editor.Mode.Normal:
            super().mouseMoveEvent(event)
        elif self.mode == Editor.Mode.ArcSource:
            pass
        elif self.mode == Editor.Mode.ArcTarget:
            pass


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
            # no duplicities and backward arcs!
            same_source = arc_item.source.assoc_obj == self.source_port.assoc_obj
            same_target = arc_item.target.assoc_obj == target_port.assoc_obj
            reversed_st = arc_item.source.assoc_obj == target_port.assoc_obj
            reversed_ts = arc_item.target.assoc_obj == self.source_port.assoc_obj
            if (same_source and same_target) or (reversed_st and reversed_ts):
                print('ERROR: already connected')
                return False

        self.source_port.setBrush(Port.NormalBrush)
        self.editor.add_arc(self.source_port, target_port)
        return True

    def cancel(self):
        print('ArcModeTemporary cancel')
        self.source_port.setBrush(Port.NormalBrush)
        self.source_port = None
