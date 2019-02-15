
# 外层函数嵌套内层函数
# 外层函数返回内层函数
# 内层函数调用外层函数的参数
from functools import wraps

from flask import session, redirect, url_for


def is_login(func):
    @wraps(func)
    def check(*args, **kwargs):
        try:
            session.get('user_id')
        except:
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)
    return check















