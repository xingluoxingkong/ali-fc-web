import json
import pymysql
import logging
from AliFCWeb import fcIndex, ResponseEntity, get, post, put, delete, getDB, getTokenFromHeader, getPayloadFromHeader
from fcorm import Orm

_log = logging.getLogger()
_db = getDB

@fcIndex(debug = True)
def handler(environ, start_response):
    pass

@get(login=True)
def getTest(data):
    testOrm = Orm(_db, 'ly_user')
    res = testOrm.selectAll()
    return ResponseEntity.ok(res)



