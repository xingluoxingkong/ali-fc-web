import json
from .fcutils import getData, getConfig
from .sign import MysqlSign, RedisSign, PostgresqlSign
from .constant import getConfByName

__all__ = ['mysqlConn', 'redisConn', 'postgresqlConn']


@MysqlSign
def mysqlConn():
    """ 获取mysql数据库连接
    --
    """
    pass


@RedisSign
def redisConn():
    """ 获取redis连接
    --
    """
    pass

@PostgresqlSign
def postgresqlConn():
    ''' 获取postgresql数据库连接
    --
    '''
    pass
