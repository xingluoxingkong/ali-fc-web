import json
import pymysql
from .fcutils import getData, getConfig
from .sign import MysqlSign, RedisSign, PostgresqlSign
from .constant import getConfByName

__all__ = ['dbConn', 'redisConn']


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
