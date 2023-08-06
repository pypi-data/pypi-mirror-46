#coding:utf-8
"""
author: sixi
summary: 指定目录发送目录下附件，配置文件
datetime: 2018/12/9
"""
class Conf(object):
    # 收件地址
    to_addr = 'xxx2@xxx.com'
    # 发件地址
    from_addr = 'xxx@xxx.com'
    # 发件邮箱的 smtp 服务器
    smtp_server = ''
    # 发件邮箱密码
    password = 'xxx'
    # 标题关键字，方便识别
    keyword = ''
    # 存放文件目录
    attach_path = r''
    # smtp 服务端口
    port = 25