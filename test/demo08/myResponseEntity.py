from AliFCWeb import ResponseEntity
from AliFCWeb import getConfByName, FC_START_RESPONSE
class MyResponseEntity(ResponseEntity):
    
    def build(self, token = None):
        # 设置请求头和请求code
        # 这一步必须要
        start_response = getConfByName(FC_START_RESPONSE)
        start_response(self.statusCode, self.response_headers)
        
        # self.res中储存了要返回的数据
        res = 'Hello ' + self.res
        return [res.encode()]