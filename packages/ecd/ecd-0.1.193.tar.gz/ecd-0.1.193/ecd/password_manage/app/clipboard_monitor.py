# coding:utf-8
"""
author: sixi
datetime: 
python version: 3.x
summary: 
install package:
"""
import time

import pyperclip

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
    null = "nan"
    while 1:
        time.sleep(0.2)
        clp_txt = mc.read().strip().lower()
        if clp_txt != pre_txt and clp_txt != pre_clp_txt:
            _s_res = hd.search(clp_txt, 1)
            if _s_res:
                s_res = _s_res[0]['value']
                mc.write(s_res)
            else:
                mc.write(null)
                print(r'D:\\tmp\\password_infos.xlsx 没有数据，不能查找到value')
            pre_txt = clp_txt
            pre_clp_txt = null


if __name__ == '__main__':
    main()
