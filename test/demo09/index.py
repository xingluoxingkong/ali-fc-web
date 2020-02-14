import json
import logging

from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity

from AliFCWeb import getPayloadFromHeader

_log = logging.getLogger()

@fcIndex(debug=True)
def handler(environ, start_response):
    pass

@get()
def testFC(data):
    password = data['password']
    if password == 123456:
        # 获取Token
        userId = data.get('id', 1)
        return ResponseEntity.ok('登录成功！').setToken({'user_id': userId})
    else:
        return ResponseEntity.unauthorized('密码错误！')

@post(login=True)
def testPost(data):
    token = getPayloadFromHeader()
    _log.info(token)
    return ResponseEntity.ok('操作成功')


    


