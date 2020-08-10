
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .scene import PetriNetScene
from petnetsim.elements import Place, Transition, TransitionPriority, TransitionTimed, TransitionStochastic, Arc, Inhibitor
from typing import Union
from .graphics_items import PlaceItem, TransitionItem, ArcItem


class Editor(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(PetriNetScene())

        self.selected = None

        self.place_items = []
        self.transition_items = []
        self.arc_items = []

        test_place = Place('PlaceA', 5, capacity=3)
        self.test_place_item = PlaceItem(test_place, self)
        self.scene().addItem(self.test_place_item)

        test_transition = Transition('T1')
        self.test_transition_item = TransitionItem(test_transition, self)
        self.test_transition_item.setPos(80, 0)
        self.scene().addItem(self.test_transition_item)

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
            print(self.test_place_item.pos())

        if key_event.key() == ord('S'):
            self.test_place_item.set_selected(not self.test_place_item.is_selected)

        if key_event.key() == ord('A'):
            print('add arc')


