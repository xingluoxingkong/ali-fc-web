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
    orm = Orm(_conn, 'user')
    userId = orm.updateByPrimaryKey({'age': 20}, 1)
    user = orm.selectByPrimaeyKey(1)
    return ResponseEntity.ok(user)
