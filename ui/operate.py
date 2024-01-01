from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QGridLayout, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QButtonGroup, QListWidget,
                               QMessageBox)
from peewee import CharField, Model, IntegerField

import ui.n_qt as nqt


class OperateWidget(QWidget):
    def __init__(self, i18n, conn, window):
        super().__init__()
        self.conn = conn
        self.window = window
        self.trans = i18n['MOperate']
        self.i18n = i18n
        # 链接数据库
        self.base_info_model = self.create_tables_model()

        # 基础交互组件定义
        self.phone_number = nqt.LineEdit()
        self.phone_number.setContentsMargins(0, 5, 10, 5)
        self.name = nqt.LineEdit(True, '...')
        self.wechat = nqt.LineEdit(True, '...')
        self.card_id = nqt.LineEdit(True, '...')
        self.birthday = nqt.LineEdit(True, '...')
        self.money_value = nqt.Text('...')
        self.money_value.setAlignment(Qt.AlignCenter)
        self.history = QListWidget()
        self.history.setWordWrap(True)
        # .addItem(f'{data} {variation}{money_value}CNY {variation_type}[{category}{-note}]')
        # .addItem('2023.01.28 -300.00CNY 消费[服务1-测试]')  <- Sample
        self.money_plus_num = nqt.DoubleSpinBox(True)
        self.money_down_num = nqt.DoubleSpinBox(True)
        self.money_down_category = nqt.ComboBox(True)
        self.money_down_note = nqt.LineEdit(True)

        self.button_search = nqt.PushButton(self.trans['search'], lambda: print(1))
        self.button_exit = nqt.PushButton(self.trans['exit'], lambda: print(2))
        self.button_modify = nqt.PushButton(self.trans['modify_info'][1],
                                            lambda: print(21), True)
        self.button_money_plus = nqt.PushButton(self.trans['money_plus'][1],
                                                lambda: print(23), True)
        self.button_money_down = nqt.PushButton(self.trans['money_down'][1],
                                                lambda: print(24), True)

        self.radio_modify = nqt.RadioButton(self.trans['modify_info'][0],
                                            lambda: print(12))
        self.radio_money_plus = nqt.RadioButton(self.trans['money_plus'][0],
                                                lambda: print(14))
        self.radio_money_down = nqt.RadioButton(self.trans['money_down'][0],
                                                lambda: print(15))
        radio_group = QButtonGroup()
        radio_group.setExclusive(True)
        radio_group.addButton(self.radio_modify)
        radio_group.addButton(self.radio_money_plus)
        radio_group.addButton(self.radio_money_down)

        # 基础显示组件定义
        self.init_ui()

    def init_ui(self):
        info_layout = QGridLayout()  # 基本信息显示Grid
        info_layout.setSpacing(0)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.addWidget(nqt.Text(self.trans['phone_number']), 0, 0)
        info_layout.addWidget(self.phone_number, 0, 1, 1, 3)
        info_layout.addWidget(nqt.Text(self.trans['name']), 1, 0)
        info_layout.addWidget(self.name, 1, 1)
        info_layout.addWidget(nqt.Text(self.trans['wechat']), 2, 0)
        info_layout.addWidget(self.wechat, 2, 1)

        info_layout.addWidget(self.button_search, 0, 4)
        info_layout.addWidget(self.button_exit, 0, 5)
        info_layout.addWidget(nqt.Text(self.trans['card_id']), 1, 3)
        info_layout.addWidget(self.card_id, 1, 4, 1, 2)
        info_layout.addWidget(nqt.Text(self.trans['birthday']), 2, 3)
        info_layout.addWidget(self.birthday, 2, 4, 1, 2)

        info_layout.addWidget(nqt.Text(self.trans['money']), 0, 7, 1, 3)
        info_layout.addWidget(self.money_value, 1, 8, 2, 1)
        info_layout.addWidget(nqt.Text('CNY'), 2, 9)

        info_layout.setColumnStretch(0, 6)
        info_layout.setColumnStretch(1, 12)
        info_layout.setColumnStretch(2, 1)
        info_layout.setColumnStretch(3, 6)
        info_layout.setColumnStretch(4, 6)
        info_layout.setColumnStretch(5, 6)
        info_layout.setColumnStretch(6, 1)
        info_layout.setColumnStretch(7, 3)
        info_layout.setColumnStretch(8, 9)
        info_layout.setColumnStretch(9, 3)
        info_layout.setRowStretch(0, 1)
        info_layout.setRowStretch(1, 1)
        info_layout.setRowStretch(2, 1)
        info_widget = QWidget()
        info_widget.setLayout(info_layout)

        operate_layout = QGridLayout()
        operate_layout.addWidget(self.radio_modify, 0, 0, 1, 3)
        operate_layout.addWidget(self.button_modify, 0, 5)

        operate_layout.addWidget(self.radio_money_plus, 2, 0, 1, 3)
        operate_layout.addWidget(nqt.Text('＋', align=Qt.AlignRight | Qt.AlignVCenter), 3, 0)
        operate_layout.addWidget(self.money_plus_num, 3, 1, 1, 2)
        operate_layout.addWidget(nqt.Text('CNY'), 3, 3)
        operate_layout.addWidget(self.button_money_plus, 3, 5)

        operate_layout.addWidget(self.radio_money_down, 5, 0, 1, 3)
        operate_layout.addWidget(self.money_down_category, 6, 1, 1, 2)
        operate_layout.addWidget(self.money_down_note, 6, 3, 1, 2)
        operate_layout.addWidget(nqt.Text('－', align=Qt.AlignRight | Qt.AlignVCenter), 7, 0)
        operate_layout.addWidget(self.money_down_num, 7, 1, 1, 2)
        operate_layout.addWidget(nqt.Text('CNY'), 7, 3)
        operate_layout.addWidget(self.button_money_down, 7, 5)

        operate_layout.setColumnStretch(0, 1)
        operate_layout.setColumnStretch(1, 4)
        operate_layout.setColumnStretch(2, 4)
        operate_layout.setColumnStretch(3, 4)
        operate_layout.setColumnStretch(4, 4)
        operate_layout.setColumnStretch(5, 5)
        operate_layout.setRowStretch(0, 1)
        operate_layout.setRowStretch(1, 1)
        operate_layout.setRowStretch(2, 1)
        operate_layout.setRowStretch(3, 1)
        operate_layout.setRowStretch(4, 1)
        operate_layout.setRowStretch(5, 1)
        operate_layout.setRowStretch(6, 1)
        operate_layout.setRowStretch(7, 1)

        operate_layout.setSpacing(3)
        operate_layout.setContentsMargins(25, 15, 25, 15)
        operate_gbox = QGroupBox()
        operate_gbox.setLayout(operate_layout)
        operate_gbox.setTitle(self.trans['operate'])

        history_layout = QVBoxLayout()
        history_layout.setSpacing(0)
        history_layout.setContentsMargins(5, 5, 5, 5)
        history_layout.addWidget(self.history)

        history_gbox = QGroupBox()
        history_gbox.setLayout(history_layout)
        history_gbox.setTitle(self.trans['history'])

        down_layout = QHBoxLayout()  # 分隔最近明细和操作区域
        down_layout.setSpacing(15)
        down_layout.setContentsMargins(0, 0, 0, 0)
        down_layout.addWidget(history_gbox, 4)
        down_layout.addWidget(operate_gbox, 7)
        down_widget = QWidget()
        down_widget.setLayout(down_layout)

        base_layout = QVBoxLayout()  # 分隔操作区上下
        base_layout.setSpacing(10)
        base_layout.setContentsMargins(50, 25, 50, 25)
        base_layout.addWidget(info_widget, 1)
        base_layout.addWidget(down_widget, 3)

        self.setLayout(base_layout)

    def create_tables_model(self):
        class BaseModel(Model):
            class Meta:
                database = self.conn

        class BaseInfo(BaseModel):
            phone_number = IntegerField(unique=True, null=False)
            card_id = IntegerField(primary_key=True, unique=True, null=False)
            name = CharField()
            wechat = CharField()
            birthday = IntegerField()
            balance = IntegerField(null=False)

        class History(BaseModel):
            card_id = IntegerField(primary_key=True, unique=True, null=False)
            time = CharField(null=False)
            category = CharField(null=False)
            note = CharField(null=True)
            i_and_e = IntegerField(null=False)
            balance = IntegerField(null=False)

        class Admin(BaseModel):
            id = IntegerField(primary_key=True)
            password_hash = CharField(null=False)
            sugar = IntegerField(null=False)

        return BaseInfo, History, Admin
