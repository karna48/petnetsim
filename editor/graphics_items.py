from math import sin, cos, pi
from typing import Union, Any

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from petnetsim.elements import Place, Transition, TransitionPriority, TransitionTimed, TransitionStochastic, Arc, \
    Inhibitor
from .mode import Mode


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

        self.circle_select = QGraphicsEllipseItem(-r - 4, -r - 4, 2 * r + 8.5, 2 * r + 8.5)
        self.circle = QGraphicsEllipseItem(-r, -r, 2 * r, 2 * r)
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
        self.ports = [Port(QPointF(r * cos(alpha), r * sin(alpha)),
                           self.place, self, editor, i)
                      for i, alpha in enumerate(np.linspace(0, 2 * pi * (n_ports - 1) / n_ports, n_ports))]

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
        self.name_text.setPos(-6 * len(self.place.name) / 2, -40)

        s = str(self.place.init_tokens)
        self.tokens_text.setText(s)
        self.tokens_text.setPos(-6 * len(s) / 2, -8)
        self.tokens_text.setVisible(self.place.init_tokens > 0)

        s = 'C=' + str(self.place.capacity)
        self.capacity_text.setText(s)
        self.capacity_text.setPos(-6 * len(s) / 2, 20)
        self.capacity_text.setVisible(self.place.capacity != Place.INF_CAPACITY)

    def update_tokens_text_simulation(self):
        s = str(self.place.tokens)
        self.tokens_text.setText(s)
        self.tokens_text.setPos(-6 * len(s) / 2, -8)
        self.tokens_text.setVisible(self.place.tokens > 0)

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
    NormalBrush = QBrush(QColor('gray'))
    FiredBrush = QBrush(QColor('orange'))

    def __init__(self,
                 transition: Union[Transition, TransitionTimed, TransitionPriority, TransitionStochastic],
                 editor):
        super().__init__()
        self.transition = transition  # source Place object
        self.editor = editor
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

        w, h = TransitionItem.RectWidth, TransitionItem.RectHeight

        self.rect = QGraphicsRectItem(-w / 2, -h / 2, w, h)
        self.name_text = QGraphicsSimpleTextItem('name')
        self.attribute_text = QGraphicsSimpleTextItem('attribute')
        self.is_selected = False

        self.rect.setBrush(TransitionItem.NormalBrush)

        self.update_texts()

        self.addToGroup(self.rect)
        self.addToGroup(self.name_text)
        self.addToGroup(self.attribute_text)

        port_centers = [QPointF(x, y) for x, y in
                        ((-w / 2, 0), (w / 2, 0),
                        (-w / 2, +h / 3), (w / 2, +h / 3),
                        (-w / 2, -h / 3), (w / 2, -h / 3))]
        t = self.transition
        self.ports = [Port(pc, t, self, editor, i) for i, pc in enumerate(port_centers)]

        for p in self.ports:
            self.addToGroup(p)

        self.hide_ports()
        self.set_selected(self.is_selected)

    def set_brush(self, is_fired):
        self.rect.setBrush(TransitionItem.FiredBrush if is_fired else TransitionItem.NormalBrush)

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
        self.name_text.setPos(-6 * len(self.transition.name) / 2, -h / 2 - 30)
        # TODO: different types

        if isinstance(self.transition, TransitionPriority):
            s = f'p={self.transition.priority}'
        elif isinstance(self.transition, TransitionStochastic):
            s = f'{self.transition.probability*100}%'
        elif isinstance(self.transition, TransitionTimed):
            s = self.transition.dist_time_str()
        else:
            s = ''

        self.attribute_text.setText(s)
        self.attribute_text.setPos(-6 * len(s) / 2, h / 2 + 5)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        selectable_with_ports_mousePressEvent(self, event)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if change == QGraphicsItem.ItemPositionChange:
            self.editor.item_moved(self.transition)

        return super().itemChange(change, value)

    def set_timed_pdist(self, func):
        if type(self.transition) == TransitionTimed:
            self.transition.p_distribution_func = func
        else:
            QMessageBox.critical(None, 'error', 'TransitionItem.set_timed_pdist requires transition to be TransitionTimed')

    def change_transition_type(self, cls: Union[Transition, TransitionTimed, TransitionPriority, TransitionStochastic]):
        old_t = self.transition
        if cls == Transition:
            new_t = Transition(old_t.name)
        elif cls == TransitionTimed:
            new_t = TransitionTimed(old_t.name, 1)
        elif cls == TransitionPriority:
            new_t = TransitionPriority(old_t.name, 1)
        elif cls == TransitionStochastic:
            new_t = TransitionStochastic(old_t.name, 0.5)
        else:
            raise RuntimeError('change_transition_type: wrong class:', str(cls))

        self.editor.substitute_object(old_t, new_t)
        self.transition = new_t


