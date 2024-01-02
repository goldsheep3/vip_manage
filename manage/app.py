import peewee
from lib.read import read_yaml
from os.path import join


if __name__ == "__main__":
    config = read_yaml('config.yaml')
    i18n = read_yaml(join('i18n', config.get('language', 'zh-CN') + '.yaml'))
    conn = peewee.SqliteDatabase('database.db')
