# coding:utf-8
"""
author: Allen
datetime: 2019-3-16
python version: 3.x
summary: 多线程下开启多进程
install package:
"""
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from itertools import chain


def thread_concurrent(count, func, *args, **kwargs):
    """
    多线程执行工作函数
    :param count: 线程并发数
    :param func: 工作函数
    :param args: 工作函数参数
    :param kwargs: 工作函数参数
    :return:
    """
    th_pool = []
    th_pool_obj = ThreadPoolExecutor(count)
    for _ in range(count):
        th_pool.append(th_pool_obj.submit(func, *args, **kwargs))
    return [t.result() for t in th_pool]


def process_concurrent(proc_count=None, thread_count=None, func=None, *args, **kwargs):
    """
    多进程执行工作函数
    :param proc_count: 进程并发数
    :param thread_count: 线程并发数
    :param func:工作函数
    :return:
    """
    proc_count = proc_count or multiprocessing.cpu_count()
    proc_pool = []
    proc_pool_obj = ProcessPoolExecutor(proc_count)
    for _ in range(proc_count):
        proc_pool.append(proc_pool_obj.submit(thread_concurrent, count=thread_count, func=func, *args, **kwargs))
    return list(chain.from_iterable([t.result() for t in proc_pool]))


if __name__ == '__main__':
    pass