class ArcItem(QGraphicsItemGroup):
    NormalPen = QPen(QColor('black'), 1)
    SelectedPen = QPen(QColor('red'), 3)
    FiredMarkerBrush = QBrush(QColor('orange'))
    FiredMarkerRect = QRectF(-5, -5, 10, 10)

    def __init__(self,
                 arc: Union[Arc, Inhibitor],
                 source: Port, target: Port,
                 editor):
        super().__init__()
        self.editor = editor
        # self.setFlag(QGraphicsItem.ItemIsMovable)

        self.source = source
        self.target = target


        self.line_item = QGraphicsLineItem()
        self.n_tokens_text = QGraphicsSimpleTextItem('n_tokens')
        self.fired_marker = QGraphicsEllipseItem(ArcItem.FiredMarkerRect)
        self.fired_marker.setBrush(ArcItem.FiredMarkerBrush)

        self.fired_marker_t = 0.0  # interpolation coefficient

        self.is_selected = False

        self.end_shape = None
        self.set_arc_or_inhibitor(arc)
        self.update_texts()

        self.addToGroup(self.line_item)
        self.addToGroup(self.n_tokens_text)
        self.addToGroup(self.fired_marker)

        self.fired_marker_set_visibility(False)

        self.update_ports()

        self.set_selected(self.is_selected)

    def set_arc_or_inhibitor(self, arc: Union[Arc, Inhibitor]):
        self.arc = arc
        if self.end_shape is not None:
            self.removeFromGroup(self.end_shape)

        if isinstance(arc, Arc):
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
            self.end_shape = QGraphicsPathItem(arrow_path)
            self.end_shape.setBrush(QColor('black'))
        else:
            r = 7
            self.end_shape = QGraphicsEllipseItem(-r, -r, 2*r, 2*r)
            self.end_shape.setBrush(QColor('white'))
            self.end_shape.setPen(QColor('black'))

        self.addToGroup(self.end_shape)
        self.update_ports()

    def update_ports(self, p2: QPointF = None):
        p1 = self.source.scenePos()
        p2 = p2 if p2 is not None else self.target.scenePos()
        line = QLineF(p1, p2)
        self.line_item.setLine(line)
        center: QPointF = line.center()
        s = str(self.arc.n_tokens)
        self.n_tokens_text.setPos(center.x() - 6 * len(s) / 2, center.y() - 20)
        self.end_shape.setRotation(-line.angle())
        self.end_shape.setPos(p2.x(), p2.y())
        self.fired_marker_interpolate_position(self.fired_marker_t)

    def set_selected(self, b):
        self.is_selected = b
        self.line_item.setPen(ArcItem.SelectedPen if self.is_selected else ArcItem.NormalPen)

    def update_texts(self):
        center: QPointF = self.line_item.line().center()
        s = str(self.arc.n_tokens)
        self.n_tokens_text.setText(s)
        self.n_tokens_text.setPos(center.x() - 6 * len(s) / 2, center.y() - 20)
        self.n_tokens_text.setVisible(self.arc.n_tokens > 1)

    def fired_marker_set_visibility(self, is_visible):
        self.fired_marker.setVisible(is_visible)

    def fired_marker_interpolate_position(self, t):
        line: QLineF = self.line_item.line()
        self.fired_marker.setPos(line.pointAt(t))

    def shape(self) -> QPainterPath:
        bounding_width_half = 5
        pp = QPainterPath()

        l = self.line_item.line()  # copy of line
        p1 = l.p1()
        p2 = l.p2()
        normal_half = l.normalVector().unitVector()
        normal_half.setLength(bounding_width_half)
        nh_vec = normal_half.p2() - normal_half.p1()

        A = p1 + nh_vec
        B = p2 + nh_vec
        C = p2 - nh_vec
        D = p1 - nh_vec

        pp.addPolygon(QPolygonF([A, B, C, D]))
        pp.closeSubpath()

        return pp

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            self.editor.select(self)
            event.accept()


def selectable_with_ports_mousePressEvent(item, event):
    if event.button() == Qt.LeftButton:
        if item.editor.main_window.mode in (Mode.ArcSource, Mode.ArcTarget):
            point = event.scenePos()
            for port_item in item.ports:
                if port_item.contains(port_item.mapFromScene(point)):
                    item.editor.select_port(port_item)
                    break

        elif item.editor.main_window.mode in (Mode.Normal, Mode.Simulation):
            if item.is_selected:
                pass
            else:
                item.editor.select(item)
                event.accept()
