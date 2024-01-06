from hashlib import md5
from re import compile as comp
from peewee import SqliteDatabase, fn
from lib.sql_table import create_tables_model

key_sugar = {
    'login': 160523498730,
    'verify': 202838234617
}


def search(phone: int,
           conn: SqliteDatabase) -> int:
    """数据库手机号搜索代码"""
    phone_number_pattern = comp(r'^1[3456789]\d{9}$')
    BaseInfo, History = create_tables_model(conn)
    if 1000 <= phone <= 9999:
        matching_items = BaseInfo.select().where(fn.RIGHT(BaseInfo.phone_number, 4) == phone)
        if len(matching_items) == 0:
            print('无匹配')
            raise NameError(32)
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
    else:
        raise ValueError
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


