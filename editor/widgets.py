from PyQt5 import uic
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

        uic.loadUi('editor/item_properties.ui', self)

        self.main_window = self.window()
        self.is_filling_forms = False

    def after_init(self):
        self.is_filling_forms = True
        for name, _ in ItemProperties.TimedPDists:
            self.transition_timed_pdist_comboBox.addItem(name)
        self.is_filling_forms = False

    def edits_enabled(self, enabled):
        edit_types = (QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox)
        widget: QWidget
        for widget in self.findChildren(edit_types):
            widget.setEnabled(enabled)

    def item_selected(self, item):
        editor = self.main_window.editor
        if item is None:
            self.setCurrentWidget(self.empty_props_page)
        elif isinstance(item, PlaceItem):
            self.is_filling_forms = True
            self.setCurrentWidget(self.place_props_page)
            self.place_name_lineEdit.setText(item.place.name)
            self.place_init_tokens_spinBox.setValue(item.place.capacity)
            self.place_capacity_spinBox.setValue(item.place.capacity)
            self.place_infinite_capacity_label.setText(f'(infinite capacity = {Place.INF_CAPACITY})')
            self.is_filling_forms = False

        elif isinstance(item, TransitionItem):
            self.setCurrentWidget(self.transition_props_page)
            transition_types_stackedWidget = self.transition_types_stackedWidget
            self.is_filling_forms = True
            self.transition_name_lineEdit.setText(item.transition.name)

            # TODO: create lookup for classes and displayed names (decouple from gui inside .ui file)
            self.transition_type_comboBox.setCurrentText(item.transition.__class__.__name__)
            if type(item.transition) == Transition:
                transition_types_stackedWidget.setCurrentWidget(self.transition_normal_page)
            elif type(item.transition) == TransitionPriority:
                transition_types_stackedWidget.setCurrentWidget(self.transition_priority_page)
                self.transition_priority_spinBox.setValue(item.transition.priority)
            elif type(item.transition) == TransitionTimed:
                transition_types_stackedWidget.setCurrentWidget(self.transition_timed_page)
                self.transition_t_min_doubleSpinBox.setValue(item.transition.t_min)
                self.transition_t_max_doubleSpinBox.setValue(item.transition.t_max)
            elif type(item.transition) == TransitionStochastic:
                transition_types_stackedWidget.setCurrentWidget(self.transition_stochastic_page)
                self.transition_probability_percent_spinBox.setValue(item.transition.probability*100)
            self.is_filling_forms = False
        elif isinstance(item, ArcItem):
            self.setCurrentWidget(self.arc_props_page)
            self.is_filling_forms = True
            self.arc_name_lineEdit.setText(item.arc.name)
            self.arc_n_tokens_spinBox.setValue(item.arc.n_tokens)
            self.arc_inhibitor_checkBox.setChecked(type(item.arc) != Arc)
            self.is_filling_forms = False

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

    def transition_priority_changed(self, value: int):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.transition.priority = value
            editor.selected.update_texts()

    def transition_pdist_changed_idx(self, idx: int):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            name, func = ItemProperties.TimedPDists[idx]
            editor.selected.set_timed_pdist(func)
            editor.selected.update_texts()

    def transition_t_min_changed(self, value: float):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.transition.t_min = value
            editor.selected.update_texts()

    def transition_t_max_changed(self, value: float):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.transition.t_max = value
            editor.selected.update_texts()

    def transition_probability_percent_changed(self, value: int):
        if not self.is_filling_forms:
            editor = self.main_window.editor
            editor.selected.transition.probability = value / 100.0
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

    def arc_inhibitor_toggled(self, toggled: bool):
        if not self.is_filling_forms:
            print('TODO: arc/inhibitor switch')
