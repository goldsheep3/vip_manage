"""该项目中所有的自定义错误类型"""


class WrongKeyError(Exception):
    def __init__(self):
        super().__init__()
