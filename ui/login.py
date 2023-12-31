from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QGridLayout, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QMessageBox)
import hashlib
import peewee as pw

import ui.n_qt as nqt


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
        password_edit.returnPressed.connect(lambda: self.login(password_edit.text(), i18n['MLogin']['wrong']))

        base_layout.addWidget(nqt.Text(i18n['MLogin']['press_key']), 1, 1, 1, 2)
        base_layout.addWidget(password_edit, 2, 1)
        base_layout.addWidget(nqt.PushButton(i18n['MLogin']['login'],
                                             lambda: self.login(password_edit.text(), i18n['MLogin']['wrong'])), 2, 2)

        forget_button = nqt.PushText(i18n['MLogin']['forget_pwd'],
                                     lambda: self.show_forget_tip(i18n['MLogin']['forget']), align=Qt.AlignCenter)
        base_layout.addWidget(forget_button, 4, 1, 1, 2)

        self.setLayout(base_layout)

    def login(self, password, trans):
        class Admin(pw.Model):
            id = pw.PrimaryKeyField()
            password_hash = pw.CharField()
            sugar = pw.IntegerField()

            class Meta:
                database = self.conn

        try:
            pwd_md5 = hashlib.md5()
            pwd_md5.update(password.encode('utf-8'))
            pwdhash = pwd_md5.hexdigest()
            admin_record = Admin.select().where(Admin.password_hash == pwdhash).get()
            sugar = admin_record.sugar
        except Admin.DoesNotExist:
            self.window.setEnabled(False)
            QMessageBox.information(self.window, trans['title'], trans['tip'])
            self.window.setEnabled(True)
        else:
            if sugar == 160523498730:
                self.login_successful.emit()  # 发送切换Stacked信号

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
                                               lambda: self.verify_key(key_line_edit.text(), trans['verify'])))
        button_layout.addWidget(nqt.PushButton(trans['button2'], self.reject))
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def verify_key(self, entered_key, trans):
        class Admin(pw.Model):
            id = pw.PrimaryKeyField()
            password_hash = pw.CharField()
            sugar = pw.IntegerField()

            class Meta:
                database = self.conn

        try:
            key_md5 = hashlib.md5()
            key_md5.update(entered_key.encode('utf-8'))
            keyhash = key_md5.hexdigest()
            admin_record = Admin.select().where(Admin.password_hash == keyhash).get()
            sugar = admin_record.sugar
        except Admin.DoesNotExist:
            QMessageBox.warning(self, trans['wrong1'], trans['wrong2'])
        else:
            if sugar == 202838234617:
                self.accept()
