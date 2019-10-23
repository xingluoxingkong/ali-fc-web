import json
from .right import encodeToken
from fcutils import dataToJson

class ResponseEntity:

    def __init__(self, statusCode, res = None, token = None):
        self.statusCode = statusCode
        self.res = res
        self.response_headers = [('Content-type', 'application/json')]
        self.token = token
        self.num = -1

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
    
    @staticmethod
    def serverError(res):
        ''' 500, 服务器错误
        '''
        return ResponseEntity('500', res)
    
    def header(self, response_headers = [('Content-type', 'application/json')]):
        ''' 自定义HTTP头
        '''
        self.response_headers = response_headers
        return self
    
    def body(self, res):
        ''' 自定义HTTP内容
        '''
        self.res = res
        return self

    def setToken(self, token):
        ''' 自定义token
        '''
        self.token = token
        return self
    
    def setNum(self, num):
        ''' 自定义num
        '''
        self.num = num
        return self
    
    def build(self, start_response, token = None):
        ''' 生成请求
        :param start_response 函数计算的token
        :param token 返回给用户的token
        '''
        start_response(self.statusCode, self.response_headers)
        response = {}

        data = {}
        if isinstance(self.res, list):
            if self.num != -1:
                n = self.num
            data = {'sum':len(self.res) if self.num == -1 else self.num, 'list':self.res}
        elif isinstance(self.res, str):
            data = {'msg': self.res}
        else :
            data = self.res

        if self.statusCode == '200':
            response['message'] = 'success'
            # 优先使用自定义Token
            if self.token:
                response['token'] = encodeToken(self.token)
            elif token:
                response['token'] = encodeToken(token)
        else:
            response['message'] = 'fail'
        
        response['data'] = data

        return response

    def __str__(self):
        return json.dumps({'status':self.statusCode, 'res':dataToJson(self.res)}) 