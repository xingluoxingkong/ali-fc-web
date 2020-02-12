import json
from .right import encodeToken
from .fcutils import dataToJson, dict2xml
from .constant import getConfByName, FC_START_RESPONSE

__all__ = ['ResponseEntity']


class ResponseEntity:

    def __init__(self, statusCode, res=None, token=None):
        ''' 返回数据封装
        --
            @param statusCode: http代码
            @param res: 返回的数据【dict, list, str】
            @param token: token
        '''
        self.statusCode = statusCode
        self.res = res
        self.response_headers = [('Content-type', 'application/json')]
        self.token = token
        self.num = -1
        self.resType = 'json'
        self._kw = None

    @staticmethod
    def status(statusCode):
        ''' 自定义状态
        --
        '''
        return ResponseEntity(statusCode)

    @staticmethod
    def ok(res):
        ''' 200，成功
        --
        '''
        return ResponseEntity('200', res)

    @staticmethod
    def responseXml(res):
        ''' 返回xml
        --
        '''
        return ResponseEntity('200', res, resType='xml')

    @staticmethod
    def badRequest(res):
        ''' 400，错误请求
        --
        '''
        return ResponseEntity('400', res)

    @staticmethod
    def unauthorized(res):
        ''' 401，权限不足
        --
        '''
        return ResponseEntity('401', res)

    @staticmethod
    def notFound(res):
        ''' 404，未找到
        --
        '''
        return ResponseEntity('404', res)

    @staticmethod
    def serverError(res):
        ''' 500, 服务器错误
        --
        '''
        return ResponseEntity('500', res)

    def setResType(self, resType):
        ''' 设置返回值类型
        --
        '''
        if resType == 'json':
            self.header([('Content-type', 'application/json')])
        elif resType == 'xml':
            self.header([('Content-type', 'text/xml')])
        elif resType == 'html':
            self.header([('Content-type', 'text/html')])
        else:
            return self

        self.resType = resType
        return self

    def header(self, response_headers=[('Content-type', 'application/json')]):
        ''' 自定义HTTP头
        --
        '''
        if isinstance(response_headers, list):
            return self
        if len(response_headers) < 1:
            return self
        if isinstance(response_headers[0], tuple):
            return self

        for h in response_headers:
            if h[0] == 'Content-type':
                if 'json' in h[1]:
                    self.resType = 'json'
                elif 'xml' in h[1]:
                    self.resType = 'xml'
                elif 'html' in h[1]:
                    self.resType = 'html'
                else:
                    return self
                self.response_headers = response_headers
                return self
         return self
    
    def body(self, res):
        ''' 自定义Data内容
        --
        '''
        self.res = res
        return self

    def setToken(self, token):
        ''' 自定义token
        --
        '''
        self.token = token
        return self
    
    def setKW(self, **kw):
        ''' 自定义返回值，此处定义的参数与data同级
        --
        '''
        self._kw = kw
        return kw
    
    def setNum(self, num):
        ''' 自定义num，data数据为list时有效
        --
        '''
        self.num = num
        return self
    
    def build(self, token = None):
        ''' 生成请求
        :param token 返回给用户的token
        '''
        start_response = getConfByName(FC_START_RESPONSE)
        start_response(self.statusCode, self.response_headers)
        
        response = {}
        data = {}
        
        if self._kw:
            response.update(self._kw)
        
        if isinstance(self.res, str):
            # html直接编码返回
            if self.resType == 'html':
                return [self.res.encode()]
            data = self.res
        elif isinstance(self.res, list):
            data = {'sum':len(self.res) if self.num == -1 else self.num, 'list':self.res}
        elif isinstance(self.res, tuple):
            data = {'sum':len(self.res) if self.num == -1 else self.num, 'list':list(self.res)}
        elif isinstance(self.res, dict) :
            if self.resType == 'json':
                data = self.res
            elif self.resType == 'xml':
                xml = dict2xml.Dict2XML()
                data = xml.parse(self.res)
        else:
            data = str(self.res)

        if self.statusCode == '200':
            # 优先使用自定义Token
            if self.token:
                response['token'] = encodeToken(self.token)
            elif token:
                response['token'] = encodeToken(token)
        
        response['data'] = data

        codeRes = dataToJson(response)
        return [json.dumps(codeRes).encode()]

    def __str__(self):
        return json.dumps({'status':self.statusCode, 'res':dataToJson(self.res)}) 
