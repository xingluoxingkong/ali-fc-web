import json
import logging

from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
from mySign import MySign

_log = logging.getLogger()


@fcIndex(debug=True)
def handler(environ, start_response):
    pass

# 使用锚点
@MySign
def getUrl():
    pass

@get()
def testFC(data):
    return ResponseEntity.ok(getUrl)
