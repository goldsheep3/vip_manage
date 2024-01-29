from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QDialog)

from lib.n_qt import LineEdit, Text, DoubleSpinBox, SpinBox, ComboBox, PushButton, RadioButton, GridLayout


class PayGridLayout(GridLayout):
    def __init__(self,
                 trans: dict,
                 trade_category: ComboBox,
                 trade_note: LineEdit,
                 amount: DoubleSpinBox,
                 discount1: SpinBox,
                 discount2: DoubleSpinBox,
                 paid_amount: DoubleSpinBox,
                 right_button: PushButton,
                 left_button: PushButton = None,
                 ):
        super().__init__()
        self.addWidget(Text(trans['category']), 0, 0)
        self.addWidget(trade_category, 0, 1)
        self.addWidget(trade_note, 0, 2, 1, 3)
        self.addWidget(Text(trans['pay1']), 1, 0)
        self.addWidget(amount, 1, 1)
        self.addWidget(Text('CNY'), 1, 2)
        self.addWidget(Text(trans['pay2']), 2, 0)
        self.addWidget(discount1, 2, 1)
        self.addWidget(Text(trans['zhe']), 2, 2)
        self.addWidget(Text(trans['pay3']), 3, 0)
        self.addWidget(discount2, 3, 1)
        self.addWidget(Text('CNY'), 3, 2)
        self.addWidget(Text(trans['pay4']), 4, 0)
        self.addWidget(paid_amount, 4, 1)
        self.addWidget(Text('CNY'), 4, 2)
        self.addWidget(right_button, 5, 5, 1, 2)
        if left_button:
            self.addWidget(left_button, 5, 2, 1, 3)


class RegisterWidget(QDialog):
    def __init__(self, trans):
        super().__init__()
        self.setWindowTitle(trans['reg']['reg'])
        self.setFixedSize(300, 150)
        self.trans = trans
        self.not_extra_area = True

        layout = GridLayout()

        layout.addWidget(Text('* ' + trans['phone_number']), 0, 0)
        layout.addWidget(Text(trans['name']), 1, 0)
        layout.addWidget(Text(trans['wechat']), 2, 0)
        layout.addWidget(Text(trans['birthday']), 3, 0)
        layout.addWidget(Text('* ' + trans['money_plus']), 4, 0)

        self.phone_number = LineEdit()
        self.name = LineEdit()
        self.wechat = LineEdit()
        self.birthday = LineEdit()
        self.edited = DoubleSpinBox(True, True)
        self.trade_category = ComboBox(True)
        self.trade_note = LineEdit(True)
        self.amount = DoubleSpinBox(0, True, True)
        self.discount1 = SpinBox(10, True, True)
        self.discount2 = DoubleSpinBox(0, True, True)
        self.paid_amount = DoubleSpinBox(0, True, True)

        self.money_plus = RadioButton(trans['reg']['mp'], self.plus_clicked)
        self.money_edit = RadioButton(trans['reg']['me'], self.edit_clicked)

        layout.addWidget(self.phone_number, 0, 1)
        layout.addWidget(self.name, 1, 1)
        layout.addWidget(self.wechat, 2, 1)
        layout.addWidget(self.birthday, 3, 1)
        layout.addWidget(self.money_plus, 4, 1)
        layout.addWidget(self.money_edit, 4, 2)
        layout.addWidget(self.edited, 5, 1)

        button_layout = GridLayout()
        button_layout.addWidget(Text(''), 1, 0)
        button_layout.setAllColumnStretch(3)
        reg_layout = QVBoxLayout()
        reg_layout.addLayout(layout)
        reg_layout.addLayout(button_layout)
        self.bg_layout = QHBoxLayout(self)
        self.bg_layout.setSpacing(10)
        self.bg_layout.setContentsMargins(0, 0, 0, 0)
        self.bg_layout.addLayout(reg_layout, 2)

    def plus_clicked(self):
        if self.not_extra_area:
            self.build_area()
        [i.setDisabled(True) for i in [
            self.trade_category,
            self.trade_note,
            self.amount,
            self.discount1,
            self.discount2,
            self.paid_amount
        ]]
        self.edited.setEnabled(True)

    def edit_clicked(self):
        [i.setEnabled(True) for i in [
            self.trade_category,
            self.trade_note,
            self.amount,
            self.discount1,
            self.discount2,
            self.paid_amount
        ]]
        self.edited.setDisabled(True)

    def build_area(self):
        self.not_extra_area = False
        pay_layout = PayGridLayout(self.trans,
                                   self.trade_category,
                                   self.trade_note,
                                   self.amount,
                                   self.discount1,
                                   self.discount2,
                                   self.paid_amount,
                                   PushButton('', print))
        self.bg_layout.addLayout(pay_layout)
        self.setFixedSize(450, 150)


class NoFullPhoneTip(QDialog):
    def __init__(self, trans):
        super().__init__()
        self.setWindowTitle(trans['errors']['error'])
        self.setFixedSize(300, 150)
        self.result_Value = 33

        button_layout = QHBoxLayout()
        button_layout.addWidget(PushButton(trans['reg']['reg'], lambda: self.exit(35)))
        button_layout.addWidget(PushButton(trans['reg']['no_reg'], lambda: self.exit(34)))
        button_layout.addWidget(PushButton(trans['reg']['close'], self.reject))

        layout = QVBoxLayout(self)
        layout.addWidget(Text(trans['errors']['not_found_phone'] + '\n' + trans['errors']['nf_11']), 2)
        layout.addLayout(button_layout, 1)

    def exit(self, value):
        self.result_Value = value
        self.accept()
