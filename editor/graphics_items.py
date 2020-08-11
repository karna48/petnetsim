from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from petnetsim.elements import Place, Transition, TransitionPriority, TransitionTimed, TransitionStochastic, Arc, Inhibitor
from typing import Union, List
from math import sin, cos, atan2, pi
import numpy as np


class Port(QGraphicsRectItem):
    RECT_SIZE = QSizeF(8.0, 8.0)
    BRUSH = QBrush(QColor('white'))

    def __init__(self, center: QPointF, assoc_obj, assoc_item, editor):
        # TODO: set position to center, make the rect centered at 0
        v = QPointF(Port.RECT_SIZE.width()/2, Port.RECT_SIZE.height()/2)
        r = QRectF(center-v, center+v)
        super().__init__(r)
        self.assoc_obj = assoc_obj
        self.assoc_item = assoc_item
        self.setBrush(Port.BRUSH)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            print('Port mouse pressed, event accepted')
            event.accept()


class PlaceItem(QGraphicsItemGroup):
    CIRCLE_RADIUS = 20

    def __init__(self, place: Place, editor):
        super().__init__()
        self.place = place  # source Place object
        self.editor = editor
        self.setFlag(QGraphicsItem.ItemIsMovable)

        r = PlaceItem.CIRCLE_RADIUS

        self.circle_select = QGraphicsEllipseItem(-r-4, -r-4, 2*r+8, 2*r+8)
        self.circle = QGraphicsEllipseItem(-r, -r, 2*r, 2*r)
        self.tokens_text = QGraphicsSimpleTextItem('')
        self.capacity_text = QGraphicsSimpleTextItem('')
        self.name_text = QGraphicsSimpleTextItem('')
        p = QPen()
        p.setColor(QColor(255, 0, 0))
        p.setWidthF(2)
        self.circle_select.setPen(p)
        self.is_selected = False

        self.update_texts()

        n_ports = 8
        self.ports = [Port(QPointF(r*cos(alpha), r*sin(alpha)),
                           self.place, self, editor)
                      for alpha in np.linspace(0, 2*pi*(n_ports-1)/n_ports, n_ports)]

        self.addToGroup(self.circle)
        self.addToGroup(self.circle_select)
        self.addToGroup(self.tokens_text)
        self.addToGroup(self.capacity_text)
        self.addToGroup(self.name_text)

        for p in self.ports:
            self.addToGroup(p)

        self.set_selected(self.is_selected)

    def set_selected(self, b):
        self.is_selected = b
        self.circle_select.setVisible(b)
        for p in self.ports:
            p.setVisible(b)

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
                 editor):
        super().__init__()
        self.transition = transition  # source Place object
        self.editor = editor
        self.setFlag(QGraphicsItem.ItemIsMovable)

        w, h = TransitionItem.RECT_WIDTH, TransitionItem.RECT_HEIGHT

        self.rect = QGraphicsRectItem(-w/2, -h/2, w, h)
        self.name_text = QGraphicsSimpleTextItem('name')
        self.attribute_text = QGraphicsSimpleTextItem('attribute')
        self.is_selected = False

        self.rect.setBrush(QColor('gray'))

        self.update_texts()

        self.addToGroup(self.rect)
        self.addToGroup(self.name_text)
        self.addToGroup(self.attribute_text)

        n_ports = 8
        self.ports = [Port(QPointF(x, y),
                           self.transition, self, editor)
                      for x, y in ((-w, 0), (w, 0), (w, 0))]

        for p in self.ports:
            self.addToGroup(p)

        self.set_selected(self.is_selected)

    def set_selected(self, b):
        self.is_selected = b
        self.rect.setPen(TransitionItem.selected_pen if self.is_selected else TransitionItem.normal_pen)
        for p in self.ports:
            p.setVisible(b)

    def update_texts(self):
        w, h = TransitionItem.RECT_WIDTH, TransitionItem.RECT_HEIGHT
        self.name_text.setText(self.transition.name)
        self.name_text.setPos(-6*len(self.transition.name)/2, -h/2-30)
        s = 'U(1~3.2)s'
        self.attribute_text.setText(s)
        self.attribute_text.setPos(-6*len(s)/2, h/2+5)

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
    ARC_END = '►'
    INHIBITOR_END = '◯'
    normal_pen = QPen(QColor('black'), 1)
    selected_pen = QPen(QColor('red'), 3)

    def __init__(self,
                 arc: Union[Arc, Inhibitor],
                 source: Port, target: Port,
                 editor):
        super().__init__()
        self.editor = editor
        #self.setFlag(QGraphicsItem.ItemIsMovable)

        self.source = source
        self.target = target

        self.line = QGraphicsLineItem()
        self.end_shape = QGraphicsSimpleTextItem('END')
        self.n_tokens_text = QGraphicsSimpleTextItem('n_tokens')
        self.is_selected = True

        self.set_arc_or_inhibitor(arc)
        self.update_texts()

        self.addToGroup(self.line)
        self.addToGroup(self.end_shape)
        self.addToGroup(self.n_tokens_text)

        self.update_ports()

        self.set_selected(self.is_selected)

    def set_arc_or_inhibitor(self, arc: Union[Arc, Inhibitor]):
        self.arc = arc
        if type(arc) == Arc:
            self.end_shape.setText(ArcItem.ARC_END)
        else:
            self.end_shape.setText(ArcItem.INHIBITOR_END)

    def update_ports(self):
        p1 = self.source.scenePos()
        p2 = self.target.scenePos()
        self.line.setLine(QLineF(p1, p2))
        v = p2-p1
        self.n_tokens_text.setPos(p1.x()+v.x()/2, p1.x()+v.y()/2-20)
        angle = atan2(v.y(), v.x())
        self.end_shape.setRotation(angle)
        self.end_shape.setPos(p2.x(), p2.y()-10)

    def set_selected(self, b):
        self.is_selected = b
        self.line.setPen(ArcItem.selected_pen if self.is_selected else ArcItem.normal_pen)

    def update_texts(self):
        p1 = self.source.scenePos()
        p2 = self.target.scenePos()
        v = p1 + (p2 - p1) / 2
        s = str(self.arc.n_tokens)
        self.n_tokens_text.setText(s)
        self.n_tokens_text.setPos(v.x()-6*len(s)/2, v.y()-20)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            self.editor.select(self)
            print('item mouse pressed')
            event.accept()
