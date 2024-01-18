from peewee import SqliteDatabase
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QStackedWidget)
import argparse

from os.path import join
from sys import argv, exit
from PySide6.QtWidgets import QApplication

from lib.read import read_yaml
from lib.n_qt import Text
from manage.app import main_app as without_ui
from ui.operate import OperateWidget
from ui.login import LoginWidget


class MainWindow(QMainWindow):
    def __init__(self, config, i18n):
        super().__init__()
        self.setGeometry(550, 250, 800, 600)
        self.setMinimumSize(600, 450)

        self.setWindowTitle(f"{config['organization']} - {i18n['title']}")

        conn = SqliteDatabase('database.db')

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
        bg_layout.addWidget(Text(''), 2)
        bg_layout.addWidget(stacked_widget, 13)
        bg_widget = QWidget()
        bg_widget.setLayout(bg_layout)

        self.setCentralWidget(bg_widget)

        # DEBUG
        stacked_widget.setCurrentIndex(1)


def with_ui(conf, translation):
    app = QApplication(argv)
    window = MainWindow(conf, translation)
    window.show()
    exit(app.exec())


if __name__ == "__main__":
    config = read_yaml('config.yaml')
    i18n = read_yaml(join('i18n', config.get('language', 'zh-CN') + '.yaml'))

    parser = argparse.ArgumentParser()
    parser.add_argument('-no_window', action='store_true', help=i18n['MMain']['no_window'])
    parser.add_argument('-language', type=str, help=i18n['MMain']['language'])
    args = parser.parse_args()

    if args.language:
        i18n = read_yaml(join('i18n', args.language + '.yaml'))
        if not i18n:
            i18n = read_yaml(join('i18n', config.get('language', 'zh-CN') + '.yaml'))
    if args.no_window:
        without_ui(config, i18n)
    else:
        with_ui(config, i18n)
