from .response import ResponseEntity

def autoRollback(db, log = None, debug = False):
    ''' 数据库操作出错自动回退，操作成功自动提交
    --
        @param db 数据库连接
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                res = func(*args, **kw)
                db.commit()
                return res
            except Exception as e:
                db.rollback()
                if log:
                    log.error()
                if debug:
                    return ResponseEntity.badRequest('发生错误:{}'.format(e))
                else:
                    return ResponseEntity.badRequest('操作失败，请联系管理员查看日志!')
        return wrapper
    return decorator