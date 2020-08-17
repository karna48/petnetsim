from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from typing import Union
from .graphics_items import PlaceItem, TransitionItem, ArcItem
from petnetsim.elements import \
    Place, Transition, TransitionStochastic, \
    TransitionPriority, TransitionTimed, Arc


class ItemProperties(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = find_main_window(self)
        self.is_filling_forms = False

    def edits_enabled(self, enabled):
        edit_types = (QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox)
        widget: QWidget
        for widget in self.findChildren(edit_types):
            widget.setEnabled(enabled)

    def item_selected(self, item):
        editor = self.main_window.editor
        if item is None:
            self.setCurrentWidget(self.main_window.empty_props_page)
        elif isinstance(item, PlaceItem):
            self.is_filling_forms = True
            self.setCurrentWidget(self.main_window.place_props_page)
            self.main_window.place_name_lineEdit.setText(item.place.name)
            self.main_window.place_init_tokens_spinBox.setValue(item.place.capacity)
            self.main_window.place_capacity_spinBox.setValue(item.place.capacity)
            self.main_window.place_infinite_capacity_label.setText(f'(infinite capacity = {Place.INF_CAPACITY})')
            self.is_filling_forms = False

        elif isinstance(item, TransitionItem):
            self.setCurrentWidget(self.main_window.transition_props_page)
            self.main_window.transition_name_lineEdit.setText(item.transition.name)

        elif isinstance(item, ArcItem):
            self.setCurrentWidget(self.main_window.arc_props_page)

    def place_name_changed(self, name):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.place.name = name
            editor.selected.update_texts()

    def transition_name_changed(self, name):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.transition.name = name
            editor.selected.update_texts()


def find_main_window(widget: QWidget):
    #while (p := widget.parent()) is not None:
    p = widget.parent()
    while p is not None:
        widget = p
        p = widget.parent()
    return widget


def find_editor(widget):
    return find_main_window(widget).editor

