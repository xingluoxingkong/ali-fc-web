#####################################################################
#
# 工具文件
#
#####################################################################
import json
import time

def pathMatch(path, pattern = None):
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
    return params

def _format(s):
    ''' 把传入的字符串格式化成对应的格式：字符串；数字；json
    '''
    if not s or len(s) == 0:
        return ''
    
    if s.startswith('{') and s.endswith('}') or s.startswith('[') and s.endswith(']'):
        try:
            return json.loads(s)
        except :
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

def createId(environ):
    ''' 生成ID
    '''
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