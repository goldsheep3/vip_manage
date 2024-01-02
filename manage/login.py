from peewee import Model, PrimaryKeyField, CharField, IntegerField
import hashlib


class WrongKeyError(Exception):
    def __init__(self):
        super().__init__()


def get_sugar(conn, key: str) -> int:
    class Admin(Model):
        id = PrimaryKeyField()
        password_hash = CharField()
        sugar = IntegerField()

        class Meta:
            database = conn

    try:
        key_md5 = hashlib.md5()
        key_md5.update(key.encode('utf-8'))
        keyhash = key_md5.hexdigest()
        admin_record = Admin.select().where(Admin.password_hash == keyhash).get()
        sugar = admin_record.sugar
    except Admin.DoesNotExist:
        raise WrongKeyError
    else:
        return sugar


def login(conn, trans, ui: bool = False, password: str = None):

    if not password:
        password = str(input(trans['press_key'] + '\n' + trans['without_ui']['forget_pwd'])).strip()

    if password == '?' and not ui:
        key = str(input(trans['wrong']['tip1'] + '\n' + trans['wrong']['tip2'])).strip()
        try:
            verify(conn, key)
        except WrongKeyError:
            print(trans['forget']['verify']['wrong2'])
            login(conn, trans, ui, password=None)
        else:
            return 2

    try:
        sugar = get_sugar(conn, password)
    except WrongKeyError:
        if ui:
            raise
        else:
            print(trans['title'], trans['tip'])
            login(conn, trans, ui, password=None)
    else:
        if sugar == 160523498730:
            return 0

    return 24


def verify(conn, entered_key):
    sugar = get_sugar(conn, entered_key)
    if sugar == 202838234617:
        return
    else:
        raise WrongKeyError
