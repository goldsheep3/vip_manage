from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QGridLayout, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QButtonGroup, QListWidget,
                               QMessageBox)

from lib.n_qt import LineEdit, Text, DoubleSpinBox, ComboBox, PushButton, RadioButton
from lib.sql_table import create_tables_model


class OperateWidget(QWidget):
    def __init__(self, i18n, conn, window):
        super().__init__()
        self.conn = conn
        self.window = window
        self.trans = i18n['MOperate']
        self.i18n = i18n
        # 链接数据库
        self.base_info_model = create_tables_model(self.conn)

        # 基础交互组件定义
        self.phone_number = LineEdit()
        self.phone_number.setContentsMargins(0, 5, 10, 5)
        self.name = LineEdit(True, '...')
        self.wechat = LineEdit(True, '...')
        self.card_id = LineEdit(True, '...')
        self.birthday = LineEdit(True, '...')
        self.money_value = Text('...')
        self.money_value.setAlignment(Qt.AlignCenter)
        self.history = QListWidget()
        self.history.setWordWrap(True)
        # .addItem(f'{data} {variation}{money_value}CNY {variation_type}[{category}{-note}]')
        # .addItem('2023.01.28 -300.00CNY 消费[服务1-测试]')  <- Sample
        self.money_plus_num = DoubleSpinBox(True)
        self.money_down_num = DoubleSpinBox(True)
        self.money_down_category = ComboBox(True)
        self.money_down_note = LineEdit(True)

        self.button_search = PushButton(self.trans['search'], self.on_search_button_clicked)
        self.button_exit = PushButton(self.trans['exit'], self.on_exit_button_clicked, True)
        self.button_modify = PushButton(self.trans['modify_info'][1],
                                        lambda: print(21), True)
        self.button_money_plus = PushButton(self.trans['money_plus'][1],
                                            lambda: print(23), True)
        self.button_money_down = PushButton(self.trans['money_down'][1],
                                            lambda: print(24), True)

        self.radio_modify = RadioButton(self.trans['modify_info'][0],
                                        lambda: print(12), True)
        self.radio_money_plus = RadioButton(self.trans['money_plus'][0],
                                            lambda: print(14), True)
        self.radio_money_down = RadioButton(self.trans['money_down'][0],
                                            lambda: print(15), True)
        radio_group = QButtonGroup()
        radio_group.setExclusive(True)
        radio_group.addButton(self.radio_modify)
        radio_group.addButton(self.radio_money_plus)
        radio_group.addButton(self.radio_money_down)

        # 基础显示组件定义
        self.init_ui()

    def on_search_button_clicked(self):
        try:
            phone_value = int(self.phone_number.text().strip())
        except ValueError:
            QMessageBox.critical(self, self.trans['errors']['error'], self.trans['errors']['no_number'])
            return

    def on_exit_button_clicked(self):
        # 清空文本框和历史记录
        self.phone_number.clear()
        self.name.setText('...')
        self.wechat.setText('...')
        self.card_id.setText('...')
        self.birthday.setText('...')
        self.money_value.clear()
        self.history.clear()

        # 禁用按钮和单选框
        self.button_exit.setDisabled(True)
        self.button_modify.setDisabled(True)
        self.button_money_plus.setDisabled(True)
        self.button_money_down.setDisabled(True)
        self.radio_modify.setDisabled(True)
        self.radio_money_plus.setDisabled(True)
        self.radio_money_down.setDisabled(True)

        # 将焦点移动到self.phone_number
        self.phone_number.setFocus()

    def init_ui(self):
        info_layout = QGridLayout()  # 基本信息显示Grid
        info_layout.setSpacing(0)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.addWidget(Text(self.trans['phone_number']), 0, 0)
        info_layout.addWidget(self.phone_number, 0, 1, 1, 3)
        info_layout.addWidget(Text(self.trans['name']), 1, 0)
        info_layout.addWidget(self.name, 1, 1)
        info_layout.addWidget(Text(self.trans['wechat']), 2, 0)
        info_layout.addWidget(self.wechat, 2, 1)

        info_layout.addWidget(self.button_search, 0, 4)
        info_layout.addWidget(self.button_exit, 0, 5)
        info_layout.addWidget(Text(self.trans['card_id']), 1, 3)
        info_layout.addWidget(self.card_id, 1, 4, 1, 2)
        info_layout.addWidget(Text(self.trans['birthday']), 2, 3)
        info_layout.addWidget(self.birthday, 2, 4, 1, 2)

        info_layout.addWidget(Text(self.trans['money']), 0, 7, 1, 3)
        info_layout.addWidget(self.money_value, 1, 8, 2, 1)
        info_layout.addWidget(Text('CNY'), 2, 9)

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
        operate_layout.addWidget(Text('＋', align=Qt.AlignRight | Qt.AlignVCenter), 3, 0)
        operate_layout.addWidget(self.money_plus_num, 3, 1, 1, 2)
        operate_layout.addWidget(Text('CNY'), 3, 3)
        operate_layout.addWidget(self.button_money_plus, 3, 5)

        operate_layout.addWidget(self.radio_money_down, 5, 0, 1, 3)
        operate_layout.addWidget(self.money_down_category, 6, 1, 1, 2)
        operate_layout.addWidget(self.money_down_note, 6, 3, 1, 2)
        operate_layout.addWidget(Text('－', align=Qt.AlignRight | Qt.AlignVCenter), 7, 0)
        operate_layout.addWidget(self.money_down_num, 7, 1, 1, 2)
        operate_layout.addWidget(Text('CNY'), 7, 3)
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
