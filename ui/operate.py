from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QButtonGroup, QListWidget,
                               QMessageBox, QStackedWidget, QToolBox)

from lib.n_qt import LineEdit, Text, DoubleSpinBox, SpinBox, ComboBox, PushButton, RadioButton, GridLayout
from lib.sql_table import create_tables_model
from manage.action import search
from ui.operate_tip import NoFullPhoneTip, PayGridLayout


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
        self.amount = DoubleSpinBox(0, True, True)
        self.discount1 = SpinBox(10, True, True)
        self.discount2 = DoubleSpinBox(0, True, True)
        self.paid_amount = DoubleSpinBox(0, True, True)

        self.button_search = PushButton(self.trans['search'], self.on_search_button_clicked)
        self.button_exit = PushButton(self.trans['exit'], self.on_exit_button_clicked)
        self.button_modify = PushButton(self.trans['modify'], self.on_modify_button_clicked, True)
        self.button_settlement = PushButton(self.trans['settlement'], self.on_settlement_button_clicked, True)

        self.radio_money_down = RadioButton(self.trans['money_down'],
                                            lambda: print(15), True)
        self.radio_money_plus = RadioButton(self.trans['money_plus'],
                                            lambda: print(14), True)

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
            try:
                phone_value = self.phone_number.text().strip()
                search_answer = search(phone_value, self.conn)
                # 返回整个数据
            except ValueError:
                QMessageBox.critical(self, self.trans['errors']['error'], self.trans['errors']['no_phone'])
                return
            except NameError as ne:
                if ne.args[0] == 32:
                    QMessageBox.critical(self, self.trans['errors']['error'], self.trans['errors']['not_found_phone'])
                    return
                elif ne.args[0] == 33:
                    # 处理是否注册
                    tip = NoFullPhoneTip(self.trans)
                    tip.exec_()
                    reg = tip.result_Value
                    if reg == 35:
                        # 注册流程
                        raise SystemError('DEBUG!')
                        search_answer = ()
                    elif reg == 34:
                        raise NameError(34)  # 临时结算
                    else:
                        return
                else:
                    raise
        except NameError as ne:
            if ne.args[0] == 34:
                # 临时结算
                raise SystemError('DEBUG!')
                return
            else:
                raise
        search_num = len(search_answer)
        if search_num == 1:
            data = search_answer[0]
            self.edit_line_edit(
                str(data.card_id), '{:.2f}'.format(data.balance / 100),
                data.name, data.wechat, data.birthday)
        else:
            pass
        self.phone_number.setDisabled(True)  # 登录后不可更改
        # 切换为退出按钮、激活编辑按钮
        self.login_sys.setCurrentIndex(1)
        self.button_modify.setEnabled(True)
        # 激活操作区
        self.radio_money_plus.setEnabled(True)
        self.radio_money_down.setEnabled(True)
        self.money_plus_area(True)

    def money_plus_area(self, state):
        pass

    def on_exit_button_clicked(self):
        # 清空文本框和历史记录
        self.phone_number.clear()
        self.edit_line_edit('...', '...', '...', '...', '...')
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

    def edit_line_edit(self, card_id, balance, name='', wechat='', birthday=''):
        self.name.setText(name)
        self.wechat.setText(wechat)
        self.card_id.setText(card_id)
        self.birthday.setText(birthday)
        self.money_value.setText(balance)
        # self.history.addItem(f'{data} {variation}{money_value}CNY {variation_type}[{category}{-note}]')
        # .addItem('2023.01.28 -300.00CNY 消费[服务1-测试]')  <- Sample

    def init_ui(self):
        radio_group = QButtonGroup()
        radio_group.setExclusive(True)
        radio_group.addButton(self.radio_money_plus)
        radio_group.addButton(self.radio_money_down)

        info_layout = GridLayout()  # 基本信息显示Grid
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

        info_layout.setAllColumnStretch([6, 12, 1, 6, 6, 6, 1, 3, 9, 3])
        info_layout.setAllRowStretch(3)

        choose_layout = QHBoxLayout()
        choose_layout.addWidget(Text(self.trans['now_operate']), 1)
        choose_layout.addWidget(self.radio_money_down, 3)
        choose_layout.addWidget(self.radio_money_plus, 3)
        choose_layout.addWidget(Text(''), 1)
        pay_layout = PayGridLayout(self.trans,
                                   self.trade_category,
                                   self.trade_note,
                                   self.amount,
                                   self.discount1,
                                   self.discount2,
                                   self.paid_amount,
                                   PushButton('', print))
        pay_layout.setAllColumnStretch([2, 3, 2, 1, 1, 2, 2])
        pay_layout.setAllRowStretch(7)

        operate_layout = QVBoxLayout()
        operate_layout.addLayout(choose_layout, 1)
        operate_layout.addLayout(pay_layout, 7)
        operate_layout.setSpacing(5)
        operate_layout.setContentsMargins(15, 5, 5, 0)

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

        base_layout = QVBoxLayout()  # 分隔操作区上下
        base_layout.setSpacing(10)
        base_layout.setContentsMargins(50, 25, 50, 25)
        base_layout.addLayout(info_layout, 1)
        base_layout.addLayout(down_layout, 3)

        self.setLayout(base_layout)
