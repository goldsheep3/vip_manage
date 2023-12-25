from os.path import join

import yaml
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QMainWindow, QGridLayout, QWidget, QHBoxLayout, QVBoxLayout,
                               QGroupBox, QButtonGroup)

from ui.e_pyside import *


def read_yaml(language_file):
    try:
        with open(language_file, 'r', encoding='utf-8') as file:
            # 使用load方法将YAML文件内容转换为Python对象
            data = yaml.load(file, Loader=yaml.FullLoader)
            return data
    except FileNotFoundError:
        print(f"File not found: {language_file}")
        return None
    except yaml.YAMLError as e:
        print(f"Error reading YAML file {language_file}: {e}")
        return None


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(550, 250, 600, 450)
        self.setMinimumSize(600, 450)
        config = read_yaml('config.yaml')
        i18n = read_yaml(join('i18n', config.get('language', 'zh-CN') + '.yaml'))

        self.setWindowTitle(i18n['operate']['title'])

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

        info_layout.addWidget(NText(i18n['operate']['money']), 1, 7, 1, 3)
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
        operate_layout.addWidget(BButton(i18n['operate']['modify_info'][1], lambda: print(21)), 0, 5)
        operate_layout.addWidget(CLEdit(True), 3, 1, 1, 2)
        operate_layout.addWidget(NText('CNY'), 3, 3)
        operate_layout.addWidget(BButton(i18n['operate']['money_plus'][1], lambda: print(22)), 3, 5)

        operate_layout.addWidget(money_down_button, 5, 0, 1, 3)
        operate_layout.addWidget(CBox(True), 6, 1, 1, 2)
        operate_layout.addWidget(CLEdit(True), 6, 3, 1, 2)
        operate_layout.addWidget(CLEdit(True), 7, 1, 1, 2)
        operate_layout.addWidget(NText('CNY'), 7, 3)

        operate_layout.addWidget(BButton(i18n['operate']['money_down'][1], lambda: print(23)), 7, 5)

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
        operate_gbox.setTitle(i18n['operate']['gbox'])

        down_layout = QHBoxLayout()  # 分隔最近明细和操作区域
        down_layout.setSpacing(15)
        down_layout.setContentsMargins(0, 0, 0, 0)
        down_layout.addWidget(Color('blue'), 1)
        down_layout.addWidget(operate_gbox, 2)
        down_widget = QWidget()
        down_widget.setLayout(down_layout)

        gc_layout = QVBoxLayout()  # 分隔操作区上下
        gc_layout.setSpacing(10)
        gc_layout.setContentsMargins(50, 25, 50, 25)
        gc_layout.addWidget(info_widget, 1)
        gc_layout.addWidget(down_widget, 3)
        gc_widget = QWidget()
        gc_widget.setLayout(gc_layout)

        bg_layout = QVBoxLayout()  # 分隔上标题和下操作
        bg_layout.setSpacing(0)
        bg_layout.setContentsMargins(0, 0, 0, 0)
        bg_layout.addWidget(Color('red'), 2)
        bg_layout.addWidget(gc_widget, 13)
        bg_widget = QWidget()
        bg_widget.setLayout(bg_layout)

        self.setCentralWidget(bg_widget)
