# coding:utf-8
"""
author: sixi
datetime: 
python version: 3.x
summary: 
install package:
"""
from functools import wraps


def singleton(cls):
    """类的装饰器单例模式"""
    @wraps(cls)
    def _inner(*args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args, **kwargs)
        return cls._instance

    return _inner


