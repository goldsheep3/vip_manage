from hashlib import md5
from os.path import join

from peewee import SqliteDatabase

from lib.errors import WrongKeyError
from lib.read import read_yaml
from lib.sql_table import create_tables_model

key_sugar = {
    'login': 160523498730,
    'verify': 202838234617
}
conn = SqliteDatabase('database.db')


def main_app(_config, i18n):
    login_in(i18n['MLogin'])


def login_in(trans):
    """console登录代码"""
    while True:
        pwd = str(key_inputer(trans['press_key'] + '\n' + trans['without_ui']['forget_pwd'])).strip()
        if pwd == '?' or pwd == '？':
            key = str(key_inputer(trans['forget']['tip1'] + '\n' + trans['forget']['tip2'])).strip()
            try:
                check_md5_key(conn, key, key_sugar.get('verify'))
                print(trans['without_ui']['found'])
                break
            except WrongKeyError:
                print(trans['forget']['verify']['wrong2'] + '\n')
                continue
        else:
            try:
                check_md5_key(conn, pwd, key_sugar.get('login'))
                break
            except WrongKeyError:
                print(trans['wrong']['title'], trans['wrong']['tip'])
                continue


def check_md5_key(sql_conn: SqliteDatabase,
                  key_in: str,
                  key: int) -> int:
    """MD5校验代码"""
    Admin = create_tables_model(sql_conn)[2]

    try:
        key_md5 = md5()
        key_md5.update(key_in.encode('utf-8'))
        keyhash = key_md5.hexdigest()
        admin_record = Admin.select().where(Admin.password_hash == keyhash).get()
        sugar = admin_record.sugar
    except Admin.DoesNotExist:
        raise WrongKeyError

    if sugar == key:
        return 0
    else:
        raise WrongKeyError


def key_inputer(text: str) -> str:
    body = input(text + '\n>> ')
    return body


if __name__ == "__main__":
    config = read_yaml('config.yaml')
    language_dict = read_yaml(join('i18n', config.get('language', 'zh-CN') + '.yaml'))
    main_app(config, language_dict)
