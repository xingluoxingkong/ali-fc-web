import json
import threading

from .PooledDB import PooledDB

from AliFCWeb.constant import getConfByName, FC_ENVIRON, CONF_CENTER_NAME, MY_SQL_CONF_FILE_NAME, POSTGRE_SQL_CONF_FILE_NAME


class Pool(object):
    _instance_lock = threading.Lock()

    def __init__(self,  *args, **kw):
        super().__init__(*args, **kw)

    def __new__(cls, *args, **kwargs):
        if not hasattr(Pool, "_instance"):
            with Pool._instance_lock:
                if not hasattr(Pool, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Pool._instance
    
    def conn(self):
        ''' 从连接池获取一个连接
        '''
        return self.POOL.connection()


class MysqlPool(object):

    def __init__(self, *args, **kw):
        ''' 获取配置中心数据。
            需要有一个application.py文件，该文件配置了配置中心的url,pwd。
            配置中心配置名为：conf_center，无默认值，必须配置。
            sql配置文件名为'mysql'
        '''

        from AliFCWeb.constant import getConfByName, FC_ENVIRON, CONF_CENTER_NAME, MY_SQL_CONF_FILE_NAME
        confCenter = getConfByName(CONF_CENTER_NAME)

        from AliFCWeb.fcutils import getConfigFromConfCenter
        res = getConfigFromConfCenter(
            confCenter['url'], MY_SQL_CONF_FILE_NAME, confCenter['pwd'])
        if res.status_code != 200:
            raise Exception('读取配置中心失败！')
        data = json.loads(res.text)

        data.update(kw)

        import pymysql
        data['creator'] = pymysql
        data['cursorclass'] = pymysql.cursors.DictCursor

        self.POOL = PooledDB(**data)
        super().__init__(*args, **kw)

    def conn(self):
        ''' 从连接池获取一个连接
        '''
        return self.POOL.connection()
