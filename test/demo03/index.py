import json
import logging

from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity


@fcIndex(debug=True)
def handler(environ, start_response):
    pass

# 改为post请求
@post()
def testFC(data):
    print('前端传来的参数：')
    print(data)
    return ResponseEntity.ok(data)
