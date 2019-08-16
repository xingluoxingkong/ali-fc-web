# 函数计算工具库

## 安装
``` shell
pip install AliFCWeb
```

## 使用

import logging
from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
import json

def authTest(environ):
    return False

@fcIndex(auth = authTest)
def handler(environ, start_response):
   pass

@get('/demo/text-application/{id}')
def testGet(id):
    return ResponseEntity.ok('收到GET请求，请求内容%d' % id)

@post()
def testPost(user):
    return ResponseEntity.ok('收到POST请求,请求内容%s' % user)

@put()
def testPut(user):
    return ResponseEntity.ok('收到PUT请求,请求内容%s' % user)

@delete()
def testDelete(user):
    return ResponseEntity.ok('收到DELETE请求,请求内容%s' % user)