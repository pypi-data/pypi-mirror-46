# coding:utf-8
"""
author: Allen
datetime: 
python version: 3.x
summary: 
install package:
"""
import random
import time

import requests

from ecd.concurrent_p_t.pressure_base import process_concurrent


def req_api(url, *args, **kwargs):
    resp = requests.post(url, *args, **kwargs)
    return resp


def random_req():
    url = "http://127.0.0.1:5000"
    datas = [
        "对系统进行压力测试和监视的目的是为了确定瓶颈。",
        "在这里发布了一个页面，其中描述了在服务器上应用的压力测试和性能结果。",
        "力测试和监视&使用峰值工作负载，对系统进行监视和压力测试。",
        "是一个反复的过程，应该通过压力测试和基准测试验证该设计。"
    ]
    st = time.time()
    req_ok, resp_json = False, None
    try:
        resp = req_api(url=url, json={"data": random.choice(datas)}, timeout=5)
        req_ok, resp_json = True, resp.json()
    except Exception:
        pass
    cost = time.time() - st
    return cost, req_ok, resp_json


def main(*args, **kwargs):
    return process_concurrent(*args, **kwargs)


if __name__ == '__main__':
    res = main(proc_count=8, thread_count=10000, func=random_req)
    print('min cost time: ', min([r[0] for r in res]))
    print('max cost time: ', max([r[0] for r in res]))
    print("request ok: ", len(list(filter(None, [r[1] for r in res]))))
    print("request error: ", len(list(filter(lambda x: not bool(x), [r[1] for r in res]))))
