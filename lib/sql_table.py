from peewee import CharField, Model, IntegerField


def create_tables_model(conn):
    class BaseModel(Model):
        class Meta:
            database = conn

    class BaseInfo(BaseModel):
        phone_number = CharField(unique=True, null=False)
        card_id = IntegerField(primary_key=True, unique=True, null=False)
        name = CharField()
        wechat = CharField()
        birthday = CharField()
        balance = IntegerField(null=False)

    class History(BaseModel):
        card_id = IntegerField(null=False)
        time = IntegerField(primary_key=True, unique=True, null=False)
        category = CharField(null=False)
        note = CharField(null=True)
        iae = IntegerField(null=False)
        balance = IntegerField(null=False)

    class Admin(BaseModel):
        id = IntegerField(primary_key=True)
        password_hash = CharField(null=False)
        sugar = IntegerField(null=False)

    return BaseInfo, History, Admin
