import json
import logging
import functools

from .response import ResponseEntity
from .utils import pathMatch, responseFormat, getBodyAsJson

_log = logging.getLogger()

def fcIndex(auth = None):
    ''' 
    :param auth 鉴权，默认None。如果需要鉴权。请传入一个function。该function接受一个参数environ。
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            environ = args[0]
            start_response = args[1]
            http_host = environ['HTTP_HOST'] if 'HTTP_HOST' in environ else environ['REMOTE_ADDR']
            res = None
            token = None
            if auth:    # 是否需要验证权限
                if not auth(environ):
                    _log.warning('客户端%s请求:%s接口权限不足' % (http_host, environ['fc.request_uri']))
                    res = ResponseEntity.unauthorized('权限不足')
            
            if not res: # 登录验证和权限验证都通过了，则执行对应的方法
                res = _run(*args, **kw)
            _log.info('客户端%s请求:%s接口。返回结果:%s' % (http_host, environ['fc.request_uri'], res))
            return responseFormat(res, start_response)
        return wrapper
    return decorator

def _run(*args, **kw):
    ''' 根据请求类型（GET，POST）执行对应的方法
    '''
    environ = args[0]
    request_method = environ['REQUEST_METHOD']

    # 获取方法列表
    funcs = _getFuncs(environ)
    
    if request_method in funcs:
        # 选择方法
        fn = funcs[request_method]
        return fn(*args, **kw)
    else:
        return '请求类型不支持！'

def get(pattern = None):
    '''
    :param pattern  路径模板，以/开头，需要带上服务名和函数名。
                    如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段，会将路径中对应位置的路径解析为key的值
                    示例：https://xxxx.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/demo/getUserById/1
                        pattern = '/demo/getUserById/{id}'
                        解析后会自动填充参数id=1
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            # 获取接口地址
            environ = args[0]
            requestUri = environ['fc.request_uri']
            fcInterfaceURL = requestUri.split('proxy')[1].replace('.LATEST', '')
            # 解析参数
            params = pathMatch(fcInterfaceURL, pattern)
            if func.__code__.co_argcount == len(params):
                res = func(**params)
            else:
                res = ResponseEntity.badRequest('参数数目不对，需要%d个参数，收到%d个参数' % (func.__code__.co_argcount, len(params)))
            return res
        wrapper.__method__ = 'GET'
        return wrapper
    return decorator

def post(no = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            environ = args[0]
            body = getBodyAsJson(environ)
            return func(body)
        wrapper.__method__ = 'POST'
        return wrapper
    return decorator

def put(no = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            environ = args[0]
            body = getBodyAsJson(environ)
            return func(body)
        wrapper.__method__ = 'PUT'
        return wrapper
    return decorator

def delete(pattern = None):
    '''
    :param pattern  路径模板，以/开头，需要带上服务名和函数名。
                    如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段，会将路径中对应位置的路径解析为key的值
                    示例：https://xxxx.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/demo/getUserById/1
                        pattern = '/demo/getUserById/{id}'
                        解析后会自动填充参数id=1
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            # 获取接口地址
            environ = args[0]
            requestUri = environ['fc.request_uri']
            fcInterfaceURL = requestUri.split('proxy')[1].replace('.LATEST', '')
            # 解析参数
            params = pathMatch(fcInterfaceURL, pattern)
            body = getBodyAsJson(environ)
            if body:
                params.update(body)
            res = func(params)
            return res
        wrapper.__method__ = 'DELETE'
        return wrapper
    return decorator

def _getFuncs(environ):
    ''' 获取方法列表
    :param environ 函数计算的environ
    :return {'GET':get方法, 'POST':post方法, 'PUT':put方法, 'DELETE':delete方法}
    '''
    context = environ['fc.context']
    function = getattr(context, 'function')
    handler = getattr(function, 'handler')
    modName = handler.split('.')[0]

    mod = __import__(modName, globals(), locals())
    funcs = {}
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            funcs[method] = fn
    return funcs
        

