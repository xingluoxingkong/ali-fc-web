import json
import logging

from AliFCWeb import fcIndex, get, post, put, delete

# 引入自定义的ResponseEntity
from myResponseEntity import MyResponseEntity

@fcIndex(debug=True)
def handler(environ, start_response):
    pass

@get()
def testFC(data):
    res = MyResponseEntity('200', data.get('name', 'World'))
    return res
