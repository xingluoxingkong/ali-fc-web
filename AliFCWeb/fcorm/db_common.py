import json
import logging
import functools

import pymysql

from AliFCWeb.connect import dbConn
from AliFCWeb.fcorm import Orm, Example
from AliFCWeb.response import ResponseEntity
from AliFCWeb.fcweb import fcIndex, get, post, put, delete

    
_log = logging.getLogger()
_conn = dbConn
_PWD = None
_PRIVATE_TABLE = []

__all__ = ['dbCommon']

def dbCommon(pwd = '123456', privateTables = []):
    global _PWD, _PRIVATE_TABLE
    _PWD = pwd
    _PRIVATE_TABLE = privateTables
    def decorator(func):
        def wrapper(*args, **kw):
            environ = args[0]
            start_response = args[1]
            environ['fc.context'].function.handler = 'AliFCWeb/fcorm/db_common'
            res = _index(environ, start_response)
            return res
        return wrapper
    return decorator

@fcIndex()
def _index(environ, start_response):
    pass

@get()
def _get(params):
    ''' 获取数据库数据
    '''
    # 表名
    model = params.get('model', None)
    # id
    tableId = params.get('id', 0)
    # 主键名
    idName = params.get('id_name', 'id')
    # 排除字段
    exclude = params.get('exclude').split(
        ',') if 'exclude' in params else None
    # 查询字段
    fields = params.get('fields').split(
        ',') if 'fields' in params else None
    # 页码
    page = params.get('page', 0)
    # 页长
    pageNum = params.get('page_num', 10)
    # 查询条件
    where = params.get('where', '')
    # 跳过鉴权密码
    pwd = str(params.get('pwd', ''))
    # delete字段，没有则不过滤delete
    delete = params.get('delete', '')
    # 是否有delete字段
    deleteColumn = False

    if not model:
        return ResponseEntity.badRequest('请输入你要获取的资源名')

    if _PWD and pwd != _PWD:
        return ResponseEntity.badRequest('密码错误')
    
    if model in _PRIVATE_TABLE:
        return ResponseEntity.badRequest('当前表禁止此操作')

    orm = Orm(_conn, model, idName)
    res = orm.selectAllBySQL(
        'SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = "{}"'.format(model))
    columns = []
    for r in res:
        f = r['COLUMN_NAME']
        if exclude and f in fields:
            pass
        elif f == 'delete':
            deleteColumn = True
        elif (fields and f in fields) or not fields:
            columns.append(f)

    if columns:
        orm.setSelectProperties(columns)

    if tableId > 0:  # 按主键查询
        res = None
        if where:
            example = Example().whereFromStr(
                where).andEqualTo({idName: tableId})
            res = orm.selectByExample(example)
        else:
            res = orm.selectByPrimaeyKey(tableId)

        if res:
            return ResponseEntity.ok(res)
        else:
            return ResponseEntity.notFound('没有需要的数据')
    elif page:  # 分页查询
        res = None
        if where:
            example = Example().whereFromStr(where)
            if deleteColumn and delete:
                example.andEqualTo({'delete': delete})
            res = orm.selectPageByExample(example, page, pageNum)
        else:
            res = orm.selectPageAll(page, pageNum)

        if not res:
            return ResponseEntity.notFound('没有需要的数据')

        n, d = res
        return ResponseEntity.ok(d).setNum(n)
    else:   # 查询所有
        res = None
        if where:
            example = Example().whereFromStr(where)
            if deleteColumn and delete:
                example.andEqualTo({'delete': delete})
            res = orm.selectByExample(example)
        else:
            res = orm.selectAll()

        if res:
            return ResponseEntity.ok(res)
        else:
            return ResponseEntity.notFound('没有需要的数据')

@post()
def _post(params):
    ''' 添加数据库数据
    '''
    # 表名
    model = params.get('model', None)

    # 主键名
    idName = params.get('id_name', 'id')
    # 数据
    data = params.get('data', None)
    # 跳过鉴权密码
    pwd = str(params.get('pwd', ''))
    if not model:
        return ResponseEntity.badRequest('请输入你要操作的资源名')

    if _PWD and pwd != _PWD:
        return ResponseEntity.badRequest('密码错误')
    
    if model in _PRIVATE_TABLE:
        return ResponseEntity.badRequest('当前表禁止此操作')

    orm = Orm(_conn, model, idName)
    res = orm.insertData(data)
    if res >= 0:
        return ResponseEntity.ok('数据写入成功！')
    else:
        return ResponseEntity.badRequest('数据写入失败！')

@put()
def _put(params):
    ''' 更新数据库数据
    '''
    # 表名
    model = params.get('model', None)
    # id
    tableId = params.get('id', 0)
    # 主键名
    idName = params.get('id_name', 'id')
    # 数据
    data = params.get('data', None)
    # 跳过鉴权密码
    pwd = str(params.get('pwd', ''))

    if not model:
        return ResponseEntity.badRequest('请输入你要操作的资源名')

    if tableId == 0:
        return ResponseEntity.badRequest('没有提供id')

    if _PWD and pwd != _PWD:
        return ResponseEntity.badRequest('密码错误')
    
    if model in _PRIVATE_TABLE:
        return ResponseEntity.badRequest('当前表禁止此操作')

    orm = Orm(_conn, model, idName)
    res = orm.updateByPrimaryKey(data, tableId)
    if res:
        return ResponseEntity.ok('数据更新成功！')
    else:
        return ResponseEntity.badRequest('数据更新失败！')

@delete()
def _delete(params):
    ''' 删除数据库数据
    '''

    # 表名
    model = params.get('model', None)
    # id
    tableId = params.get('id', 0)
    # 主键名
    idName = params.get('id_name', 'id')
    # 有delete字段则更改delete的值
    delete = params.get('delete', '')
    # 跳过鉴权密码
    pwd = str(params.get('pwd', ''))
    if not model:
        return ResponseEntity.badRequest('请输入你要操作的资源名')

    if tableId == 0:
        return ResponseEntity.badRequest('没有提供id')

    if _PWD and pwd != _PWD:
        return ResponseEntity.badRequest('密码错误')
    
    if model in _PRIVATE_TABLE:
        return ResponseEntity.badRequest('当前表禁止此操作')

    orm = Orm(_conn,  model, idName)
    res = orm.selectAllBySQL(
        'SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = "{}"'.format(model))
    
    if 'delete' in res and delete:
        res = orm.updateByPrimaryKey({'delete': delete}, tableId)
    else:
        res = orm.deleteByPrimaryKey(tableId)

    if res:
        return ResponseEntity.ok('数据删除成功！')
    else:
        return ResponseEntity.badRequest('数据删除失败！')