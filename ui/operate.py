from os.path import join

from PySide6.QtCore import (Qt, QRect)
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QHBoxLayout, QVBoxLayout,
                               QLineEdit, QFrame, QSizePolicy)

import yaml


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


class NText(QLabel):
    def __init__(self, text):
        super().__init__(text)


class CLEdit(QLineEdit):
    def __init__(self, read_only=False, text=''):
        super().__init__()
        self.setContentsMargins(0, 5, 0, 5)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setText(text)
        if read_only:
            self.setReadOnly(True)


class BButton(QPushButton):
    def __init__(self, text, function, read_only=False):
        super().__init__()
        self.setText(text)
        self.clicked.connect(function)
        self.setContentsMargins(5, 5, 5, 5)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if read_only:
            self.setEnabled(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 800, 600)
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
        name_show = CLEdit(True, '- -')
        info_layout.addWidget(name_show, 1, 1)
        info_layout.addWidget(NText(i18n['operate']['wechat']), 2, 0)
        wechat_show = CLEdit(True, '- -')
        info_layout.addWidget(wechat_show, 2, 1)

        # info_layout.addWidget(Color('cyan'), 0, 3)
        info_layout.addWidget(BButton(i18n['operate']['search'], lambda: print(1)), 0, 4)
        info_layout.addWidget(BButton(i18n['operate']['exit'], lambda: print(2)), 0, 5)
        info_layout.addWidget(NText(i18n['operate']['card_id']), 1, 3)
        card_id_show = CLEdit(True, '- -')
        info_layout.addWidget(card_id_show, 1, 4, 1, 2)
        info_layout.addWidget(NText(i18n['operate']['birthday']), 2, 3)
        birthday_show = CLEdit(True, '- -')
        info_layout.addWidget(birthday_show, 2, 4, 1, 2)

        money_text = NText('- -')
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

        operate_layout = QHBoxLayout()
        operate_layout.setSpacing(5)
        operate_layout.setContentsMargins(0, 0, 0, 0)
        operate_layout.addWidget(Color('blue'), 1)
        operate_layout.addWidget(Color('blue'), 2)
        operate_widget = QWidget()
        operate_widget.setLayout(operate_layout)

        gc_layout = QVBoxLayout()  # 分隔操作区上下
        gc_layout.setSpacing(10)
        gc_layout.setContentsMargins(15, 15, 15, 15)
        gc_layout.addWidget(info_widget, 1)
        gc_layout.addWidget(operate_widget, 3)
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
