import json
import logging

from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity


@fcIndex(debug=True)
def handler(environ, start_response):
    pass


@get()
def confirmSeller(data):
    print('前端传来的参数：')
    print(data)
    return ResponseEntity.ok(data)
