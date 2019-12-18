#####################################################################
#
# 工具文件
#
#####################################################################
import json
import time
from urllib.parse import unquote
from .constant import getConfByName, FC_ENVIRON

__all__ = ['pathMatch', 'createId', 'getBody', 'getBodyAsJson', 'getBodyAsStr']


def pathMatch(path, pattern=None):
    ''' 解析路径
    --
        :params path 路径，路径中形如【xxxx?key=value&key=value】的字符串会被解析成键值对
        :params pattern 路径模板。
                        如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段
                        会将path中对应位置的路径解析为key的值        
    '''
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
                    params[aa[0]] = _format(unquote(aa[1], 'utf-8'))
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
                            params[key] = _format(unquote(paths2[i], 'utf-8'))
    return params


def _format(s):
    ''' 把传入的字符串格式化成对应的格式：字符串；数字；json
    '''
    if not s or len(s) == 0:
        return ''

    if s.startswith('{') and s.endswith('}') or s.startswith('[') and s.endswith(']'):
        try:
            return json.loads(s)
        except:
            return s

    if s.isdigit():
        if s.startswith('0'):
            return s
        else:
            return int(s)

    if s.startswith('-') and s[1:].isdigit():
        return int(s)

    try:
        f = float(s)
        return f
    except ValueError:
        return s


def createId():
    ''' 生成ID
    '''
    environ = getConfByName(FC_ENVIRON)
    temp = str(time.time()).replace('.', '')
    if len(temp) < 17:
        temp = ("0" * (17-len(temp))) + temp
    if len(temp) > 17:
        temp = temp[:17]

    serviceName = str(int('0x' + environ['SERVER_NAME'], 16))
    if len(serviceName) < 15:
        serviceName = ("0" * (15 - len(serviceName))) + serviceName
    if len(serviceName) > 15:
        serviceName = serviceName[:15]

    return temp + serviceName

def getBody():
    ''' 读取body中的数据并自动格式化
    --
    '''
    environ = getConfByName(FC_ENVIRON)
    request_body_size = 0
    data = {}
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    data = environ['wsgi.input'].read(request_body_size)
    try:
        return json.loads(data)
    except Exception as e:
        pass
    
    try:
        from .fcutils import xml2dict
        xml = xml2dict.XML2Dict()
        return xml.parse(data)
    except Exception as e:
        pass
    
    return data
    
def getBodyAsJson():
    ''' 获取json格式的请求体
    '''
    environ = getConfByName(FC_ENVIRON)
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    return json.loads(environ['wsgi.input'].read(request_body_size)) if request_body_size > 0 else {}


def getBodyAsStr():
    ''' 获取string格式的请求体
    '''
    environ = getConfByName(FC_ENVIRON)
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    return environ['wsgi.input'].read(request_body_size)