import logging
import functools
from .response import ResponseEntity
from .utils import pathMatch, responseFormat, getBodyAsStr, getBodyAsJson

_log = logging.getLogger()

def fcIndex(login= None, auth = None, debug = False):
    ''' 
    :param login 登录认证方法，此方法接收一个参数environ，已登录返回True，未登录返回False
    :param auth 鉴权认证方法，此方法接收一个参数environ，鉴权通过返回True，鉴权不通过返回False
    :param debug 是否是调试模式，默认False，开启调试模式后所有的报错将直接返回给前端。
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            res = None
            newToken = None
            try:
                environ = args[0]
                start_response = args[1]
                http_host = environ['HTTP_HOST'] if 'HTTP_HOST' in environ else environ['REMOTE_ADDR']
                if login:   # 是否需要验证登录
                    if not login(environ):
                        _log.warning('客户端%s未登录请求:%s接口' % (http_host, environ['fc.request_uri']))
                        res = ResponseEntity.unauthorized('用户未登录，或登录已过期')
                if auth:    # 是否需要验证权限
                    if not auth(environ):
                        _log.warning('客户端%s请求:%s接口权限不足' % (http_host ,environ['fc.request_uri']))
                        res = ResponseEntity.unauthorized('权限不足')

                if not res: # 登录验证和权限验证都通过了，则执行对应的方法
                    res = _run(*args, **kw)
                _log.info('客户端%s请求:%s接口。返回结果:%s' % (http_host, environ['fc.request_uri'], res))
            except Exception as e:
                _log.error(e)
                if debug:
                    return e
                else:
                    res = ResponseEntity.serverError('服务器发生错误，请联系管理员查看系统日志!')
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
        return ResponseEntity.badRequest('请求类型不支持！') 

def get(pattern = None):
    ''' 使用方法
    @get(pattern="/ly-test/test/{id}")
    def testFun(params, environ, start_response):
        return ResponseEntity.ok('Hello World')

    :param pattern  可选参数。路径模板，以/开头，需要带上服务名和函数名。
                    如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段，会将路径中对应位置的路径解析为key的值
                    示例：https://xxxx.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/demo/getUserById/1
                        pattern = '/demo/getUserById/{id}'
                        解析后会自动填充参数id=1
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return _commonHttp(pattern, func, *args, **kw)
        wrapper.__method__ = 'GET'
        return wrapper
    return decorator

def post(pattern = None):
    ''' 使用方法
    @post(pattern="/ly-test/test/{id}")
    def testFun(params, environ, start_response):
        return ResponseEntity.ok('Hello World')

    :param pattern  可选参数。路径模板，以/开头，需要带上服务名和函数名。
                    如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段，会将路径中对应位置的路径解析为key的值
                    示例：https://xxxx.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/demo/getUserById/1
                        pattern = '/demo/getUserById/{id}'
                        解析后会自动填充参数id=1
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return _commonHttp(pattern, func, *args, **kw)
        wrapper.__method__ = 'POST'
        return wrapper
    return decorator

def put(pattern = None):
    ''' 使用方法
    @put(pattern="/ly-test/test/{id}")
    def testFun(params, environ, start_response):
        return ResponseEntity.ok('Hello World')

    :param pattern  可选参数。路径模板，以/开头，需要带上服务名和函数名。
                    如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段，会将路径中对应位置的路径解析为key的值
                    示例：https://xxxx.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/demo/getUserById/1
                        pattern = '/demo/getUserById/{id}'
                        解析后会自动填充参数id=1
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return _commonHttp(pattern, func, *args, **kw)
        wrapper.__method__ = 'PUT'
        return wrapper
    return decorator

def delete(pattern = None):
    ''' 使用方法
    @delete(pattern="/ly-test/test/{id}")
    def testFun(params, environ, start_response):
        return ResponseEntity.ok('Hello World')

    :param pattern  可选参数。路径模板，以/开头，需要带上服务名和函数名。
                    如果模板中有类似【/{key}/】或者【/{key}】或者【/{key}?】这样的字段，会将路径中对应位置的路径解析为key的值
                    示例：https://xxxx.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/demo/getUserById/1
                        pattern = '/demo/getUserById/{id}'
                        解析后会自动填充参数id=1
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return _commonHttp(pattern, func, *args, **kw)
        wrapper.__method__ = 'DELETE'
        return wrapper
    return decorator

def _commonHttp(pattern, func, *args, **kw):
    ''' 通用的HTTP请求处理方式，post，get，put，delete都可以用这个
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