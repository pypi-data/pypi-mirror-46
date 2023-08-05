# coding:utf-8
"""
author: sixi
datetime: 
python version: 3.x
summary: 
install package:
"""
import pyperclip
import time
from ecd.password_manage.app.handle_data import HandleData


class MonitorClipboard(object):
    def read(self):
        return pyperclip.paste()

    def write(self, txt: str):
        pyperclip.copy(txt)


def main():
    mc = MonitorClipboard()
    hd = HandleData()
    pre_txt = None
    pre_clp_txt = None
    while 1:
        time.sleep(0.2)
        clp_txt = mc.read().strip().lower()
        if clp_txt != pre_txt and clp_txt != pre_clp_txt:
            s_res = hd.search(clp_txt, 1)[0]['value']
            pre_txt = clp_txt
            pre_clp_txt = s_res
            mc.write(s_res)


if __name__ == '__main__':
    main()
