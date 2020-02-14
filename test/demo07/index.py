import json
import logging

from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity

from AliFCWeb import getConfByName, CONF_CENTER_NAME
# 引入getConfigFromConfCenter方法
# 该方法在AliFCWeb.fcutils包下
from AliFCWeb.fcutils import getConfigFromConfCenter


@fcIndex(debug=True)
def handler(environ, start_response):
    pass

@get()
def testFC(data):
    # 先获取配置中心url
    centerConfig = getConfByName(CONF_CENTER_NAME)
    # 获取配置
    myConf = getConfigFromConfCenter(centerConfig['url'], ['mysql', 'postgresql'], centerConfig['pwd'])
    return ResponseEntity.ok(myConf.text)
