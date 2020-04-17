import json
import logging
import functools
import importlib
from inspect import isfunction
from urllib.parse import unquote

from .sign import Sign
from .response import ResponseEntity
from .constant import getConfByName, FC_ENVIRON, FC_START_RESPONSE
from .right import isLogin, updateToken, getTokenFromHeader

__all__ = ['fcIndex', 'get', 'post', 'put', 'delete']

_log = logging.getLogger()

def fcIndex(debug = False): 
    ''' 程序入口，拦截原函数计算入口，使用方法如下：
    --
        @fcIndex(debug = True)
        def handler(environ, start_response):
            pass
        
        @param debug: 可选参数,是否是调试模式，默认False
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            environ = args[0]
            start_response = args[1]

            # 初始化
            from .constant import init
            init(environ, start_response)
            
            try:
                return _run()
            except Exception as e:
                _log.error(e)
                res = None
                if debug:
                    res = ResponseEntity.badRequest(e)
                else:
                    res = ResponseEntity.badRequest('服务器发生错误，请联系管理员查看系统日志!')
                return _responseFormat(res)
        return wrapper
    return decorator

def _findFc():
    environ = getConfByName(FC_ENVIRON)
    # 接口地址
    requestUri = environ['fc.request_uri']

    # 如果没有使用自定义域名
    if requestUri.startswith("/2016-08-15/proxy"):
        # 去掉服务名
        fcInterfaceURL = requestUri.split('proxy/')[1]
        fcInterfaceURL = fcInterfaceURL[fcInterfaceURL.find('/') + 1:]
    else:
        fcInterfaceURL = fcInterfaceURL[1:] if fcInterfaceURL.startswith('/') else fcInterfaceURL
    
    # 去掉函数名
    fcInterfaceURL = fcInterfaceURL[fcInterfaceURL.find('/')+1:]
    # 去掉参数
    n = fcInterfaceURL.rfind('?')
    fcInterfaceURL = fcInterfaceURL[:n]
    
    module_name = fcInterfaceURL.split('/')[0]
    try:
        # 加载模块
        mod = importlib.import_module(module_name)
    except Exception as e:
        # 加载入口函数所在的文件
        context = environ['fc.context']
        function = getattr(context, 'function')
        handler = getattr(function, 'handler')
        module_name = handler.split('.')[0]
        module_name = module_name.replace('/', '.')
        mod = importlib.import_module(module_name)
    
    request_method = environ['REQUEST_METHOD'].upper() 

    func = None 
    
    for attr in dir(mod):
        if attr.startswith('__'):
            continue
        fn = getattr(mod, attr)
        
        if isfunction(fn):
            method = getattr(fn, '__method__', None)
            if request_method == method:
                func = fn
        if isinstance(fn, Sign):    # 替换标记
            setattr(mod, attr, fn.replace())
            
    return func

def _run():
    ''' 根据请求类型（GET，POST）执行对应的方法
    '''
    # 获取方法列表
    funcs = _findFc()
    
    if funcs:
        return funcs()
    else:
        res = ResponseEntity.badRequest('请求类型不支持！') 
        return _responseFormat(res)

def get(pattern = None, login = False, auth = None, uToken = False):
    ''' 使用方法
    --
        @get(pattern="/ly-test/test/{id}", login = True, auth = True, uToken = True)
        def testFun(params, environ, start_response):
            return ResponseEntity.ok('Hello World')

        @param pattern  可选参数。路径模板，以/开头，需要带上服务名和函数名。
                            如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段，会将路径中对应位置的路径解析为key的值
                            示例：https://xxxx.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/demo/getUserById/1
                                 pattern = '/demo/getUserById/{id}'
                                 解析后会自动填充参数id=1
        @param login 可选参数。是否需要登录，默认False
        @param auth 可选参数。鉴权函数。此函数接收一个参数token，返回true则鉴权通过，返回false则鉴权失败
        @param uToken 可选参数。是否更新token，默认False
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            return _commonHttpEntry(pattern, func, login, auth, uToken)
        wrapper.__method__ = 'GET'
        return wrapper
    return decorator

