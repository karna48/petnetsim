from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from typing import Union
from . import Editor


class ItemProperties(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.editor: Union[Editor, None] = None

    def after_init(self, editor: Editor):
        self.editor = editor



