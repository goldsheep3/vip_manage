from sys import argv

from PySide6.QtCore import Signal
from peewee import SqliteDatabase
from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QApplication)
import qdarkstyle

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

        login_widget.login_successful.connect(lambda: stacked_widget.setCurrentIndex(1))
        self.login_successful.connect(lambda: stacked_widget.setCurrentIndex(1))

        self.setCentralWidget(stacked_widget)


def main_app(conf, translation):
    app = QApplication(argv)
    window = MainWindow(conf, translation)
    window.show()
    exit(app.exec())
