import json
import logging

from AliFCWeb.fcorm import Orm, Example
from AliFCWeb import fcIndex, get, post, put, delete, mysqlConn, ResponseEntity

_log = logging.getLogger()
_conn = mysqlConn


@fcIndex(debug=True)
def handler(environ, start_response):
    pass


@post()
def testFC(data):
    '''
    '''
    orm = Orm(_conn, 'user')
    userId = orm.insertData(data)
    return ResponseEntity.ok('新增用户成功，你的id：{}'.format(userId))