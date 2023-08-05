# coding:utf-8
"""
author: sixi
summary: 记录日志
datetime: 2018/12/9
python version: 3.x
"""
import logging


class Logger(object):
    def __init__(self):
        pass

    @staticmethod
    def create_logger(path="file.log", log_level=logging.DEBUG, encoding='utf-8'):
        """
        创建日志函数
        :param path: 日志文件路径
        :param log_level: 日志等级:logging.DEBUG/logging.INFO/ logging.WARNING/logging.ERROR/logging.CRITICAL
        :param encoding: 文件编码
        :return: logger
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d:%(levelname)s:%(message)s")
        if path is not None:
            file_handler = logging.FileHandler(path, mode='a', encoding=encoding)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger


if __name__ == '__main__':
    pass
