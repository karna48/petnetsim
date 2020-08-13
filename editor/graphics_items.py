from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from petnetsim.elements import Place, Transition, TransitionPriority, TransitionTimed, TransitionStochastic, Arc, Inhibitor
from typing import Union, List, Any
from math import sin, cos, atan2, pi
import numpy as np


class Port(QGraphicsRectItem):
    RectSize = QSizeF(10.0, 10.0)
    NormalBrush = QBrush(QColor('white'))
    SelectedBrush = QBrush(QColor('blue'))

    def __init__(self, center: QPointF, assoc_obj, assoc_item, editor, number):
        v = QPointF(Port.RectSize.width() / 2, Port.RectSize.height() / 2)
        r = QRectF(-v, Port.RectSize)
        super().__init__(r)
        self.number = number
        self.setPos(center)
        self.assoc_obj = assoc_obj
        self.assoc_item = assoc_item
        self.setBrush(Port.NormalBrush)


class PlaceItem(QGraphicsItemGroup):
    CircleRadius = 20

    def __init__(self, place: Place, editor):
        super().__init__()
        self.place = place  # source Place object
        self.editor = editor
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

        r = PlaceItem.CircleRadius

        self.circle_select = QGraphicsEllipseItem(-r-4, -r-4, 2*r+8.5, 2*r+8.5)
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
                           self.place, self, editor, i)
                      for i, alpha in enumerate(np.linspace(0, 2*pi*(n_ports-1)/n_ports, n_ports))]

        self.addToGroup(self.circle)
        self.addToGroup(self.circle_select)
        self.addToGroup(self.tokens_text)
        self.addToGroup(self.capacity_text)
        self.addToGroup(self.name_text)

        for p in self.ports:
            self.addToGroup(p)

        self.hide_ports()
        self.set_selected(self.is_selected)

    def show_ports(self):
        for p in self.ports:
            p.setVisible(True)

    def hide_ports(self):
        for p in self.ports:
            p.setVisible(False)

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
        self.capacity_text.setVisible(self.place.capacity != Place.INF_CAPACITY)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        selectable_with_ports_mousePressEvent(self, event)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if change == QGraphicsItem.ItemPositionChange:
            self.editor.item_moved(self.place)

        return super().itemChange(change, value)


class TransitionItem(QGraphicsItemGroup):
    RectWidth = 12
    RectHeight = 46
    NormalPen = QPen(QColor('black'), 1)
    SelectedPen = QPen(QColor('red'), 3)

    def __init__(self,
                 transition: Union[Transition, TransitionTimed, TransitionPriority, TransitionStochastic],
                 editor):
        super().__init__()
        self.transition = transition  # source Place object
        self.editor = editor
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

        w, h = TransitionItem.RectWidth, TransitionItem.RectHeight

        self.rect = QGraphicsRectItem(-w/2, -h/2, w, h)
        self.name_text = QGraphicsSimpleTextItem('name')
        self.attribute_text = QGraphicsSimpleTextItem('attribute')
        self.is_selected = False

        self.rect.setBrush(QColor('gray'))

        self.update_texts()

        self.addToGroup(self.rect)
        self.addToGroup(self.name_text)
        self.addToGroup(self.attribute_text)

        self.ports = [Port(QPointF(x, y),
                           self.transition, self, editor, i)
                      for i, (x, y) in
                        enumerate(
                            ((-w/2, 0), (w/2, 0),
                             (-w/2, +h/3), (w/2, +h/3),
                             (-w/2, -h/3), (w/2, -h/3)))]

        for p in self.ports:
            self.addToGroup(p)

        self.hide_ports()
        self.set_selected(self.is_selected)

    def show_ports(self):
        for p in self.ports:
            p.setVisible(True)

    def hide_ports(self):
        for p in self.ports:
            p.setVisible(False)

    def set_selected(self, b):
        self.is_selected = b
        self.rect.setPen(TransitionItem.SelectedPen if self.is_selected else TransitionItem.NormalPen)

    def update_texts(self):
        w, h = TransitionItem.RectWidth, TransitionItem.RectHeight
        self.name_text.setText(self.transition.name)
        self.name_text.setPos(-6*len(self.transition.name)/2, -h/2-30)
        s = 'U(1~3.2)s'
        self.attribute_text.setText(s)
        self.attribute_text.setPos(-6*len(s)/2, h/2+5)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        selectable_with_ports_mousePressEvent(self, event)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if change == QGraphicsItem.ItemPositionChange:
            self.editor.item_moved(self.transition)

        return super().itemChange(change, value)


