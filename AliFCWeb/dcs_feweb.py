import json
import logging
import functools
from .utils import pathMatch
from fcutils import dataToJson
from inspect import isfunction
from .response import ResponseEntity
from .right import isLogin, updateToken, getTokenFromHeader, authRight, getBodyAsJson, getBodyAsStr

_log = logging.getLogger()

def dscFcIndex(debug = False):
    ''' 程序入口，拦截原函数计算入口，分发到对应的文件下，使用方法如下：
    --
        @example
            @dscFcIndex(debug = True)
            def handler(environ, start_response):
                pass
            
            当前函数计算的地址为：
                <account_id>.<region>.fc.aliyuncs.com/<version>/proxy/<serviceName>/<functionName>/[action?queries]

        @param debug 可选参数,是否是调试模式，默认False
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            environ = args[0]
            start_response = args[1]

            try:
                return _run(*args, **kw)
            except Exception as e:
                _log.error(e)
                if debug:
                    return e
                else:
                    res = ResponseEntity.serverError('服务器发生错误，请联系管理员查看系统日志!')
                    return _responseFormat(res, start_response)
        return wrapper
    return decorator

def _run(*args, **kw):
    ''' 根据请求类型（GET，POST）执行对应的方法
    '''
    environ = args[0]
    start_response = args[1]
    request_method = environ['REQUEST_METHOD']
    
    # 获取方法列表
    funcs = _getFuncs(environ)
    
    if request_method in funcs:
        # 选择方法
        fn = funcs[request_method]
        return fn(*args, **kw)
    else:
        res = ResponseEntity.badRequest('请求类型不支持！') 
        return _responseFormat(res, start_response)

def get(pattern = None, login = False, auth = False, uToken = False):
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
        @param auth 可选参数。是否需要鉴权，默认False
        @param uToken 可选参数。是否更新token，默认False
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return _commonHttpEntry(pattern, func, login, auth, uToken, *args, **kw)
        wrapper.__method__ = 'GET'
        return wrapper
    return decorator

def post(pattern = None, login = False, auth = False, uToken = False):
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
        @param auth 可选参数。是否需要鉴权，默认False
        @param uToken 可选参数。是否更新token，默认False
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return _commonHttpEntry(pattern, func, login, auth, uToken, *args, **kw)
        wrapper.__method__ = 'POST'
        return wrapper
    return decorator

def put(pattern = None, login = False, auth = False, uToken = False):
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
        @param auth 可选参数。是否需要鉴权，默认False
        @param uToken 可选参数。是否更新token，默认False
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return _commonHttpEntry(pattern, func, login, auth, uToken, *args, **kw)
        wrapper.__method__ = 'PUT'
        return wrapper
    return decorator

def delete(pattern = None, login = False, auth = False, uToken = False):
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
        @param auth 可选参数。是否需要鉴权，默认False
        @param uToken 可选参数。是否更新token，默认False
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return _commonHttpEntry(pattern, func, login, auth, uToken, *args, **kw)
        wrapper.__method__ = 'DELETE'
        return wrapper
    return decorator

def _commonHttpEntry(pattern, func, login = False, auth = False, uToken = False, *args, **kw):
    ''' 通用http入口， 先过滤一遍再执行_commonHttp
    --
    '''
    res = None
    newToken = None
    environ = args[0]
    start_response = args[1]
    
    http_host = environ['HTTP_HOST'] if 'HTTP_HOST' in environ else environ['REMOTE_ADDR']
    oldToken = getTokenFromHeader(environ)
    if login:   # 是否需要验证登录
        if not isLogin(oldToken):
            _log.warning('客户端%s请求:%s接口权限不足' % (http_host, environ['fc.request_uri']))
            res = ResponseEntity.unauthorized('用户未登录，或登录已过期')
    if auth:    # 是否需要验证权限
        if not authRight(oldToken, environ['fc.request_uri']):
            _log.warning('客户端%s请求:%s接口权限不足' % (http_host ,environ['fc.request_uri']))
            res = ResponseEntity.unauthorized('权限不足')
    if uToken: # 是否需要更新token
        newToken = updateToken(oldToken)
    
    if not res: # 登录验证和权限验证都通过了，则执行对应的方法
        res = _commonHttp(pattern, func, *args, **kw)
    
    responseData = _responseFormat(res, start_response, newToken)
    _log.info('客户端%s请求:%s接口。返回结果:%s' % (http_host, environ['fc.request_uri'], res))

    return responseData

def _commonHttp(pattern, func, *args, **kw):
    ''' 通用的HTTP请求处理方式，post，get，put，delete都可以用这个
    --
    '''
    # 获取接口地址
    environ = args[0]
    start_response = args[1]
    requestUri = environ['fc.request_uri']
    fcInterfaceURL = requestUri.split('proxy')[1].replace('.LATEST', '')
    # 解析参数
    params = pathMatch(fcInterfaceURL, pattern)
    body = {}
    try:
        body = getBodyAsJson(environ)
    except :
        body = getBodyAsStr(environ)
    
    if params == None:
        params = {}
    if body:
        params.update(body)
    res = func(params, environ, start_response)
    return res

def _getFuncs(environ):
    ''' 获取方法列表
    --
        @param environ 函数计算的environ
        @return {'GET':get方法, 'POST':post方法, 'PUT':put方法, 'DELETE':delete方法}
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
        if isfunction(fn):
            method = getattr(fn, '__method__', None)
            funcs[method] = fn
    return funcs

def _responseFormat(responseEntitys, start_response, token = None):
    ''' 格式化返回数据
    --
        :param res 返回数据
        :param start_response 函数计算的start_response
        :param token 用户token
        :return 按照函数计算的格式返回数据
    '''
    if not isinstance(responseEntitys, ResponseEntity):
        raise TypeError('只支持ResponseEntity格式的返回值')
    
    res = responseEntitys.build(start_response, token)
    codeRes = dataToJson(res)
    return [json.dumps(codeRes).encode()]