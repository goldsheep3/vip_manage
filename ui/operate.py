from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QGridLayout, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QButtonGroup, QListWidget,
                               QMessageBox, QStackedWidget, QToolBox)

from lib.n_qt import LineEdit, Text, DoubleSpinBox, ComboBox, PushButton, RadioButton
from lib.sql_table import create_tables_model
from manage.action import search


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
        self.order = QListWidget()
        self.order.setWordWrap(True)

        self.trade_category = ComboBox(True)
        self.trade_note = LineEdit(True)
        self.amount = DoubleSpinBox(True, True)
        self.discount = DoubleSpinBox(True, True)
        self.paid_amount = DoubleSpinBox(True, True)

        self.button_search = PushButton(self.trans['search'], self.on_search_button_clicked)
        self.button_exit = PushButton(self.trans['exit'], self.on_exit_button_clicked)
        self.button_modify = PushButton(self.trans['modify'], self.on_modify_button_clicked, True)
        self.button_settlement = PushButton(self.trans['settlement'], self.on_settlement_button_clicked, True)

        self.radio_money_plus = RadioButton(self.trans['money_plus'],
                                            lambda: print(14), True)
        self.radio_money_down = RadioButton(self.trans['money_down'],
                                            lambda: print(15), True)

        self.phone_number.returnPressed.connect(self.button_search.clicked)

        self.login_sys = QStackedWidget()
        self.login_sys.setContentsMargins(0, 0, 0, 0)
        self.login_sys.addWidget(self.button_search)
        self.login_sys.addWidget(self.button_exit)

        self.left_tbox = QToolBox()

        # 基础显示组件定义
        self.init_ui()

    def on_search_button_clicked(self):
        try:
            phone_value = self.phone_number.text().strip()
            search_answer = search(phone_value, self.conn)
            print(search_answer)
        except ValueError:
            QMessageBox.critical(self, self.trans['errors']['error'], self.trans['errors']['no_phone'])
            return
        self.phone_number.setDisabled(True)  # 登录后不可更改
        # 切换为退出按钮、激活编辑按钮
        self.login_sys.setCurrentIndex(1)
        self.button_modify.setEnabled(True)

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
        self.button_modify.setDisabled(True)
        self.radio_money_plus.setDisabled(True)
        self.radio_money_down.setDisabled(True)

        # 恢复手机号码输入框
        self.phone_number.setEnabled(True)
        # 切换搜索按钮、取消激活编辑按钮、移动焦点
        self.login_sys.setCurrentIndex(0)
        self.phone_number.setFocus()

    def on_modify_button_clicked(self):
        pass

    def on_settlement_button_clicked(self):
        pass

    def init_ui(self):
        radio_group = QButtonGroup()
        radio_group.setExclusive(True)
        radio_group.addButton(self.radio_money_plus)
        radio_group.addButton(self.radio_money_down)

        info_layout = QGridLayout()  # 基本信息显示Grid
        info_layout.setSpacing(0)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.addWidget(Text(self.trans['phone_number']), 0, 0)
        info_layout.addWidget(self.phone_number, 0, 1, 1, 3)
        info_layout.addWidget(Text(self.trans['name']), 1, 0)
        info_layout.addWidget(self.name, 1, 1)
        info_layout.addWidget(Text(self.trans['wechat']), 2, 0)
        info_layout.addWidget(self.wechat, 2, 1)

        info_layout.addWidget(self.login_sys, 0, 4)
        info_layout.addWidget(self.button_modify, 0, 5)
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

        operate_layout.addWidget(Text(self.trans['now_operate']), 0, 0)
        operate_layout.addWidget(self.radio_money_plus, 0, 1, 1, 1)
        operate_layout.addWidget(self.radio_money_down, 0, 2, 1, 2)

        operate_layout.addWidget(Text(self.trans['category']), 1, 0)
        operate_layout.addWidget(self.trade_category, 1, 1)
        operate_layout.addWidget(self.trade_note, 1, 2, 1, 2)
        operate_layout.addWidget(Text(self.trans['pay1']), 2, 0)
        operate_layout.addWidget(self.amount, 2, 1)
        operate_layout.addWidget(Text('CNY'), 2, 2)
        operate_layout.addWidget(Text(self.trans['pay2']), 3, 0)
        operate_layout.addWidget(self.discount, 3, 1)
        operate_layout.addWidget(Text('CNY'), 3, 2)
        operate_layout.addWidget(Text('3,3'), 3, 3, 1, 2)
        operate_layout.addWidget(Text('3,4'), 3, 5)
        operate_layout.addWidget(Text('3,5'), 3, 6)
        operate_layout.addWidget(Text(self.trans['pay3']), 4, 0)
        operate_layout.addWidget(self.paid_amount, 4, 1)
        operate_layout.addWidget(Text('CNY'), 4, 2)
        operate_layout.addWidget(Text('6,2'), 6, 2, 1, 3)
        operate_layout.addWidget(Text('6,5'), 6, 5, 1, 2)

        operate_layout.setColumnStretch(0, 2)
        operate_layout.setColumnStretch(1, 3)
        operate_layout.setColumnStretch(2, 2)
        operate_layout.setColumnStretch(3, 1)
        operate_layout.setColumnStretch(4, 1)
        operate_layout.setColumnStretch(5, 2)
        operate_layout.setColumnStretch(6, 2)
        operate_layout.setRowStretch(0, 1)
        operate_layout.setRowStretch(1, 1)
        operate_layout.setRowStretch(2, 1)
        operate_layout.setRowStretch(3, 1)
        operate_layout.setRowStretch(4, 1)
        operate_layout.setRowStretch(5, 1)
        operate_layout.setRowStretch(6, 1)
        operate_layout.setSpacing(5)
        operate_layout.setContentsMargins(25, 15, 25, 15)

        operate_gbox = QGroupBox()
        operate_gbox.setLayout(operate_layout)
        operate_gbox.setTitle(self.trans['operate'])
        # operate_gbox.setStyleSheet('QWidget {border: 2px solid red;}')

        order_layout = QVBoxLayout()
        order_layout.setSpacing(5)
        order_layout.setContentsMargins(0, 0, 0, 0)
        order_layout.addWidget(self.order, 8)
        order_layout.addWidget(self.button_settlement, 1)
        order_widget = QWidget()
        order_widget.setLayout(order_layout)

        self.left_tbox.addItem(order_widget, self.trans['order'])
        self.left_tbox.addItem(self.history, self.trans['history'])
        self.left_tbox.setCurrentIndex(1)

        down_layout = QHBoxLayout()  # 分隔最近明细和操作区域
        down_layout.setSpacing(15)
        down_layout.setContentsMargins(0, 0, 0, 0)
        down_layout.addWidget(self.left_tbox, 4)
        down_layout.addWidget(operate_gbox, 7)
        down_widget = QWidget()
        down_widget.setLayout(down_layout)

        base_layout = QVBoxLayout()  # 分隔操作区上下
        base_layout.setSpacing(10)
        base_layout.setContentsMargins(50, 25, 50, 25)
        base_layout.addWidget(info_widget, 1)
        base_layout.addWidget(down_widget, 3)

        self.setLayout(base_layout)
