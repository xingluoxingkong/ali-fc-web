######################################
#
# 读取配置文件工具
#
######################################
import json
import importlib
from .http_utils import getDataForStr

def getConfig(names, configFileName = 'application'):
    ''' 读取本地配置文件
    --
        @param names: 配置名,列表格式/元组格式/字符串格式
        @param configFileName: 配置文件名字，默认使用同目录下的application.py文件

        @return: names为列表或者元组返回{配置名:配置值...}; names为字符串直接返回该配置
    '''
    if '.' in configFileName:
            configFileName = configFileName.split('.')[0]

    configFile = importlib.import_module(configFileName)

    if isinstance(names, list) or isinstance(names, tuple):
        confDatas = {}
        for name in names:
            confData = getattr(configFile, name, None)
            if isinstance(confData, bytes):
                confData = str(confData, encoding='utf-8')
            confDatas[name] = confData
        return confDatas
    else:
        confData = getattr(configFile, names, None)
        if isinstance(confData, bytes):
            return str(confData, encoding='utf-8')
        return confData
    

def getConfigFromConfCenter(url, configNames, pwd):
    ''' 从网络配置中心获取配置
    --
        @param url: 配置中心地址
        @param configNames: 配置名列表，字典格式
        @param pwd: 密码
    '''
    data = {
        'pwd': pwd,
        'config_names': configNames
    }
    res = getDataForStr(url, json.dumps(data))
    return res
