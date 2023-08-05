# coding:utf-8
"""
@author:ZouLingyun
@date:
@summary:
"""
import platform
import time
import webbrowser
from concurrent.futures import ThreadPoolExecutor

from ecd.password_manage.app.password_web import app


def open_browser(url):
    if platform.system() == "MacOS":
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

    elif platform.system() == 'Windows':
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    elif platform.system() == 'Linux':
        chrome_path = '/usr/bin/google-chrome %s'
    else:
        raise SystemError("无法确定当前平台")
    webbrowser.get(chrome_path).open(url)


def main():
    host = '127.0.0.1'
    port = 9000
    m_pool = ThreadPoolExecutor(1)
    m_pool.submit(app.run, host=host, port=port)

    time.sleep(2)
    open_browser("http://{host}:{port}/".format(host=host, port=port))


if __name__ == '__main__':
    main()

