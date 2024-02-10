from datetime import datetime
from hashlib import md5
from re import compile as comp
from peewee import SqliteDatabase, fn
from lib.sql_table import create_tables_model

key_sugar = {
    'login': 160523498730,
    'verify': 202838234617
}


class NormalPay:
    def __init__(self):
        pass


def card_id_search(card_id: int,
                   conn: SqliteDatabase) -> tuple:
    """数据库卡号搜索代码，返回数据结果元组。"""

    # 获取模型
    BaseInfo = create_tables_model(conn)[0]
    # 通过完整卡号进行查询
    matching_items = BaseInfo.select().where(BaseInfo.card_id == card_id)
    if len(matching_items) == 0:
        # 无匹配记录
        raise NameError(32)
    elif len(matching_items) == 1:
        # 一条匹配记录
        return matching_items

    raise


def phone_search(phone: str,
                 conn: SqliteDatabase) -> tuple:
    """数据库手机号搜索代码，返回数据结果元组。"""

    # 定义手机号码的正则表达式模式
    phone_number_pattern = comp(r'^1[3456789]\d{9}$')
    # 获取模型
    BaseInfo = create_tables_model(conn)[0]
    # 根据手机号长度判断查询条件
    if len(phone) == 4:
        # 如果手机号长度为4，通过查询末尾4位匹配记录
        matching_items = BaseInfo.select().where(fn.SUBSTR(BaseInfo.phone_number, -4) == phone)
        if len(matching_items) == 0:
            # 无匹配记录
            raise NameError(32)
        else:
            return matching_items
    elif phone_number_pattern.match(phone):
        # 如果手机号符合正则表达式模式，通过完整手机号进行查询
        matching_items = BaseInfo.select().where(BaseInfo.phone_number == phone)
        if len(matching_items) == 0:
            # 无匹配记录
            raise NameError(33, phone)
        elif len(matching_items) == 1:
            # 一条匹配记录
            return matching_items
    else:
        raise ValueError(164)


def get_history(card_id: int,
                conn: SqliteDatabase,
                back_sort = False) -> tuple:
    """获取指定卡号的历史记录"""

    # 获取模型
    History = create_tables_model(conn)[1]

    # 查询指定卡号的历史记录
    history_items = History.select().where(History.card_id == card_id)

    # 如果没有匹配的历史记录，则返回空列表
    if not history_items:
        return ()

    # 构建历史记录列表
    history_list = []
    for item in history_items:
        # 判断收支类型并设置变动符号
        variation_sign = '+' if item.iae >= 0 else '-'
        # 构建历史记录字典
        history_dict = {
            'date': datetime.fromtimestamp(int(item.time)).strftime('%Y.%m.%d'),
            'v_sign': variation_sign,
            'money_value': '{:.2f}'.format(item.iae/100),
            'variation_type': '储值' if item.iae >= 0 else '消费',
            'category': item.category,
            'note': item.note
        }
        history_list.append(history_dict)

    if back_sort:
        history_list = history_list[::-1]

    return tuple(history_list)


def check_md5_key(conn: SqliteDatabase,
                  key_in: str,
                  key: int) -> int:
    """MD5校验代码"""

    # 获取Admin模型
    Admin = create_tables_model(conn)[2]
    try:
        # 使用MD5哈希算法对输入的密码进行哈希
        key_md5 = md5()
        key_md5.update(key_in.encode('utf-8'))
        keyhash = key_md5.hexdigest()
        # 查询数据库以获取与哈希匹配的管理员记录
        admin_record = Admin.select().where(Admin.password_hash == keyhash).get()
        sugar = admin_record.sugar
    except Admin.DoesNotExist:
        raise NameError(32)
    if sugar == key:
        # 如果管理员记录的`sugar`值与传入的密钥匹配，返回0表示验证成功
        return 0
    else:
        raise ValueError(42)