def post(pattern = None, login = False, auth = None, uToken = False):
    ''' 使用方法
    --
        @post(pattern="/ly-test/test/{id}", login = True, auth = True, uToken = True)
        def testFun(params, environ, start_response):
            return ResponseEntity.ok('Hello World')

        @param pattern  可选参数。路径模板，以/开头，需要带上服务名和函数名。
                            如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段，会将路径中对应位置的路径解析为key的值
                            示例：https://xxxx.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/demo/getUserById/1
                                 pattern = '/demo/getUserById/{id}'
                                 解析后会自动填充参数id=1
        @param login 可选参数。是否需要登录，默认False
        @param auth 可选参数。鉴权函数。此函数接收一个参数token，返回true则鉴权通过，返回false则鉴权失败
        @param uToken 可选参数。是否更新token，默认False
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            return _commonHttpEntry(pattern, func, login, auth, uToken)
        wrapper.__method__ = 'POST'
        return wrapper
    return decorator

def put(pattern = None, login = False, auth = None, uToken = False):
    ''' 使用方法
    --
        @put(pattern="/ly-test/test/{id}", login = True, auth = True, uToken = True)
        def testFun(params, environ, start_response):
            return ResponseEntity.ok('Hello World')

        @param pattern  可选参数。路径模板，以/开头，需要带上服务名和函数名。
                            如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段，会将路径中对应位置的路径解析为key的值
                            示例：https://xxxx.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/demo/getUserById/1
                                 pattern = '/demo/getUserById/{id}'
                                 解析后会自动填充参数id=1
        @param login 可选参数。是否需要登录，默认False
        @param auth 可选参数。鉴权函数。此函数接收一个参数token，返回true则鉴权通过，返回false则鉴权失败
        @param uToken 可选参数。是否更新token，默认False
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            return _commonHttpEntry(pattern, func, login, auth, uToken)
        wrapper.__method__ = 'PUT'
        return wrapper
    return decorator

def delete(pattern = None, login = False, auth = None, uToken = False):
    ''' 使用方法
    --
        @delete(pattern="/ly-test/test/{id}", login = True, auth = True, uToken = True)
        def testFun(params, environ, start_response):
            return ResponseEntity.ok('Hello World')

        @param pattern  可选参数。路径模板，以/开头，需要带上服务名和函数名。
                            如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段，会将路径中对应位置的路径解析为key的值
                            示例：https://xxxx.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/demo/getUserById/1
                                 pattern = '/demo/getUserById/{id}'
                                 解析后会自动填充参数id=1
        @param login 可选参数。是否需要登录，默认False
        @param auth 可选参数。鉴权函数。此函数接收一个参数token，返回true则鉴权通过，返回false则鉴权失败
        @param uToken 可选参数。是否更新token，默认False
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            return _commonHttpEntry(pattern, func, login, auth, uToken)
        wrapper.__method__ = 'DELETE'
        return wrapper
    return decorator

def _commonHttpEntry(pattern, func, login = False, auth = False, uToken = False):
    ''' 通用http入口， 先过滤一遍再执行_commonHttp
    --
    '''
    res = None
    newToken = None
    environ = getConfByName(FC_ENVIRON)
    start_response = getConfByName(FC_START_RESPONSE)
    
    http_host = environ['HTTP_HOST'] if 'HTTP_HOST' in environ else environ['REMOTE_ADDR']

    oldToken = getTokenFromHeader()
    if login:   # 是否需要验证登录
        if not isLogin(oldToken):
            _log.warning('客户端%s请求:%s接口权限不足' % (http_host, environ['fc.request_uri']))
            res = ResponseEntity.unauthorized('用户未登录，或登录已过期')
    if auth:    # 是否需要验证权限
        if not auth(oldToken):
            _log.warning('客户端%s请求:%s接口权限不足' % (http_host ,environ['fc.request_uri']))
            res = ResponseEntity.unauthorized('权限不足')
    if uToken: # 是否需要更新token
        newToken = updateToken(oldToken)
    
    if not res: # 登录验证和权限验证都通过了，则执行对应的方法
        res = _commonHttp(pattern, func)
    
    responseData = _responseFormat(res, newToken)
    _log.info('客户端%s请求:%s接口。返回结果:%s' % (http_host, environ['fc.request_uri'], res))

    return responseData

def _commonHttp(pattern, func):
    ''' 通用的HTTP请求处理方式，post，get，put，delete都可以用这个
    --
    '''
    # 获取接口地址
    environ = getConfByName(FC_ENVIRON)
    start_response = getConfByName(FC_START_RESPONSE)
    requestUri = environ['fc.request_uri']
    fcInterfaceURL = requestUri
    try:
        fcInterfaceURL = requestUri.split('proxy/')[1]
        fcInterfaceURL = fcInterfaceURL[fcInterfaceURL.find('/'):]
    except Exception as e:
        pass
    
    # 解析参数
    from .utils import pathMatch, getBody
    params = pathMatch(fcInterfaceURL, pattern)
    body = getBody()
    
    if params == None:
        params = {}
    if body:
        if not params:
            params = body
        elif isinstance(body, dict):
            params.update(body)
        else:
            params['body'] = body
    res = func(params)
    return res



def _responseFormat(responseEntity, token = None):
    ''' 获取返回数据
    --
        :param res 返回数据
        :param token 用户token
        :return 按照函数计算的格式返回数据
    '''
    if not isinstance(responseEntity, ResponseEntity):
        raise TypeError('只支持ResponseEntity格式的返回值')
    
    return responseEntity.build(token)
