import json
import logging

from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity

_log = logging.getLogger()

@fcIndex(debug=True)
def handler(environ, start_response):
    pass

def myAuth(token):
    if token['user_id'] == 1:
        return True
    return False

@post(login=True, auth=myAuth)
def testPost(data):
    return ResponseEntity.ok('操作成功')






    


