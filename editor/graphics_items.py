from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .scene import PetriNetScene
from petnetsim.elements import Place, Transition, TransitionPriority, TransitionTimed, TransitionStochastic, Arc, Inhibitor
from typing import Union, List
from . import Editor


class ConnectSlots(QGraphicsItemGroup):
    RECT_SIZE = QSizeF(8.0, 8.0)

    def __init__(self, points: List[QPointF]):
        super().__init__()
        self.rects = [QGraphicsRectItem() for p in points]
        for r in self.rects:
            self.addToGroup(r)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            self.editor.select(self)
            print('ConnectSlots mouse pressed, event accepted')
            event.accept()


class PlaceItem(QGraphicsItemGroup):
    CIRCLE_RADIUS = 20

    def __init__(self, place: Place, editor: Editor):
        super().__init__()
        self.place = place  # source Place object
        self.editor = editor
        self.setFlag(QGraphicsItem.ItemIsMovable)

        r = PlaceItem.CIRCLE_RADIUS

        self.circle_select = QGraphicsEllipseItem(-r-2.5, -r-2.5, 2*r+6, 2*r+6)
        self.circle = QGraphicsEllipseItem(-r, -r, 2*r, 2*r)
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

    def connection_point(self, point: QPointF):
        r = PlaceItem.CIRCLE_RADIUS
        v: QVector2D = (self.pos() - point)
        v.normalize()
        v *= r
        return self.pos() + v.toPointF()


class TransitionItem(QGraphicsItemGroup):
    RECT_WIDTH = 12
    RECT_HEIGHT = 46
    normal_pen = QPen(QColor('black'), 1)
    selected_pen = QPen(QColor('red'), 3)

    def __init__(self,
                 transition: Union[Transition, TransitionTimed, TransitionPriority, TransitionStochastic],
                 editor: Editor):
        super().__init__()
        self.transition = transition  # source Place object
        self.editor = editor
        self.setFlag(QGraphicsItem.ItemIsMovable)

        w, h = TransitionItem.RECT_WIDTH, TransitionItem.RECT_HEIGHT

        self.rect = QGraphicsRectItem(-w/2, -h/2, w, h)
        self.name_text = QGraphicsSimpleTextItem('name')
        self.attribute_text = QGraphicsSimpleTextItem('attribute')
        self.is_selected = False

        self.rect.setPen(TransitionItem.selected_pen if self.is_selected else TransitionItem.normal_pen)
        self.rect.setBrush(QColor('gray'))

        self.update_texts()

        self.addToGroup(self.rect)
        self.addToGroup(self.name_text)
        self.addToGroup(self.attribute_text)

    def set_selected(self, b):
        self.is_selected = b
        self.rect.setPen(TransitionItem.selected_pen if self.is_selected else TransitionItem.normal_pen)

    def update_texts(self):
        w, h = TransitionItem.RECT_WIDTH, TransitionItem.RECT_HEIGHT
        self.name_text.setText(self.transition.name)
        self.name_text.setPos(-6*len(self.transition.name)/2, h-20)
        s = 'U(1~3.2)s'
        self.attribute_text.setText(s)
        self.attribute_text.setPos(-6*len(s)/2, h-10)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            self.editor.select(self)
            event.accept()

    def connection_point(self, point: QPointF):
        v: QVector2D = (self.pos() - point)
        if v.x() >= 0:
            if v.y() >= v.y():
                pass

        return self.pos() + v.toPointF()


class ArcItem(QGraphicsItemGroup):
    def __init__(self,
                 arc: Union[Arc, Inhibitor],
                 editor: Editor):
        super().__init__()
        self.arc = arc  # source Place object
        self.editor = editor
        self.setFlag(QGraphicsItem.ItemIsMovable)

#        self.line =
        #self.rect_select = QGraphicsRectItem(-12., -22.5, 12, 46)
        self.name_text = QGraphicsSimpleTextItem('name')
        self.attribute_text = QGraphicsSimpleTextItem('attribute')
        #self.is_selected = False
        #self.rect_select.setBrush()
        self.is_selected = True
        #self.rect_select.setVisible(self.is_selected)

        self.normal_pen = QPen(QColor('black'), 1)
        self.selected_pen = QPen(QColor('red'), 3)

        self.rect.setPen(self.selected_pen if self.is_selected else self.normal_pen)
        self.rect.setBrush(QColor('gray'))

        self.update_texts()

        self.addToGroup(self.rect)
        #self.addToGroup(self.rect_select)
        self.addToGroup(self.name_text)
        self.addToGroup(self.attribute_text)

    def set_selected(self, b):
        self.is_selected = b
        self.rect.setPen(self.selected_pen if self.is_selected else self.normal_pen)

    def update_texts(self):
        self.name_text.setText(self.transition.name)
        self.name_text.setPos(-6*len(self.transition.name)/2, -50)
        s = 'U(1~3.2)s'
        self.attribute_text.setText(s)
        self.attribute_text.setPos(-6*len(s)/2, -40)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            self.editor.select(self)
            print('item mouse pressed')
            event.accept()
