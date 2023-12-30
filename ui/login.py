from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QGridLayout, QWidget)
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

    def __init__(self, i18n, conn):
        super().__init__()
        self.conn = conn

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
        password_edit.returnPressed.connect(lambda: self.login(password_edit.text()))

        base_layout.addWidget(nqt.Text(i18n['MLogin']['press_key']), 1, 1, 1, 2)
        base_layout.addWidget(password_edit, 2, 1)
        base_layout.addWidget(nqt.PushButton(i18n['MLogin']['login'],
                                             lambda: self.login(password_edit.text())), 2, 2)

        forget_button = nqt.PushText('忘记密码？', lambda: print(51), align=Qt.AlignCenter)
        base_layout.addWidget(forget_button, 4, 1, 1, 2)

        self.setLayout(base_layout)

    def login(self, password):
        class Admin(pw.Model):
            id = pw.PrimaryKeyField()
            password_hash = pw.CharField()
            sugar = pw.IntegerField()

            class Meta:
                database = self.conn

        pwd_md5 = hashlib.md5()
        pwd_md5.update(password.encode('utf-8'))
        pwdhash = pwd_md5.hexdigest()

        try:
            admin_record = Admin.select().where(Admin.password_hash == pwdhash).get()
            sugar = admin_record.sugar
        except Admin.DoesNotExist:
            print('Wrong Key.')
        else:
            if sugar == 160523498730:
                print('Key Right')
                self.login_successful.emit()
            elif sugar == 202838234617:
                print('Reset Key?')


        # setCurrentIndex(0)

        # SHA FOR: Initial commit

