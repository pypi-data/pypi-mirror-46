# coding:utf-8
"""
author: sixi
summary: 指定目录发送目录下附件
datetime: 2018/12/9
python version: 3.x
"""
from __future__ import absolute_import

import os
import random
import smtplib
import time
import uuid
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEBase, MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from ecd.send_email_attachments.email_conf import Conf


def format_addr(add_info):
    name, addr = parseaddr(add_info)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send(to_addr, from_addr, smtp_server, password, e_content=None, keyword='', attach_path=None):
    if attach_path:
        files = os.listdir(attach_path)
        files = [os.path.join(attach_path, each) for each in files]
        print(files)
        files_count = len(files)
        for file in files:
            try:
                e_content = e_content or str(uuid.uuid1())
                msg = MIMEMultipart()
                msg['From'] = format_addr(from_addr)
                msg['To'] = format_addr(u'管理员 <%s>' % to_addr)
                msg['Subject'] = Header(str(uuid.uuid1()) + '___' + keyword + '___all count::%s___' % files_count,
                                        'utf-8').encode()
                msg.attach(MIMEText(e_content, 'plain', 'utf-8'))
                with open(file, 'rb') as fp:
                    mime = MIMEBase('application', 'octet-stream', filename=file)
                    mime.add_header('Content-Disposition', 'attachment', filename=file)
                    mime.add_header('Content-ID', '<0>')
                    mime.add_header('X-Attachment-Id', '0')
                    # 把附件的内容读进来:
                    mime.set_payload(fp.read())
                    # 用Base64编码:
                    encoders.encode_base64(mime)
                    # 添加到MIMEMultipart:
                    msg.attach(mime)
                server = smtplib.SMTP(smtp_server, Conf.port)
                server.login(from_addr, password)
                server.sendmail(from_addr, [to_addr], msg.as_string())
                server.quit()
                time.sleep(random.randint(2, 20))
            except Exception as e:
                print(e)
            else:
                with open('email.log', 'a+') as fp:
                    fp.write('send success :: %s' % file)
                    print('send success :: %s' % file)
                os.remove(file)


if __name__ == '__main__':
    send(Conf.to_addr, Conf.from_addr, Conf.smtp_server, Conf.password, keyword=Conf.keyword,
         attach_path=Conf.attach_path)
