
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from petnetsim.elements import Place, Transition, TransitionPriority, TransitionTimed, TransitionStochastic, Arc, Inhibitor
from typing import Union
from .graphics_items import PlaceItem, TransitionItem, ArcItem


class Editor(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene())

        self.selected = None

        self.place_items = []
        self.transition_items = []
        self.arc_items = []

        place_A = Place('PlaceA', 5, capacity=3)
        self.place_A_item = PlaceItem(place_A, self)
        self.scene().addItem(self.place_A_item)

        place_B = Place('B', 2)
        self.place_B_item = PlaceItem(place_B, self)
        self.scene().addItem(self.place_B_item)
        self.place_B_item.setPos(0, 100)

        test_transition = Transition('T1')
        self.test_transition_item = TransitionItem(test_transition, self)
        self.test_transition_item.setPos(80, 0)
        self.scene().addItem(self.test_transition_item)

        test_arc = Arc(place_A, test_transition, 3)
        self.test_arc_item = ArcItem(test_arc,
                                     self.place_A_item.ports[0],
                                     self.test_transition_item.ports[0],
                                     self)
        self.scene().addItem(self.test_arc_item)

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
        print('editor mousePressEvent')
        super().mousePressEvent(event)
        print('editor mousePressEvent: event.isAccepted():', event.isAccepted())
        if not event.isAccepted() and event.button() == Qt.LeftButton:
            self.select(None)

    def keyPressEvent(self, key_event: QKeyEvent):
        print(key_event.key())

        if key_event.key() == Qt.Key_Escape:
            self.select(None)

        if key_event.key() == ord('X'):
            print(self.place_A_item.pos())

        if key_event.key() == ord('S'):
            self.place_A_item.set_selected(not self.place_A_item.is_selected)

        if key_event.key() == ord('A'):
            print('add arc')


