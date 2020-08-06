
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .scene import PetriNetScene
import petnetsim.elements


class PlaceGraphicsItem(QGraphicsItemGroup):
    def __init__(self, place: petnetsim.elements.Place):
        super().__init__()
        self.place = place  # source Place object

        self.circle = QGraphicsEllipseItem(0, 0, 30, 30)
        self.tokens_text = QGraphicsSimpleTextItem ('')
        self.capacity_text = QGraphicsSimpleTextItem ('')
        self.name_text = QGraphicsSimpleTextItem ('')
        self.name_text.setPos(-10, -20)

        self.update_texts()

        self.addToGroup(self.circle)
        self.addToGroup(self.tokens_text)
        self.addToGroup(self.capacity_text)
        self.addToGroup(self.name_text)

    def update_texts(self):
        self.name_text.setText(self.place.name)
        self.tokens_text.setText(str(self.place.init_tokens))
        self.capacity_text.setText('C='+str(self.place.capacity))


class Editor(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(PetriNetScene())

        self.place_items = []
        self.transition_items = []
        self.arc_items = []

        test_place = petnetsim.elements.Place('PlaceA', 5, capacity=3)
        test_place_item = PlaceGraphicsItem(test_place)
        test_place_item.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene().addItem(test_place_item)

        #print('viewport:', )

    def keyPressEvent(self, key_event: QKeyEvent):
        print(key_event.key())

        if key_event.key() == ord('A'):
            print('add arc')

