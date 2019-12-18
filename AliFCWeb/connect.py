import json
import pymysql
from .fcutils import getData, getConfig
from .sign import DBSign, RedisSign
from .constant import getConfByName

__all__ = ['dbConn', 'redisConn']


@DBSign
def dbConn():
    """ 获取数据库连接
    --
    """
    pass


@RedisSign
def redisConn():
    """ 获取redis连接
    --
    """
    pass
