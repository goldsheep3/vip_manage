from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QGridLayout, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QButtonGroup, QListWidget,
                               QMessageBox, QStackedWidget, QToolBox, QDialog, QInputDialog)

from lib.n_qt import LineEdit, Text, DoubleSpinBox, ComboBox, PushButton, RadioButton
from lib.sql_table import create_tables_model
from manage.action import search

#
# class RegisterWidget(QDialog):
#     def __init__(self, trans):
#         super().__init__()
#         self.setWindowTitle(trans['title'])
#         self.setFixedSize(300, 150)
#
#         layout = QGridLayout(self)
#         layout.addWidget(Text('* ' + trans['phone_number']), 0, 0)
#         layout.addWidget(Text(trans['name']), 1, 0)
#         layout.addWidget(Text(trans['wechat']), 2, 0)
#         layout.addWidget(Text(trans['birthday']), 3, 0)
#         layout.addWidget(Text(trans['money_plus']), 4, 0)
#
#         phone_number = LineEdit()
#         name = LineEdit()
#         wechat = LineEdit()
#         birthday = LineEdit()
#
#         money_plus = PushButton(trans['reg']['mp'], lambda: print(3012))
#         money_edit = PushButton(trans['reg']['me'], lambda: print(3013))
#
#         layout.addWidget(phone_number, 0, 1, 1, 2)
#         layout.addWidget(name, 1, 1, 1, 2)
#         self.widget = layout.addWidget(wechat, 2, 1, 1, 2)
#         layout.addWidget(birthday, 3, 1, 1, 2)
#         layout.addWidget(money_plus, 4, 1)
#         layout.addWidget(money_edit, 4, 2)
#
#         key_line_edit = LineEdit()
#         layout.addWidget(key_line_edit)
#
#         button_layout = QHBoxLayout()
#         button_layout.addWidget(PushButton(trans['button1'],
#                                            lambda: self.verify_key(key_line_edit.text(), trans)))
#         button_layout.addWidget(PushButton(trans['button2'], self.reject))
#         layout.addLayout(button_layout)
#
#     def verify_key(self, entered_key, trans):
#         try:
#             check_md5_key(self.conn, entered_key, key_sugar.get('verify'))
#         except ValueError:
#             QMessageBox.warning(self, trans['wrong1'], trans['wrong2'])
#         else:
#             self.accept()
#
#
# class RegisterMoneyPlus(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         operate_layout = QGridLayout()
#
#         operate_layout.addWidget(Text(self.trans['now_operate']), 0, 0)
#         operate_layout.addWidget(self.radio_money_plus, 0, 1, 1, 1)
#         operate_layout.addWidget(self.radio_money_down, 0, 2, 1, 2)
#
#         operate_layout.addWidget(Text(self.trans['category']), 1, 0)
#         operate_layout.addWidget(self.trade_category, 1, 1)
#         operate_layout.addWidget(self.trade_note, 1, 2, 1, 2)
#         operate_layout.addWidget(Text(self.trans['pay1']), 2, 0)
#         operate_layout.addWidget(self.amount, 2, 1)
#         operate_layout.addWidget(Text('CNY'), 2, 2)
#         operate_layout.addWidget(Text(self.trans['pay2']), 3, 0)
#         operate_layout.addWidget(self.discount, 3, 1)
#         operate_layout.addWidget(Text('CNY'), 3, 2)
#         operate_layout.addWidget(Text('3,3'), 3, 3, 1, 2)
#         operate_layout.addWidget(Text('3,4'), 3, 5)
#         operate_layout.addWidget(Text('3,5'), 3, 6)
#         operate_layout.addWidget(Text(self.trans['pay3']), 4, 0)
#         operate_layout.addWidget(self.paid_amount, 4, 1)
#         operate_layout.addWidget(Text('CNY'), 4, 2)
#         operate_layout.addWidget(Text('6,2'), 6, 2, 1, 3)
#         operate_layout.addWidget(Text('6,5'), 6, 5, 1, 2)
#
#         operate_layout.setColumnStretch(0, 2)
#         operate_layout.setColumnStretch(1, 3)
#         operate_layout.setColumnStretch(2, 2)
#         operate_layout.setColumnStretch(3, 1)
#         operate_layout.setColumnStretch(4, 1)
#         operate_layout.setColumnStretch(5, 2)
#         operate_layout.setColumnStretch(6, 2)
#         [operate_layout.setRowStretch(i, 1) for i in range(7)]
#         operate_layout.setSpacing(5)
#         operate_layout.setContentsMargins(25, 15, 25, 15)


class NoFullPhoneTip(QDialog):
    def __init__(self, trans):
        super().__init__()
        self.setWindowTitle(trans['errors']['error'])
        self.setFixedSize(300, 150)
        self.setResult(33)

        button_layout = QHBoxLayout()
        button_layout.addWidget(PushButton(trans['reg']['reg'], lambda: self.exit(35)))
        button_layout.addWidget(PushButton(trans['reg']['no_reg'], lambda: self.exit(34)))
        button_layout.addWidget(PushButton(trans['reg']['close'], self.reject))

        layout = QVBoxLayout(self)
        layout.addWidget(Text(trans['errors']['not_found_phone'] + '\n' + trans['errors']['nf_11']), 2)
        layout.addLayout(button_layout, 1)

    def exit(self, value):
        self.setResult(value)
        self.accept()

