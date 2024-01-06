from hashlib import md5
from os.path import join
from re import compile as comp

from peewee import SqliteDatabase, fn

from lib.read import read_yaml
from lib.sql_table import create_tables_model

key_sugar = {
    'login': 160523498730,
    'verify': 202838234617
}
sql_conn = SqliteDatabase('database.db')


def key_inputer(front: str = '') -> str:
    if front:
        front += ' '
    body = input(f'{front}>> ')
    return body


def main_app(_config, i18n):
    login_in(i18n['MLogin'])


def search(phone: int, conn: SqliteDatabase) -> int:
    phone_number_pattern = comp(r'^1[3456789]\d{9}$')
    BaseInfo, History = create_tables_model(conn)
    if 1000 <= phone <= 9999:
        matching_items = BaseInfo.select().where(fn.RIGHT(BaseInfo.phone_number, 4) == phone)
        if len(matching_items) == 0:
            print('无匹配')
            return 32
        elif len(matching_items) == 1:
            print('匹配1')
        elif len(matching_items) > 1:
            print('需要选择')
    elif phone_number_pattern.match(str(phone)):
        matching_items = BaseInfo.select().where(BaseInfo.phone_number == phone)
        if len(matching_items) == 0:
            print('无匹配')
            return 33
        elif len(matching_items) == 1:
            print('匹配1')
    elif phone == 0:
        print('临时')
    raise ValueError


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


def check_md5_key(conn: SqliteDatabase,
                  key_in: str,
                  key: int) -> int:
    """MD5校验代码"""
    Admin = create_tables_model(conn)[2]

    try:
        key_md5 = md5()
        key_md5.update(key_in.encode('utf-8'))
        keyhash = key_md5.hexdigest()
        admin_record = Admin.select().where(Admin.password_hash == keyhash).get()
        sugar = admin_record.sugar
    except Admin.DoesNotExist:
        raise ValueError(32)

    if sugar == key:
        return 0
    else:
        raise ValueError(42)


if __name__ == "__main__":
    config = read_yaml('config.yaml')
    language_dict = read_yaml(join('i18n', config.get('language', 'zh-CN') + '.yaml'))
    main_app(config, language_dict)
