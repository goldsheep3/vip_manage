from os.path import join

import yaml
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QStackedWidget)

from ui.operate import OperateWidget


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
        self.setGeometry(550, 250, 800, 600)
        self.setMinimumSize(600, 450)
        config = read_yaml('config.yaml')
        i18n = read_yaml(join('i18n', config.get('language', 'zh-CN') + '.yaml'))

        self.setWindowTitle(f"{config['organization']} - {i18n['title']}")

        operate_widget = OperateWidget(i18n)

        stacked_widget = QStackedWidget()
        stacked_widget.setContentsMargins(0, 0, 0, 0)
        stacked_widget.addWidget(operate_widget)

        bg_layout = QVBoxLayout()  # 分隔上标题和下操作
        bg_layout.setSpacing(0)
        bg_layout.setContentsMargins(0, 0, 0, 0)
        bg_layout.addWidget(Color('red'), 2)
        bg_layout.addWidget(stacked_widget, 13)
        bg_widget = QWidget()
        bg_widget.setLayout(bg_layout)

        self.setCentralWidget(bg_widget)
