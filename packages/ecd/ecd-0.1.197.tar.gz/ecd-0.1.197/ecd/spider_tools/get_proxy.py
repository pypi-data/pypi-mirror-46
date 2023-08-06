# coding:utf-8
"""
author: sixi
datetime: 
python version: 3.x
summary:
    芝麻代理API获取代理：http://h.zhimaruanjian.com/
    使用：
        proxy_ip = ProxyIp(proxy_api, balance_api)
        status, proxy = proxy_ip.get_proxy()
    实现功能：
        1、缓存获取的代理，通过有效时间重新获取，或者使用缓存；
        2、scoket 检测端口，判断代理是否可用，自动获取缓存或者重新请求新的代理地址
install package:
"""
import copy
import json
import re
import socket
import time
import traceback
from math import inf
import requests
import logging

from ecd.spider_tools.user_agents import gen_random_ua
from ecd.common_tools.decrator_tools import singleton

logger = logging.getLogger(__name__)


@singleton
class ProxyIp(object):
    def __init__(self, proxy_api, balance_api=None, neek=None, appkey=None):
        """
        :param proxy_api: 获取代理的api
        :param balance_api: 获取余额的api
        :param cache_time: 代理ip有效时间
        :param use_cache: 是否缓存代理
        """
        assert "zhimacangku" in proxy_api, "需要提供正确的芝麻代理api：http://h.zhimaruanjian.com/"
        assert (neek and appkey), "需要提供白名单更新参数"
        self.neek = neek
        self.appkey = appkey
        self._white_pa = re.compile(r'请将(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})设置为白名单')
        self.proxy_api = proxy_api
        self.balance_api = balance_api
        self.ip_port_pa = re.compile(r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>\d+)')
        self._cache = {"cache_proxy": None}
        self._proxy_info = {"proxy": None, "create_time": None}
        self._use_times = 0

    def get_proxy(self, cache_time=20 * 60, try_times=5, sleep_time=1, timeout=3, use_cache=True,
                  use_times=inf,
                  flush=False):
        """
        获取代理ip
        :param cache_time: 每个缓存的代理有效时间（单位秒）
        :param try_times: 尝试获取代理ip的次数
        :param sleep_time: 每次获取失败的等待时间（单位秒）
        :param timeout: 代理ip的获取超时时间（单位秒）
        :param use_cache: 是否使用缓存
        :param use_times: 指定是https/http
        :param flush: 刷新缓存代理
        :return: type == tuple(状态，代理连接url)
        """
        # 代理服务：http://h.zhimaruanjian.com/getapi/#obtain_ip
        if use_cache and (self._use_times < use_times) and (not flush):
            status, ip_s = self._get_proxy_cache(cache_time)
            if status:
                return status, ip_s
        status, ip_s = self._get_proxy()
        count = 0
        while not status:
            if count > try_times:
                break
            time.sleep(sleep_time)
            status, ip_s = self._get_proxy(timeout)
            count += 1
        self._add_proxy_cacahe(ip_s)
        return status, ip_s

    def _get_proxy(self, timeout=5):
        """获取代理ip"""
        # 代理服务：http://h.zhimaruanjian.com/getapi/#obtain_ip
        headers = {"User-Agent": gen_random_ua()}
        resp = requests.get(url=self.proxy_api, headers=headers, timeout=timeout)
        if resp.status_code == 200 and resp.json()["success"]:
            ip_info = resp.json()["data"][0]
            prox = "{protcol}://{ip}:{port}".format(ip=ip_info["ip"], port=ip_info["port"], protcol="http")
            proxs = "{protcol}://{ip}:{port}".format(ip=ip_info["ip"], port=ip_info["port"], protcol="https")
            proxy_infos = {"http": prox, "https": proxs}
            return True, proxy_infos
        logger.warning("获取代理失败:{}".format(resp.json()))
        w_ip = self._white_pa.match(resp.json().get("msg", ""))
        if w_ip:
            self._add_white(w_ip.group("ip"))
        return False, None

    def _add_white(self, ip):
        try:
            url = "http://web.http.cnapi.cc/index/index/save_white?neek={n}&appkey={a}&white={ip}".format(ip=ip,
                                                                                                          n=self.neek,
                                                                                                          a=self.appkey)
            requests.get(url)
            logger.debug("代理ip白名单增加成功:{ip}".format(ip=ip))
        except Exception as e:
            logger.warning("代理ip白名单增加失败:{e}\n{t}".format(e=str(e), t=str(traceback.format_exc())))

    def _get_proxy_cache(self, cache_time):
        """获取缓存数据"""
        if not self._cache.get("cache_proxy"):
            return False, None
        c_time = self._cache["cache_proxy"]["create_time"]
        if time.time() - c_time > cache_time:
            return False, None
        proxy = self._cache["cache_proxy"]["proxy"]
        if self.valid_proxy(proxy):
            return True, proxy
        self._use_times += 1
        return False, None

    def _add_proxy_cacahe(self, url):
        _cache_item = copy.deepcopy(self._proxy_info)
        _cache_item["proxy"] = url
        _cache_item["create_time"] = time.time()
        self._cache["cache_proxy"] = _cache_item
        self._use_times = 0

    def get_proxy_balance(self):
        # 代理服务：http://h.zhimaruanjian.com/getapi/#obtain_ip
        headers = {"User-Agent": gen_random_ua()}
        if self.balance_api is None:
            msg = "没有提供余额查询api"
            logger.warning(msg)
            return msg
        resp = requests.get(url=self.balance_api, headers=headers)
        try:
            return json.dumps(resp.json())
        except Exception as e:
            return "余额查询失败, error:{}".format(str(e) + '\n' + str(traceback.format_exc()))

    def valid_proxy(self, url):
        if isinstance(url, dict):
            url = url.get('http', None)
        assert isinstance(url, str), "提供的url需要是字符串"
        u_status, (ip, port) = self.parse_host_port(url)
        assert u_status, "输入的待提取url中不包含主机ip和端口信息:{}".format(url)
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(3)
        resp = soc.connect_ex((ip, int(port)))
        soc.close()
        return resp == 0

    def parse_host_port(self, url):
        """获取主机名和端口"""
        m_obj = self.ip_port_pa.search(url)
        if m_obj:
            ip = m_obj.group("ip")
            port = m_obj.group("port")
            return True, (ip, port)
        return False, (None, None)


if __name__ == '__main__':
    pass
