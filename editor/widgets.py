from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from typing import Union
from .graphics_items import PlaceItem, TransitionItem, ArcItem
from petnetsim.elements import \
    Place, Transition, TransitionStochastic, \
    TransitionPriority, TransitionTimed, Arc, \
    constant_distribution, uniform_distribution


class ItemProperties(QStackedWidget):
    TimedPDists = [('constant t = t_min', constant_distribution),
                   ('uniform [t_min; t_max]', uniform_distribution)]

    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = self.window()
        self.is_filling_forms = False

    def after_init(self):
        self.is_filling_forms = True
        for name, _ in ItemProperties.TimedPDists:
            self.main_window.transition_timed_pdist_comboBox.addItem(name)
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
            transition_types_stackedWidget = self.main_window.transition_types_stackedWidget
            self.main_window.transition_name_lineEdit.setText(item.transition.name)
            if type(item.transition) == Transition:
                transition_types_stackedWidget.setCurrentWidget(self.main_window.transition_normal_page)
            elif type(item.transition) == TransitionPriority:
                transition_types_stackedWidget.setCurrentWidget(self.main_window.transition_priority_page)

            elif type(item.transition) == TransitionTimed:
                transition_types_stackedWidget.setCurrentWidget(self.main_window.transition_timed_page)
            elif type(item.transition) == TransitionStochastic:
                transition_types_stackedWidget.setCurrentWidget(self.main_window.transition_stochastic_page)
        elif isinstance(item, ArcItem):
            self.setCurrentWidget(self.main_window.arc_props_page)
            self.main_window.arc_name_lineEdit.setText(item.arc.name)
            self.main_window.arc_n_tokens_spinBox.setValue(item.arc.n_tokens)

    def place_name_changed(self, name):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.place.name = name
            editor.selected.update_texts()

    def place_init_tokens_changed(self, value: int):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.place.init_tokens = value
            editor.selected.update_texts()

    def place_capacity_changed(self, value: int):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.place.capacity = value
            editor.selected.update_texts()

    def transition_name_changed(self, name):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.transition.name = name
            editor.selected.update_texts()

    def transition_type_changed(self, class_name):
        if not self.is_filling_forms:
            classes = [Transition, TransitionTimed, TransitionStochastic, TransitionPriority]
            try:
                idx = [c.__name__ for c in classes].index(class_name)
                cls = classes[idx]
            except ValueError:
                QMessageBox.critical('wrong class name of transition:'+class_name)
                return

            editor = self.main_window.editor
            editor.selected.change_transition_type(cls)
            self.item_selected(editor.selected)

    def transition_timed_pdist_changed(self, idx):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            name, func = ItemProperties.TimedPDists[idx]
            editor.selected.set_timed_pdist(func)
            editor.selected.update_texts()

    def arc_name_changed(self, name: str):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.arc.name = name

    def arc_n_tokens_changed(self, value: int):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.arc.n_tokens = value
            editor.selected.update_texts()

    def arc_inhibitor_checkbox_toggled(self, toggled: bool):
        if not self.is_filling_forms:
            print('TODO: arc/inhibitor switch')
