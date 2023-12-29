from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QGridLayout, QWidget, QHBoxLayout, QVBoxLayout,
                               QGroupBox, QButtonGroup, QListWidget)

from ui.e_pyside import *


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class OperateWidget(QWidget):
    def __init__(self, i18n):
        super().__init__()

        info_layout = QGridLayout()  # 基本信息显示Grid
        info_layout.setSpacing(0)  # DEBUG
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.addWidget(NText(i18n['operate']['phone_number']), 0, 0)
        phone_input = CLEdit()
        phone_input.setContentsMargins(0, 5, 10, 5)
        info_layout.addWidget(phone_input, 0, 1, 1, 3)
        info_layout.addWidget(NText(i18n['operate']['name']), 1, 0)
        name_show = CLEdit(True, '...')
        info_layout.addWidget(name_show, 1, 1)
        info_layout.addWidget(NText(i18n['operate']['wechat']), 2, 0)
        wechat_show = CLEdit(True, '...')
        info_layout.addWidget(wechat_show, 2, 1)

        info_layout.addWidget(BButton(i18n['operate']['search'], lambda: print(1)), 0, 4)
        info_layout.addWidget(BButton(i18n['operate']['exit'], lambda: print(2)), 0, 5)
        info_layout.addWidget(NText(i18n['operate']['card_id']), 1, 3)
        card_id_show = CLEdit(True, '...')
        info_layout.addWidget(card_id_show, 1, 4, 1, 2)
        info_layout.addWidget(NText(i18n['operate']['birthday']), 2, 3)
        birthday_show = CLEdit(True, '...')
        info_layout.addWidget(birthday_show, 2, 4, 1, 2)

        money_text = NText('...')
        money_text.setAlignment(Qt.AlignCenter)

        info_layout.addWidget(NText(i18n['operate']['money']), 0, 7, 1, 3)
        info_layout.addWidget(money_text, 1, 8, 2, 1)
        info_layout.addWidget(NText('CNY'), 2, 9)

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

        modify_button = RButton()  # 修改信息
        modify_button.setText(i18n['operate']['modify_info'][0])
        modify_button.clicked.connect(lambda: print(12))
        money_plus_button = RButton()  # 储值
        money_plus_button.setText(i18n['operate']['money_plus'][0])
        money_plus_button.clicked.connect(lambda: print(14))
        money_down_button = RButton()  # 消费
        money_down_button.setText(i18n['operate']['money_down'][0])
        money_down_button.clicked.connect(lambda: print(15))
        operate_button_group = QButtonGroup()
        operate_button_group.setExclusive(True)
        operate_button_group.addButton(modify_button)
        operate_button_group.addButton(money_plus_button)
        operate_button_group.addButton(money_down_button)
        operate_layout = QGridLayout()
        operate_layout.addWidget(modify_button, 0, 0, 1, 3)

        operate_layout.addWidget(money_plus_button, 2, 0, 1, 3)
        operate_layout.addWidget(BButton(i18n['operate']['modify_info'][1], lambda: print(21), True), 0, 5)
        operate_layout.addWidget(NText('＋', align=Qt.AlignRight | Qt.AlignVCenter), 3, 0)
        operate_layout.addWidget(DSBox(True), 3, 1, 1, 2)
        operate_layout.addWidget(NText('CNY'), 3, 3)
        operate_layout.addWidget(BButton(i18n['operate']['money_plus'][1], lambda: print(22), True), 3, 5)

        operate_layout.addWidget(money_down_button, 5, 0, 1, 3)
        operate_layout.addWidget(CBox(True), 6, 1, 1, 2)
        operate_layout.addWidget(CLEdit(True), 6, 3, 1, 2)
        operate_layout.addWidget(NText('－', align=Qt.AlignRight | Qt.AlignVCenter), 7, 0)
        operate_layout.addWidget(DSBox(True), 7, 1, 1, 2)
        operate_layout.addWidget(NText('CNY'), 7, 3)

        operate_layout.addWidget(BButton(i18n['operate']['money_down'][1], lambda: print(23), True), 7, 5)

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
        operate_gbox.setTitle(i18n['operate']['operate'])

        history_text = QListWidget()
        # history_text.addItem('2023.01.28 -300.00CNY 消费[服务1-测试]')  # DEBUG
        history_text.setWordWrap(True)
        history_layout = QVBoxLayout()
        history_layout.setSpacing(0)
        history_layout.setContentsMargins(5, 5, 5, 5)
        history_layout.addWidget(history_text)

        history_gbox = QGroupBox()
        history_gbox.setLayout(history_layout)
        history_gbox.setTitle(i18n['operate']['history'])

        down_layout = QHBoxLayout()  # 分隔最近明细和操作区域
        down_layout.setSpacing(15)
        down_layout.setContentsMargins(0, 0, 0, 0)
        down_layout.addWidget(history_gbox, 4)
        down_layout.addWidget(operate_gbox, 7)
        down_widget = QWidget()
        down_widget.setLayout(down_layout)

        gc_layout = QVBoxLayout()  # 分隔操作区上下
        gc_layout.setSpacing(10)
        gc_layout.setContentsMargins(50, 25, 50, 25)
        gc_layout.addWidget(info_widget, 1)
        gc_layout.addWidget(down_widget, 3)

        self.setLayout(gc_layout)
