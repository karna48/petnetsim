
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from petnetsim.elements import Place, Transition, TransitionPriority, TransitionTimed, TransitionStochastic, Arc, Inhibitor
from typing import Union, DefaultDict
from itertools import chain
from collections import defaultdict
from .graphics_items import PlaceItem, TransitionItem, ArcItem, Port
import enum


class Editor(QGraphicsView):
    class Mode(enum.IntEnum):
        Normal = 0
        ArcSource = 1
        ArcTarget = 2

    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.setMouseTracking(True)

        self.mode = Editor.Mode.Normal

        self.arc_lookup = defaultdict(list)
        self.arc_mode_data = {'source_port': None, 'target_port': None}


        self.selected = None

        self.place_items = []
        self.transition_items = []
        self.arc_items = []

        place_A = Place('A', 5, capacity=3)
        self.place_A_item = PlaceItem(place_A, self)
        self.scene().addItem(self.place_A_item)
        self.place_items.append(self.place_A_item)

        place_B = Place('B', 2)
        self.place_B_item = PlaceItem(place_B, self)
        self.scene().addItem(self.place_B_item)
        self.place_B_item.setPos(0, 100)
        self.place_items.append(self.place_B_item)

        place_C = Place('C')
        self.place_C_item = PlaceItem(place_C, self)
        self.scene().addItem(self.place_C_item)
        self.place_C_item.setPos(150, 20)
        self.place_items.append(self.place_C_item)

        test_transition = Transition('T1')
        self.test_transition_item = TransitionItem(test_transition, self)
        self.test_transition_item.setPos(80, 0)
        self.scene().addItem(self.test_transition_item)
        self.place_items.append(self.test_transition_item)

        self.add_arc(self.place_A_item.ports[0], self.test_transition_item.ports[0], 3)
        self.add_arc(self.place_B_item.ports[7], self.test_transition_item.ports[2], 1)
        self.add_arc(self.test_transition_item.ports[1], self.place_C_item.ports[5], 1)

    def item_moved(self, assoc_obj):
        arc_item: ArcItem
        for arc_item in self.arc_lookup[assoc_obj]:
            arc_item.update_ports()

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
        print(self.selected, item)
        if self.selected == item:
            return
        if self.selected is not None:
            self.selected.set_selected(False)
        self.selected = item
        if item is not None:
            item.set_selected(True)

    def mousePressEvent(self, event: QMouseEvent):
        if self.mode == Editor.Mode.Normal:
            super().mousePressEvent(event)
            print('editor mousePressEvent: event.isAccepted():', event.isAccepted())

            if not event.isAccepted() and event.button() == Qt.LeftButton:
                self.select(None)

        elif self.mode == Editor.Mode.ArcSource:
            pass

    def keyPressEvent(self, key_event: QKeyEvent):
        if key_event.isAutoRepeat():
            return  # no autorepeats!

        if key_event.key() == Qt.Key_Escape:
            self.select(None)

        if key_event.key() == ord('X'):
            print(self.place_A_item.pos())

        if key_event.key() == ord('S'):
            self.place_A_item.set_selected(not self.place_A_item.is_selected)

        if key_event.key() == ord('A'):
            if self.mode == Editor.Mode.Normal:
                for item in chain(self.place_items, self.transition_items):
                    item.show_ports()

                self.mode = Editor.Mode.ArcSource


    def keyReleaseEvent(self, key_event: QKeyEvent):
        if key_event.isAutoRepeat():
            return  # no autorepeats!

        if key_event.key() == ord('A'):
            if self.mode in (Editor.Mode.ArcSource, Editor.Mode.ArcTarget):
                self.mode = Editor.Mode.Normal

            for item in chain(self.place_items, self.transition_items):
                item.hide_ports()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.mode == Editor.Mode.ArcTarget:




