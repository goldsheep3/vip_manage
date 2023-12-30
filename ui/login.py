from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QGridLayout, QWidget)

import ui.n_qt as nqt


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class LoginWidget(QWidget):
    def __init__(self, i18n):
        super().__init__()

        base_layout = QGridLayout()
        base_layout.setSpacing(10)
        base_layout.setContentsMargins(50, 50, 50, 50)
        base_layout.setColumnStretch(0, 1)
        base_layout.setColumnStretch(1, 1)
        base_layout.setColumnStretch(2, 1)
        base_layout.setRowStretch(0, 3)
        base_layout.setRowStretch(1, 1)
        base_layout.setRowStretch(2, 1)
        base_layout.setRowStretch(3, 1)
        base_layout.setRowStretch(4, 6)

        forget_button = nqt.PushText('忘记密码？', lambda: print(51))

        base_layout.addWidget(nqt.Text(i18n['MLogin']['press_key']), 1, 1)
        base_layout.addWidget(nqt.LineEdit(), 2, 1)
        base_layout.addWidget(forget_button, 3, 1)

        self.setLayout(base_layout)
