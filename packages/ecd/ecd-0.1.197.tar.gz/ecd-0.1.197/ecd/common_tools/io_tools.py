# coding:utf-8
"""
author: sixi
summary: 文件io操作
datetime: 2018/12/9
python version: 3.x
"""
import os
from io import BytesIO
from io import StringIO
from typing import AnyStr
from typing import List


class IoHandler(object):
    def __init__(self):
        self.fp = None

    @staticmethod
    def read_txt(path: str, encoding='utf-8', mode=0):
        """
        读取txt文件
        :param path: 文件路径
        :param encoding: 编码
        :param mode: 读取模式，0：按行读取， 1：读取全部
        :return: list/str
        """
        with open(path, 'r', encoding=encoding) as fp:
            if mode == 0:
                data = fp.readlines()
            else:
                data = fp.read()
        return data

    @staticmethod
    def write_str(path: str, str_d: str) -> None:
        with open(path, 'w', encoding="utf-8") as fp:
            fp.write(str_d)

    @staticmethod
    def write_str_seq(path: str, str_seq) -> None:
        with open(path, 'w', encoding="utf-8") as fp:
            fp.write('\n'.join(str_seq))

    @staticmethod
    def read_byte(path: str) -> bytes:
        """
        读取二进制文件
        :param path: 文件路径
        :return: 二进制流
        """
        with open(path, 'rb') as fp:
            data = fp.read()
        return data

    def io_byte_fp(self, byte_data: bytes) -> BytesIO:
        """
        构建内存二进制文件对象
        :param byte_data: 二进制数据
        :return: 文件对象
        """
        self.fp = BytesIO()
        self.fp.write(byte_data)
        self.fp.seek(0, 0)
        return self.fp

    def io_str_fp(self, str_data: str) -> StringIO:
        """
        构建内存字符串文件对象
        :param str_data: 字符串
        :return: 文件对象
        """
        self.fp = StringIO()
        self.fp.write(str_data)
        self.fp.seek(0, 0)
        return self.fp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()


class HandlerFs(object):
    def __init__(self):
        """操作文件系统"""
        pass

    @staticmethod
    def scan_dir(path: AnyStr, recursion=True) -> List:
        """
        扫描目录
        :param path: 开始路径
        :param recursion: 是否递归扫描
        :return: 文件绝对路径列表
        """

        if recursion:
            res = []
            for fi in os.walk(path):
                res.extend([os.path.join(fi[0], f) for f in fi[2]])
            return res
        else:
            return [os.path.join(path, f) for f in os.listdir(path)]

    @staticmethod
    def mk_dirs(path: str):
        if not os.path.exists(path):
            os.makedirs(path)


if __name__ == '__main__':
    pass