class ArcItem(QGraphicsItemGroup):
    NormalPen = QPen(QColor('black'), 1)
    SelectedPen = QPen(QColor('red'), 3)

    def __init__(self,
                 arc: Union[Arc, Inhibitor],
                 source: Port, target: Port,
                 editor):
        super().__init__()
        self.editor = editor
        #self.setFlag(QGraphicsItem.ItemIsMovable)

        self.source = source
        self.target = target

        arrow_path = QPainterPath()

        arrow_path.addPolygon(
            QPolygonF(
                (QPointF(0, 0),
                 QPointF(-8, -3),
                 QPointF(-8, +3),
                 QPointF(0, 0)
                 )
            )
        )

        self.line = QGraphicsLineItem()
        self.end_shape = QGraphicsPathItem(arrow_path)
        self.end_shape.setBrush(QColor('black'))
        self.n_tokens_text = QGraphicsSimpleTextItem('n_tokens')
        self.is_selected = False

        self.set_arc_or_inhibitor(arc)
        self.update_texts()

        self.addToGroup(self.line)
        self.addToGroup(self.end_shape)
        self.addToGroup(self.n_tokens_text)

        self.update_ports()

        self.set_selected(self.is_selected)

    def set_arc_or_inhibitor(self, arc: Union[Arc, Inhibitor]):
        self.arc = arc
        # if type(arc) == Arc:
        #     self.end_shape.setText(ArcItem.ARC_END)
        # else:
        #     self.end_shape.setText(ArcItem.INHIBITOR_END)

    def update_ports(self, p2: QPointF = None):
        p1 = self.source.scenePos()
        p2 = p2 if p2 is not None else self.target.scenePos()
        line = QLineF(p1, p2)
        self.line.setLine(line)
        center: QPointF = line.center()
        s = str(self.arc.n_tokens)
        self.n_tokens_text.setPos(center.x()-6*len(s)/2, center.y()-20)
        self.end_shape.setRotation(-line.angle())
        self.end_shape.setPos(p2.x(), p2.y())

    def set_selected(self, b):
        self.is_selected = b
        self.line.setPen(ArcItem.SelectedPen if self.is_selected else ArcItem.NormalPen)

    def update_texts(self):
        center: QPointF = self.line.line().center()
        s = str(self.arc.n_tokens)
        self.n_tokens_text.setText(s)
        self.n_tokens_text.setPos(center.x()-6*len(s)/2, center.y()-20)
        self.n_tokens_text.setVisible(self.arc.n_tokens > 1)

    def shape(self) -> QPainterPath:
        pp = QPainterPath()
        rect = self.line.boundingRect()
        if rect.width() < 5:
            rem = 5 - rect.width()
            rect.setX(rect.x()+rem/2)
            rect.setWidth(rect.width()+rem)
        if rect.height() < 5:
            rem = 5 - rect.height()
            rect.setY(rect.y()+rem/2)
            rect.setHeight(rect.height()+rem)
        pp.addRect(rect)
        return pp

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            self.editor.select(self)
            print('ArcItem mouse pressed and accepted')
            event.accept()


def selectable_with_ports_mousePressEvent(item, event):
    from . import Editor
    if event.button() == Qt.LeftButton:
        if item.editor.mode in (Editor.Mode.ArcSource, Editor.Mode.ArcTarget):
            point = event.scenePos()
            for port_item in item.ports:
                if port_item.contains(port_item.mapFromScene(point)):
                    item.editor.select_port(port_item)
                    break

        elif item.editor.mode == Editor.Mode.Normal:
            if item.is_selected:
                pass
            else:
                item.editor.select(item)
                event.accept()