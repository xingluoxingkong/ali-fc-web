import json
import logging

from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity


@fcIndex(debug=True)
def handler(environ, start_response):
    pass


@get()
def testFC(data):
    return ResponseEntity.ok('Hello World!')
