import argparse

from os.path import join

from lib.read import read_yaml
from manage.app import main_app as without_ui
from ui.app import main_app as with_ui

"""
██╗   ██╗ ██╗ ██████╗           ███╗   ███╗  █████╗  ███╗   ██╗  █████╗   ██████╗  ███████╗
██║   ██║ ██║ ██╔══██╗          ████╗ ████║ ██╔══██╗ ████╗  ██║ ██╔══██╗ ██╔════╝  ██╔════╝
██║   ██║ ██║ ██████╔╝          ██╔████╔██║ ███████║ ██╔██╗ ██║ ███████║ ██║  ███╗ █████╗  
╚██╗ ██╔╝ ██║ ██╔═══╝           ██║╚██╔╝██║ ██╔══██║ ██║╚██╗██║ ██╔══██║ ██║   ██║ ██╔══╝  
 ╚████╔╝  ██║ ██║      ███████╗ ██║ ╚═╝ ██║ ██║  ██║ ██║ ╚████║ ██║  ██║ ╚██████╔╝ ███████╗
  ╚═══╝   ╚═╝ ╚═╝      ╚══════╝ ╚═╝     ╚═╝ ╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚═╝  ╚═╝  ╚═════╝  ╚══════╝
"""


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
