from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton, QSizePolicy, QRadioButton, QComboBox, QDoubleSpinBox)


class NText(QLabel):
    def __init__(self, text, align=None):
        super().__init__(text)
        if align:
            self.setAlignment(align)


class CLEdit(QLineEdit):
    def __init__(self, read_only=False, text=''):
        super().__init__()
        self.setContentsMargins(0, 2, 0, 2)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setText(text)
        if read_only:
            self.setReadOnly(True)


class BButton(QPushButton):
    def __init__(self, text, function, read_only=False):
        super().__init__()
        self.setText(text)
        self.clicked.connect(function)
        self.setContentsMargins(5, 5, 5, 5)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if read_only:
            self.setEnabled(False)


class RButton(QRadioButton):
    def __init__(self, read_only=False):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if read_only:
            self.setEnabled(False)


class CBox(QComboBox):
    def __init__(self, read_only=False):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if read_only:
            self.setEnabled(False)


class DSBox(QDoubleSpinBox):
    def __init__(self, read_only=False):
        super().__init__()
        if read_only:
            self.setEnabled(False)
