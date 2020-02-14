import json
import logging

from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity


@fcIndex(debug=True)
def handler(environ, start_response):
    pass

@post('/demo05/{name}')
def testFC(data):
    print('前端传来的参数：')
    print(data)
    return ResponseEntity.ok(data)
