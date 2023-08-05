# coding:utf-8
"""
author: Allen
datetime: 
python version: 3.x
summary: 
install package:
"""
import argparse
import sys
import re


from ecd.password_manage.app.clipboard_monitor import main as clipboard_monitor_main

def main():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('-c', '--clip', action='store_true', default=None,
                        help='monitor clipboard and write value to clipboard')
    parser.add_argument('-d', '--dryrun', default=None, help='monitor clipboard and write value to clipboard')

    sp = list(filter(None, re.split(r'\s+', "python main.py -c -d 1")))[2:]
    args = parser.parse_args(sp)
    if args.clip:
        clipboard_monitor_main()


if __name__ == '__main__':
    main()
