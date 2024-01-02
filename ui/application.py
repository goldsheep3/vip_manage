from os.path import join

import peewee
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QStackedWidget)

from ui.operate import OperateWidget
from ui.login import LoginWidget
from lib.read import read_yaml


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
        self.setGeometry(550, 250, 800, 600)
        self.setMinimumSize(600, 450)
        config = read_yaml('config.yaml')
        i18n = read_yaml(join('i18n', config.get('language', 'zh-CN') + '.yaml'))

        self.setWindowTitle(f"{config['organization']} - {i18n['title']}")

        conn = peewee.SqliteDatabase('database.db')

        operate_widget = OperateWidget(i18n, conn, self)
        login_widget = LoginWidget(i18n, conn, self)

        stacked_widget = QStackedWidget()
        stacked_widget.setContentsMargins(0, 0, 0, 0)

        stacked_widget.addWidget(login_widget)
        stacked_widget.addWidget(operate_widget)
        login_widget.login_successful.connect(lambda: stacked_widget.setCurrentIndex(1))

        bg_layout = QVBoxLayout()  # 分隔上标题和下操作
        bg_layout.setSpacing(0)
        bg_layout.setContentsMargins(0, 0, 0, 0)
        bg_layout.addWidget(Color('red'), 2)
        bg_layout.addWidget(stacked_widget, 13)
        bg_widget = QWidget()
        bg_widget.setLayout(bg_layout)

        self.setCentralWidget(bg_widget)
