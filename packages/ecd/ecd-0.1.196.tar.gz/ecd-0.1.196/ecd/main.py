# coding:utf-8
"""
author: Allen
datetime: 
python version: 3.x
summary: 
install package:
"""
import argparse
import re

from ecd.password_manage.app.clipboard_monitor import clp_main


def main():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('-c', '--clip', action='store_true', default=None,
                        help=r'以剪贴板内容为key根据相似度匹配值后写回剪贴板, 数据文件在 D:\\tmp\\password_infos.xlsx，自己维护 key,value的值')
    parser.add_argument('--ccf', '--clip-cache-file', default=r'D:\tmp\password_infos.xlsx',
                        type=str, help=r'指定数据文件路径')
    parser.add_argument('-d', '--dryrun', default=None, help='monitor clipboard and write value to clipboard')

    args = parser.parse_args()
    if args.clip:
        clp_main(args.ccf)


if __name__ == '__main__':
    main()
