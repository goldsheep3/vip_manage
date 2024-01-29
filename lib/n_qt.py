from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton, QSizePolicy, QRadioButton, QComboBox, QDoubleSpinBox,
                               QAbstractSpinBox, QGridLayout, QSpinBox)


class GridLayout(QGridLayout):

    def setAllColumnStretch(self, stretch: list | int):
        if isinstance(stretch, int):
            stretch = [1] * stretch
        [self.setColumnStretch(i, j) for i, j in enumerate(stretch)]

    def setAllRowStretch(self, stretch: list | int):
        if isinstance(stretch, int):
            stretch = [1] * stretch
        [self.setRowStretch(i, j) for i, j in enumerate(stretch)]


class Text(QLabel):
    def __init__(self, text, align=None):
        super().__init__(text)
        if align:
            self.setAlignment(align)


class LineEdit(QLineEdit):
    def __init__(self, read_only=False, text='', pwd=False):
        super().__init__()
        self.setContentsMargins(0, 2, 0, 2)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setText(text)
        if read_only:
            self.setReadOnly(True)
        if pwd:
            # noinspection PyUnresolvedReferences
            self.setEchoMode(QLineEdit.Password)


class PushText(QLabel):
    def __init__(self, text, function, align=None):
        super().__init__()
        self.setTextFormat(Qt.RichText)
        self.setText(f'<span style="color: blue;"><u>{text}</u></span>')
        self.linkActivated.connect(function)
        if align:
            self.setAlignment(align)

    def mousePressEvent(self, event):
        self.linkActivated.emit(self.text())

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)


class PushButton(QPushButton):
    def __init__(self, text, function, read_only=False):
        super().__init__()
        self.setText(text)
        self.clicked.connect(function)
        self.setContentsMargins(5, 5, 5, 5)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if read_only:
            self.setEnabled(False)


class RadioButton(QRadioButton):
    def __init__(self, text, function, read_only=False):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setText(text)
        self.clicked.connect(function)
        if read_only:
            self.setEnabled(False)


class ComboBox(QComboBox):
    def __init__(self, read_only=False):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if read_only:
            self.setEnabled(False)


class SpinBox(QSpinBox):
    def __init__(self, value: int = 0, no_buttons=False, read_only=False):
        super().__init__()
        self.setValue(value)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignRight)
        if no_buttons:
            # noinspection PyUnresolvedReferences
            self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        if read_only:
            self.setEnabled(False)


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, value: float = 0.00, no_buttons=False, read_only=False):
        super().__init__()
        self.setValue(value)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignRight)
        if no_buttons:
            # noinspection PyUnresolvedReferences
            self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        if read_only:
            self.setEnabled(False)
