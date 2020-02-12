######################################
#
# 发送http请求工具
#
######################################
import requests
import datetime

__all__ = ['getDataForStr', 'getDataForJson', 'getData', 'aMonthlater']

_HEADER = {
    'Content-Type': 'application/json; charset=utf-8',
    'Date': (datetime.datetime.now()-datetime.timedelta(hours=8)).strftime("%a, %d %b %Y %H:%M:%S GMT")
}


def getDataForStr(host, data):
    """ 获取配置文件
    :param data:请求内容,字符串
    """
    r = requests.post(host, headers=_HEADER, data=data.encode())
    return r


def getDataForJson(host, data):
    """ 获取配置文件
    :param data:请求内容,json格式
    """
    r = requests.post(host, headers=_HEADER, data=data)
    return r


def getData(host):
    """ 发送GET请求
    """
    r = requests.get(host, headers=_HEADER)
    return r


def aMonthlater(day=30):
    """ 生成cookie过期时间，默认30分钟
    格式：Tue, 19 Jan 2038 03:14:07 GMT
    """
    month_time = (datetime.datetime.now() + datetime.timedelta(days=day)
                  ).strftime("%a, %d %b %Y %H:%M:%S GMT")
    return month_time
