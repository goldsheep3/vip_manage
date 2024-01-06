from os.path import join

from peewee import SqliteDatabase

from lib.read import read_yaml
from manage.action import check_md5_key, key_sugar

sql_conn = SqliteDatabase('database.db')


def key_inputer(front: str = '') -> str:
    if front:
        front += ' '
    body = input(f'{front}>> ')
    return body


def main_app(_config, i18n):
    login_in(i18n['MLogin'])


def login_in(trans) -> int:
    """console登录代码"""
    while True:
        print(trans['press_key'] + '\n' + trans['without_ui']['forget_pwd'] + '\n' + trans['without_ui']['exit_tip'])
        pwd = str(key_inputer()).strip()
        if pwd == '?' or pwd == '？':
            print(trans['forget']['tip1'] + '\n' + trans['forget']['tip2'])
            key = str(key_inputer()).strip()
            try:
                check_md5_key(sql_conn, key, key_sugar.get('verify'))
                print(trans['without_ui']['found'])
                break
            except ValueError:
                print(trans['forget']['verify']['wrong2'] + '\n')
                continue
        elif pwd == 'exit':
            raise SystemExit(3)
        else:
            try:
                check_md5_key(sql_conn, pwd, key_sugar.get('login'))
                break
            except ValueError:
                print(trans['wrong']['title'], trans['wrong']['tip'])
                continue
    return 0


if __name__ == "__main__":
    config = read_yaml('config.yaml')
    language_dict = read_yaml(join('i18n', config.get('language', 'zh-CN') + '.yaml'))
    main_app(config, language_dict)
