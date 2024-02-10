from sys import argv

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
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

        # 创建菜单栏
        menubar = self.menuBar()
        self.menus = []

        menu_edit = menubar.addMenu('编辑')
        action_settle = QAction('切换到 前台结算', self)
        action_settle.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        menu_edit.addAction(action_settle)
        action_manage = QAction('切换到 后台管理', self)
        action_manage.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        menu_edit.addAction(action_manage)
        action_lock = QAction('锁定管理账号', self)
        action_lock.triggered.connect(self.login_out)
        menu_edit.addAction(action_lock)
        menu_edit.setDisabled(True)
        self.menus.append(menu_edit)

        menu_about = menubar.addMenu('关于')
        menu_about.addAction(QAction('当前版本：DEV.', self))

        # 主操作窗口
        operate_widget = OperateWidget(i18n, conn, self)
        login_widget = LoginWidget(i18n, conn, self)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget.addWidget(login_widget)
        self.stacked_widget.addWidget(operate_widget)
        self.stacked_widget.addWidget(QMainWindow())

        # 登录信号处理
        login_widget.login_successful.connect(self.login_in)
        self.login_successful.connect(self.login_in)

        self.setCentralWidget(self.stacked_widget)

    def login_in(self):
        self.stacked_widget.setCurrentIndex(1)
        [m.setEnabled(True) for m in self.menus]

    def login_out(self):
        self.stacked_widget.setCurrentIndex(0)
        [m.setDisabled(True) for m in self.menus]


def main_app(conf, translation):
    app = QApplication(argv)
    window = MainWindow(conf, translation)
    window.show()
    exit(app.exec())
