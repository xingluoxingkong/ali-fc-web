import sys
import json
import importlib

def handler(environ, start_response):
    # 获取请求体
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = json.loads(environ['wsgi.input'].read(request_body_size))

    configFile = importlib.import_module('application')
    
    # 验证密码
    pwd = getattr(configFile, 'pwd')
    if pwd != request_body['pwd']:  # 密码错误
        status = '401'
        response_headers = [('Content-type', 'application/json')]
        start_response(status, response_headers)
        return [json.dumps({"message": "fail","data": "权限不足"}).encode()]
    
    try:
        confData = {}
        configNames = request_body['config_names']
        if isinstance(configNames, list) or isinstance(configNames, tuple):
            for name in configNames:
                confData[name] = getattr(configFile, name)
        else:
            confData = getattr(configFile, configNames)

        status = '200'
        response_headers = [('Content-type', 'application/json')]
        start_response(status, response_headers)
        
        if isinstance(confData, dict):
            return [json.dumps(confData).encode()]

        return [confData.encode()]
    except Exception as e:
        status = '404'
        response_headers = [('Content-type', 'application/json')]
        start_response(status, response_headers)
        return [json.dumps({"message": "fail","data": "配置不存在"}).encode()]