
import json
import logging

_log = logging.getLogger()

class ResponseEntity:

    def __init__(self, statusCode, res = None):
        self.statusCode = statusCode
        self.res = res
        self.response_headers = [('Content-type', 'application/json')]

    @staticmethod
    def status(statusCode):
        ''' 自定义状态
        '''
        return ResponseEntity(statusCode)

    @staticmethod
    def ok(res):
        ''' 200，成功
        '''
        return ResponseEntity('200', res)

    @staticmethod
    def badRequest(res):
        ''' 400，错误请求
        '''
        return ResponseEntity('400', res)

    @staticmethod
    def unauthorized(res):
        ''' 401，权限不足
        '''
        return ResponseEntity('401', res)

    @staticmethod
    def notFound(res):
        ''' 404，未找到
        '''
        return ResponseEntity('404', res)
    
    def header(self, response_headers = [('Content-type', 'application/json')]):
        ''' 自定义HTTP头
        '''
        self.response_headers = response_headers
    
    def body(self, res):
        ''' 自定义HTTP内容
        '''
        self.res = res

    def build(self, start_response):
        ''' 生成请求
        :param start_response 函数计算的start_response
        :param token 返回给用户的token
        '''
        start_response(self.statusCode, self.response_headers)

        _log.info('返回数据:%s,状态码:%s' % (self.res, self.statusCode))

        if isinstance(self.res, str):
            return self.res.encode()
        
        if isinstance(self.res, dict) or isinstance(self.res, list):
            return json.dumps(self.res).encode()
        
        return str(self.res).encode()