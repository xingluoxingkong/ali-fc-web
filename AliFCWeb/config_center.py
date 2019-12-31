import sys
import json
import importlib
import functools
__all__ = ['configCenter']
def configCenter(fileName='application'):
    ''' 配置中心
    --
        @param fileName: 配置文件名
    ''' 
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            environ = args[0]
            start_response = args[1]
            # 获取请求体
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_body_size = 0
            request_body = json.loads(environ['wsgi.input'].read(request_body_size))
            response_headers = [('Content-type', 'application/json')]
            
            configFile = importlib.import_module(fileName)
            
            # 验证密码
            pwd = getattr(configFile, 'pwd', None)
            if pwd:
                if pwd != request_body['pwd']:
                    status = '401'
                    start_response(status, response_headers)
                    return [json.dumps({"message": "fail","data": "密码错误"}).encode()]
            
            try:
                confData = {}
                configNames = request_body['config_names']
                if isinstance(configNames, list) or isinstance(configNames, tuple):
                    for name in configNames:
                        confData[name] = getattr(configFile, name)
                else:
                    confData = getattr(configFile, configNames)

                status = '200'
                start_response(status, response_headers)
                
                if isinstance(confData, dict):
                    return [json.dumps(confData).encode()]

                return [confData.encode()]
            except Exception as e:
                status = '404'
                start_response(status, response_headers)
                return [json.dumps({"message": "fail","data": "配置不存在"}).encode()]
        return wrapper
    return decorator