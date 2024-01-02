from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QGridLayout, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QMessageBox)
import hashlib
from peewee import Model, PrimaryKeyField, CharField, IntegerField

import ui.n_qt as nqt
from manage.login import login, verify, WrongKeyError


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class LoginWidget(QWidget):
    login_successful = Signal()

    def __init__(self, i18n, conn, window):
        super().__init__()
        self.conn = conn
        self.window = window
        self.trans = i18n['MLogin']

        base_layout = QGridLayout()
        base_layout.setSpacing(10)
        base_layout.setContentsMargins(50, 50, 50, 50)
        base_layout.setColumnStretch(0, 12)
        base_layout.setColumnStretch(1, 11)
        base_layout.setColumnStretch(2, 1)
        base_layout.setColumnStretch(3, 12)
        base_layout.setRowStretch(0, 3)
        base_layout.setRowStretch(1, 1)
        base_layout.setRowStretch(2, 1)
        base_layout.setRowStretch(3, 6)
        base_layout.setRowStretch(4, 1)

        password_edit = nqt.LineEdit()
        password_edit.returnPressed.connect(lambda: self.login(password_edit.text(), self.trans['wrong']))

        base_layout.addWidget(nqt.Text(self.trans['press_key']), 1, 1, 1, 2)
        base_layout.addWidget(password_edit, 2, 1)
        base_layout.addWidget(nqt.PushButton(self.trans['login'],
                                             lambda: self.login(password_edit.text(), self.trans['wrong'])), 2, 2)

        forget_button = nqt.PushText(self.trans['forget_pwd'],
                                     lambda: self.show_forget_tip(self.trans['forget']), align=Qt.AlignCenter)
        base_layout.addWidget(forget_button, 4, 1, 1, 2)

        self.setLayout(base_layout)

    def login(self, password, trans):
        try:
            login_code = login(self.conn, trans, True, password)
        except WrongKeyError:
            self.window.setEnabled(False)
            QMessageBox.information(self.window, trans['title'], trans['tip'])
            self.window.setEnabled(True)
        else:
            if login_code == 0:
                self.login_successful.emit()  # 发送切换Stacked信号
            else:
                QMessageBox.information(self.window, trans['title'], str(login_code))

    def show_forget_tip(self, trans):
        self.window.setEnabled(False)
        forget_tip = ForgetTip(trans, self.conn)
        forget_tip.exec_()
        self.window.setEnabled(True)


class ForgetTip(QDialog):
    def __init__(self, trans, conn):
        super().__init__()
        self.setWindowTitle(trans['title'])
        self.setFixedSize(300, 150)
        self.conn = conn

        layout = QVBoxLayout()

        layout.addWidget(nqt.Text(trans['tip1']))
        layout.addWidget(nqt.Text(trans['tip2']))

        key_line_edit = nqt.LineEdit()
        layout.addWidget(key_line_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(nqt.PushButton(trans['button1'],
                                               lambda: self.verify_key(key_line_edit.text(), trans)))
        button_layout.addWidget(nqt.PushButton(trans['button2'], self.reject))
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def verify_key(self, entered_key, trans):
        try:
            verify(self.conn, entered_key)
        except WrongKeyError:
            QMessageBox.warning(self, trans['wrong1'], trans['wrong2'])
        else:
            self.accept()
