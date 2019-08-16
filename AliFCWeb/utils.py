#####################################################################
#
# 工具文件
#
#####################################################################
import re
import json
import logging
from .response import ResponseEntity

_log = logging.getLogger()

def getBodyAsJson(environ):
    ''' 获取json格式的请求体，并转换为对象
    '''
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    return json.loads(environ['wsgi.input'].read(request_body_size))

def getBodyAsStr(environ):
    ''' 获取string格式的请求体
    '''
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    return environ['wsgi.input'].read(request_body_size)

def responseFormat(responseEntitys, start_response):
    ''' 格式化返回数据
    :param res 返回数据
    :param start_response 函数计算的start_response
    :return 按照函数计算的格式返回数据
    '''
    if not isinstance(responseEntitys, ResponseEntity):
        err = TypeError('只支持ResponseEntity格式的返回值')
        _log.error(err)
        raise err
    
    return responseEntitys.build(start_response)

def pathMatch(path, pattern = None):
    ''' 解析路径
    :params path 路径，路径中形如【xxxx?key=value&key=value】的字符串会被解析成键值对
    :params pattern 路径模板。
                    如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段
                    会将path中对应位置的路径解析为key的值        
    '''
    _log.info('开始解析路径%s' % path)
    params = {}
    n = path.rfind('?')
    # 获取?后面的参数
    if n != -1:
        paths = path[n + 1:]
        if len(paths) > 0:
            arr = paths.split('&')
            for a in arr:
                aa = a.split('=')
                if len(aa) == 2:
                    params[aa[0]] = _format(aa[1])
    # 获取模板中的参数
    if pattern:
        paths1 = pattern.split('/')
        paths2 = path.split('/') if n == -1 else path[:n].split('/')
        if len(paths2) == len(paths1):
            for i, a in enumerate(paths1):
                if a.startswith('{') and a.endswith('}'):
                    key = a[1:-1]
                    if len(key) > 0:
                        if key not in params:
                            params[key] = _format(paths2[i])
    _log.info('解析成功%s' % params)
    return params

def _format(s):
    ''' 把传入的字符串格式化成对应的格式：字符串；数字；json
    '''
    if not s or len(s) == 0:
        return ''
    
    if s.startswith('{') and s.endswith('}') or s.startswith('[') and s.endswith(']'):
        return json.loads(s)
    
    if s.isdigit():
        return int(s)
    
    if s.startswith('-') and s[1:].isdigit():
        return int(s)
    
    try:
        return float(s)
    except:
        _log.error('格式转化错误，传入参数%s' % s)
        return s