from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QMessageBox, QStackedWidget, QTableView,
                               QHeaderView, QListWidget)

from lib.n_qt import (LineEdit, Text, DoubleSpinBox, SpinBox, ComboBox, PushButton, GridLayout,
                      VerticalLine)
from lib.sql_table import create_tables_model
from manage.action import phone_search, card_id_search, get_history
from ui.operate_tip import NoFullPhoneTip


class OperateWidget(QWidget):
    def __init__(self, i18n, conn, window):
        super().__init__()
        self.conn = conn
        self.window = window
        self.trans = i18n['MOperate']
        # self.i18n = i18n
        # 链接数据库
        self.base_info_model = create_tables_model(self.conn)
        self.user_info: dict = dict()

        self.card_id = LineEdit()
        self.phone = LineEdit()
        self.balance = DoubleSpinBox(no_buttons=True, read_only=True)
        self.name = Text('...')
        self.wechat = Text('...')
        self.birthday = Text('...')
        self.history = QListWidget()

        self.login_stack = QStackedWidget()
        self.login_stack.addWidget(PushButton('登入', self.on_login_button_clicked))
        self.login_stack.addWidget(PushButton('退出', print))

        self.category1 = ComboBox()
        self.category2 = LineEdit()
        self.pay_zhe = SpinBox(10, no_buttons=True)
        self.pay_1 = DoubleSpinBox(no_buttons=True)  # 原金额
        self.pay_2 = DoubleSpinBox(no_buttons=True)  # 立减额
        self.pay_3 = DoubleSpinBox(no_buttons=True)  # 现金额

        self.order_model = QStandardItemModel()
        header = ['时间', '项目', '金额', '优惠', '实额', '余额']
        self.order_model.setHorizontalHeaderLabels(header)
        self.orders = QTableView()
        self.orders.setModel(self.order_model)

        self.button_add_order = PushButton('添加订单', print)
        self.button_settlement = PushButton('订单结算', print)
        self.button_order_settlement = PushButton('添加并结算', print)

        self.button_modify = PushButton('修改信息', print, True)
        self.button_addcny = PushButton('余额储值', print, True)

        self.init_ui()

    def on_login_button_clicked(self):
        phone_value = ''
        try:
            phone_value = self.phone.text().strip()
            if (phone_value == '') and (self.card_id.text().strip() != ''):
                search_answer = card_id_search(int(self.card_id.text().strip()), self.conn)
            else:
                search_answer = phone_search(phone_value, self.conn)
            # 返回数据元组
        except ValueError:
            QMessageBox.critical(self, self.trans['errors']['error'], self.trans['errors']['no_phone'])
            return
        except NameError as ne:
            if ne.args[0] == 32:
                QMessageBox.critical(self, self.trans['errors']['error'], self.trans['errors']['not_found_phone'])
                return
            elif ne.args[0] == 33:
                # 处理是否注册
                reg = NoFullPhoneTip(self.trans)
                reg.exec_()
                if reg.result_Value == 21:
                    search_answer = ()  # 未确认当前位置
                else:
                    return
            else:
                raise
        search_num = len(search_answer)
        if search_num == 1:
            data = search_answer[0]
        elif search_num == 0:
            raise
        else:
            # 4位尾号多结果
            if len(phone_value) == 4:
                raise SystemError('DEBUG!')
                # data = dict()
                # 待完成：多结果，弹窗选择
            else:
                raise

        # 登录后处理
        self.user_info = data
        self.edit_line_edit(
            str(self.user_info.card_id),
            self.user_info.phone_number,
            self.user_info.balance/100,  # 余额存储为非浮点数（分）
            self.user_info.name,
            self.user_info.wechat,
            self.user_info.birthday
        )
        self.card_id.setDisabled(True)
        self.phone.setDisabled(True)
        # 切换为退出按钮
        self.login_stack.setCurrentIndex(1)
        # 激活操作区
        self.button_modify.setEnabled(True)
        self.button_addcny.setEnabled(True)
        # 读取历史操作
        histories = get_history(self.user_info.card_id, self.conn, True)
        for i in histories:
            note = '-' + i['note'] if i['note'] is not None else ''
            self.history.addItem(
                f"{i['date']}\t{i['v_sign']}{i['money_value']}CNY ({i['variation_type']})\n\t {i['category']}{note}")

    def on_exit_button_clicked(self):

        self.user_info = dict()

        # 清空文本框和历史记录
        self.phone.clear()
        self.edit_line_edit('...', '...', 0, '...', '...', '...')
        self.history.clear()
        # 禁用按钮和单选框
        self.button_modify.setDisabled(True)
        self.button_addcny.setDisabled(True)
        # 恢复卡号/手机号输入框
        self.card_id.setEnabled(True)
        self.phone.setEnabled(True)
        # 切换搜索按钮、取消激活编辑按钮、移动焦点
        self.login_stack.setCurrentIndex(0)
        self.phone.setFocus()

    def on_modify_button_clicked(self):
        pass

    def on_settlement_button_clicked(self):
        pass

    def edit_line_edit(self, card_id, phone, balance: int, name='', wechat='', birthday=''):
        self.name.setText(name)
        self.wechat.setText(wechat)
        self.card_id.setText(card_id)
        self.phone.setText(phone)
        self.birthday.setText(birthday)
        self.balance.setValue(balance)

    def init_ui(self):
        """Init UI."""

        # 左侧用户区
        user_info_layout = GridLayout()
        user_info_layout.setAllRowStretch([
            4, 1, 4, 4, 4, 4, 4, 4, 4, 1, 4, 26
        ])
        user_info_layout.setAllColumnStretch([2, 1, 2, 1])

        user_info_layout.addWidget(Text('会员信息'), 0, 0, 1, 4)
        user_info_layout.addWidget(Text('卡号'), 2, 0)
        user_info_layout.addWidget(Text('手机号'), 3, 0)
        user_info_layout.addWidget(Text('余额'), 4, 0)
        user_info_layout.addWidget(Text('CNY'), 4, 3)
        user_info_layout.addWidget(Text('姓名'), 5, 0)
        user_info_layout.addWidget(Text('微信'), 6, 0)
        user_info_layout.addWidget(Text('生日'), 7, 0)
        user_info_layout.addWidget(Text('近期交易'), 10, 0, 1, 4)

        user_info_layout.addWidget(PushButton('修改信息', print, True), 8, 0, 1, 2)
        user_info_layout.addWidget(PushButton('余额储值', print, True), 8, 2, 1, 2)
        user_info_layout.addWidget(self.login_stack, 3, 3)

        user_info_layout.addWidget(self.card_id, 2, 1, 1, 3)
        user_info_layout.addWidget(self.phone, 3, 1, 1, 2)
        user_info_layout.addWidget(self.balance, 4, 1, 1, 2)
        user_info_layout.addWidget(self.name, 5, 1, 1, 3)
        user_info_layout.addWidget(self.wechat, 6, 1, 1, 3)
        user_info_layout.addWidget(self.birthday, 7, 1, 1, 3)

        user_info_layout.addWidget(self.history, 11, 0, 1, 4)

        user_info_layout = GridLayout()
        user_info_layout.setAllRowStretch([
            4, 1, 4, 4, 4, 4, 4, 4, 4, 1, 4, 26
        ])
        user_info_layout.setAllColumnStretch([1, 1, 2, 1])

        user_info_layout.addWidget(Text('会员信息'), 0, 0, 1, 4)
        user_info_layout.addWidget(Text('卡号'), 2, 0)
        user_info_layout.addWidget(Text('手机号'), 3, 0)
        user_info_layout.addWidget(Text('余额'), 4, 0)
        user_info_layout.addWidget(Text('CNY'), 4, 3)
        user_info_layout.addWidget(Text('姓名'), 5, 0)
        user_info_layout.addWidget(Text('微信'), 6, 0)
        user_info_layout.addWidget(Text('生日'), 7, 0)
        user_info_layout.addWidget(Text('近期交易'), 10, 0, 1, 4)

        user_info_layout.addWidget(self.button_modify, 8, 0, 1, 2)
        user_info_layout.addWidget(self.button_addcny, 8, 2, 1, 2)
        user_info_layout.addWidget(self.login_stack, 3, 3)

        user_info_layout.addWidget(self.card_id, 2, 1, 1, 3)
        user_info_layout.addWidget(self.phone, 3, 1, 1, 2)
        user_info_layout.addWidget(self.balance, 4, 1, 1, 2)
        user_info_layout.addWidget(self.name, 5, 1, 1, 3)
        user_info_layout.addWidget(self.wechat, 6, 1, 1, 3)
        user_info_layout.addWidget(self.birthday, 7, 1, 1, 3)

        user_info_layout.addWidget(self.history, 11, 0, 1, 4)

        # 右侧操作区：下方操作
        operate_box = QGroupBox()
        operate_box.setTitle('交易操作')
        operate_box_layout = GridLayout()
        operate_box.setLayout(operate_box_layout)

        operate_box_layout.setAllColumnStretch(6)
        operate_box_layout.addWidget(Text('交易项目'), 0, 0)
        operate_box_layout.addWidget(Text('交易金额'), 1, 0)
        operate_box_layout.addWidget(Text('CNY'), 1, 3)
        operate_box_layout.addWidget(Text('交易优惠'), 2, 0)
        operate_box_layout.addWidget(Text('折后立减'), 2, 2)
        operate_box_layout.addWidget(Text('CNY'), 2, 4)
        operate_box_layout.addWidget(Text('交易实额'), 3, 0)
        operate_box_layout.addWidget(Text('CNY'), 3, 3)

        operate_box_layout.addWidget(self.category1, 0, 1, 1, 2)
        operate_box_layout.addWidget(self.category2, 0, 3, 1, 2)
        operate_box_layout.addWidget(self.pay_1, 1, 1, 1, 2)
        operate_box_layout.addWidget(self.pay_zhe, 2, 1)
        operate_box_layout.addWidget(self.pay_2, 2, 3)
        operate_box_layout.addWidget(self.pay_3, 3, 1, 1, 2)

        operate_box_layout.addWidget(self.button_add_order, 4, 3)
        operate_box_layout.addWidget(self.button_settlement, 4, 4)
        operate_box_layout.addWidget(self.button_order_settlement, 4, 5)

        # 右侧操作区：表格
        order_layout = QVBoxLayout()
        order_layout.addWidget(self.orders)
        order_box = QGroupBox()
        order_box.setTitle('当前订单')
        order_box.setLayout(order_layout)
        header = self.orders.horizontalHeader()
        # noinspection PyUnresolvedReferences
        header.setSectionResizeMode(QHeaderView.Stretch)
        # noinspection PyUnresolvedReferences
        [header.setSectionResizeMode(i, QHeaderView.ResizeToContents) for i in list(range(2, 6)) + [0]]

        # 右侧操作区整体
        operate_layout = QVBoxLayout()
        operate_layout.addWidget(Text('订单信息'), 4)
        operate_layout.addWidget(order_box, 38)
        operate_layout.addWidget(operate_box, 22)

        # 总布局
        base_layout = QHBoxLayout()
        base_layout.addLayout(user_info_layout, 3)
        base_layout.addWidget(VerticalLine(), 1)
        base_layout.addLayout(operate_layout, 7)

        self.setLayout(base_layout)
