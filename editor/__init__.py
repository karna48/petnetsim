
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from .scene import PetriNetScene
from petnetsim.elements import Place, Transition, TransitionPriority, TransitionTimed, TransitionStochastic, Arc, Inhibitor
from typing import Union

class Editor(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(PetriNetScene())

        self.selected = None

        self.place_items = []
        self.transition_items = []
        self.arc_items = []

        test_place = petnetsim.elements.Place('PlaceA', 5, capacity=3)
        self.test_place_item = PlaceGraphicsItem(test_place, self)
        self.scene().addItem(self.test_place_item)

        #print('viewport:', )

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


class PlaceGraphicsItem(QGraphicsItemGroup):
    def __init__(self, place: Place, editor: Editor):
        super().__init__()
        self.place = place  # source Place object
        self.editor = editor
        self.setFlag(QGraphicsItem.ItemIsMovable)

        self.circle_select = QGraphicsEllipseItem(-22.5, -22.5, 46, 46)
        self.circle = QGraphicsEllipseItem(-20, -20, 40, 40)
        self.tokens_text = QGraphicsSimpleTextItem('')
        self.capacity_text = QGraphicsSimpleTextItem('')
        self.name_text = QGraphicsSimpleTextItem('')
        p = QPen()
        p.setColor(QColor(255, 0, 0))
        p.setWidthF(2)
        self.circle_select.setPen(p)
        self.is_selected = False
        self.circle_select.setVisible(self.is_selected)

        self.update_texts()

        self.addToGroup(self.circle)
        self.addToGroup(self.circle_select)
        self.addToGroup(self.tokens_text)
        self.addToGroup(self.capacity_text)
        self.addToGroup(self.name_text)

    def set_selected(self, b):
        self.is_selected = b
        self.circle_select.setVisible(b)

    def update_texts(self):
        self.name_text.setText(self.place.name)
        self.name_text.setPos(-6*len(self.place.name)/2, -40)

        s = str(self.place.init_tokens)
        self.tokens_text.setText(s)
        self.tokens_text.setPos(-6*len(s)/2, -8)
        self.tokens_text.setVisible(self.place.init_tokens > 0)

        s = 'C='+str(self.place.capacity)
        self.capacity_text.setText(s)
        self.capacity_text.setPos(-6*len(s)/2, 20)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            self.editor.select(self)
            print('item mouse pressed')
            event.accept()


class TransitionGraphicsItem(QGraphicsItemGroup):
    def __init__(self,
                 transition: Union[Transition, TransitionTimed, TransitionPriority, TransitionStochastic],
                 editor: Editor):
        super().__init__()
        self.transition = transition  # source Place object
        self.editor = editor
        self.setFlag(QGraphicsItem.ItemIsMovable)

        self.rect
        self.rect_select = QGraphicsRectItem(-22.5, -22.5, 46, 46)
        self.rect = QGraphicsEllipseItem(-20, -20, 40, 40)
        self.name_text = QGraphicsSimpleTextItem('')
        p = QPen()
        p.setColor(QColor(255, 0, 0))
        p.setWidthF(2)
        self.circle_select.setPen(p)
        self.is_selected = False
        self.circle_select.setVisible(self.is_selected)

        self.update_texts()

        self.addToGroup(self.circle)
        self.addToGroup(self.circle_select)
        self.addToGroup(self.tokens_text)
        self.addToGroup(self.capacity_text)
        self.addToGroup(self.name_text)

    def set_selected(self, b):
        self.is_selected = b
        self.circle_select.setVisible(b)

    def update_texts(self):
        self.name_text.setText(self.place.name)
        self.name_text.setPos(-6*len(self.place.name)/2, -40)

        s = str(self.place.init_tokens)
        self.tokens_text.setText(s)
        self.tokens_text.setPos(-6*len(s)/2, -8)
        self.tokens_text.setVisible(self.place.init_tokens > 0)

        s = 'C='+str(self.place.capacity)
        self.capacity_text.setText(s)
        self.capacity_text.setPos(-6*len(s)/2, 20)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            self.editor.select(self)
            print('item mouse pressed')
            event.accept()
