from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from typing import Union
from .graphics_items import PlaceItem, TransitionItem, ArcItem


class ItemProperties(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = find_main_window(self)
        #self.editor = find_editor(self)

    def edits_enabled(self, enabled):
        edit_types = (QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox)
        for widget in self.findChildren(edit_types):
            widget.setEnabled(enabled)

    def item_selected(self, item):
        if item is None:
            self.setCurrentWidget(self.main_window.empty_props_page)
        elif isinstance(item, PlaceItem):
            self.setCurrentWidget(self.main_window.place_props_page)
        elif isinstance(item, TransitionItem):
            self.setCurrentWidget(self.main_window.transition_props_page)
        elif isinstance(item, ArcItem):
            self.setCurrentWidget(self.main_window.arc_props_page)


def find_main_window(widget: QWidget):
    while (p := widget.parent()) is not None:
        widget = p
    return widget


def find_editor(widget):
    return find_main_window(widget).editor

