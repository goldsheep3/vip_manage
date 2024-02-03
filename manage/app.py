from os.path import join

from peewee import SqliteDatabase

from lib.read import read_yaml
from manage.action import key_sugar, check_md5_key, phone_search

sql_conn = SqliteDatabase('database.db')


def key_inputer(front: str = '') -> str:
    if front:
        front += ' '
    body = input(f'{front}>> ')
    return body


def main_app(_config, i18n):
    login_in(i18n['MLogin'])
    while True:
        print()
        print(i18n['MCommand']['tip1'], i18n['MCommand']['tip2'], sep='\n')
        command_text = key_inputer('Admin').strip()
        command = command_text.split()
        if command[0] == 'login':
            try:
                keys = phone_search(command[1], sql_conn)
            except ValueError:
                print(i18n['MOperate']['errors']['no_phone'])
                continue
            except NameError:
                pass  # 新用户或临时结算或continue
            else:
                if len(keys) == 1:
                    if keys[0] == 0:
                        pass  # 临时结算
                elif len(keys) > 1:
                    pass  # 选择手机号

        elif command[0] == 'exit':
            continue
        elif command[0] == 'leave':
            raise SystemExit(3)
        elif command[0] == 'config':
            continue
        elif command[0] == 'help':
            print()
            for i in i18n['MCommand']['help']:
                print(i)
            continue
        else:
            print(i18n['MCommand']['no_exist'])
            continue


def login_in(trans) -> int:
    """console登录代码"""
    while True:
        # 显示登录选项和用户提示
        print(trans['press_key'], trans['without_ui']['forget_pwd'], trans['without_ui']['exit_tip'], sep='\n')
        # 获取用户输入的密码
        pwd = str(key_inputer()).strip()
        # 检查用户是否想要找回密码
        if pwd == '?' or pwd == '？':
            print(trans['forget']['tip1'], trans['forget']['tip2'], sep='\n')
            key = str(key_inputer()).strip()
            try:
                # 使用MD5密钥验证密码以进行密码找回
                check_md5_key(sql_conn, key, key_sugar.get('verify'))
                print(trans['without_ui']['found'])
                break
            except NameError as e:
                if e.args[0] == 32:
                    print(trans['forget']['verify']['wrong2'] + '\n')
                    continue
                raise
        # 检查用户是否想要退出程序
        elif pwd == 'exit':
            raise SystemExit(3)
        else:
            try:
                # 使用MD5密钥验证登录密码
                check_md5_key(sql_conn, pwd, key_sugar.get('login'))
                break
            except NameError as e:
                if e.args[0] == 32:
                    print(trans['wrong']['title'], trans['wrong']['tip'])
                    continue
                raise
    # 返回0表示成功登录
    return 0


if __name__ == "__main__":
    config = read_yaml('config.yaml')
    language_dict = read_yaml(join('i18n', config.get('language', 'zh-CN') + '.yaml'))
    main_app(config, language_dict)
