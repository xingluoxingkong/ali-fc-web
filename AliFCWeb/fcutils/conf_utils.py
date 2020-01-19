######################################
#
# 读取配置文件工具
#
######################################
import json
import importlib
from .http_utils import getDataForStr

__all__ = ['getConfig', 'getConfigFromConfCenter']

def getConfig(configName):
    ''' 读取本地配置文件
    --
    '''       

    module = importlib.import_module(configName)
    
    conf = {}
    for attr in dir(module):
        if attr.startswith('__'):
            continue
        
        conf[attr] = getattr(module, attr)
    
    return conf
    

def getConfigFromConfCenter(url, configNames, pwd = None):
    ''' 从网络配置中心获取配置
    --
        @param url: 配置中心地址
        @param configNames: 配置名列表，字典格式
        @param pwd: 密码
    '''
    data = configNames
    if pwd:
        data = {
            'pwd': pwd,
            'config_names': configNames
        }
        data = json.dumps(data)
    res = getDataForStr(url, data)
    return res
