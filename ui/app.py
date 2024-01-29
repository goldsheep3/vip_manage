from PySide6.QtCore import Signal
from peewee import SqliteDatabase
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QStackedWidget)
import qdarkstyle

from lib.n_qt import Text
from ui.login import LoginWidget
from ui.operate import OperateWidget


class MainWindow(QMainWindow):
    login_successful = Signal()

    def __init__(self, config, i18n):
        super().__init__()
        self.setGeometry(550, 250, 800, 600)
        self.setMinimumSize(600, 450)

        self.setWindowTitle(f"{config['organization']} - {i18n['title']}")
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))

        conn = SqliteDatabase('database.db')

        operate_widget = OperateWidget(i18n, conn, self)
        login_widget = LoginWidget(i18n, conn, self)

        stacked_widget = QStackedWidget()
        stacked_widget.setContentsMargins(0, 0, 0, 0)

        stacked_widget.addWidget(login_widget)
        stacked_widget.addWidget(operate_widget)

        bg_layout = QVBoxLayout()  # 分隔上标题和下操作
        bg_layout.setSpacing(0)
        bg_layout.setContentsMargins(0, 0, 0, 0)
        bg_layout.addWidget(Text(''), 1)
        bg_layout.addWidget(stacked_widget, 10)
        bg_widget = QWidget()
        bg_widget.setLayout(bg_layout)

        login_widget.login_successful.connect(lambda: stacked_widget.setCurrentIndex(1))
        self.login_successful.connect(lambda: stacked_widget.setCurrentIndex(1))

        self.setCentralWidget(bg_widget)
