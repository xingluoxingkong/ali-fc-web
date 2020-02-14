import json
import logging

from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity

# 引入获取配置的方法
from AliFCWeb import getConfByName


@fcIndex(debug=True)
def handler(environ, start_response):
    pass

@get()
def testFC(data):
    # 获取配置
    mysqlConf = getConfByName('mysql')
    return ResponseEntity.ok(mysqlConf)
