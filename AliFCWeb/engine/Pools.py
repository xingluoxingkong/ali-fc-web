import json
import threading

from .PooledDB import PooledDB

from AliFCWeb.constant import getConfByName, FC_ENVIRON, CONF_CENTER_NAME, MY_SQL_CONF_FILE_NAME, POSTGRE_SQL_CONF_FILE_NAME


class Pool(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Pool, "_instance"):
            with Pool._instance_lock:
                if not hasattr(Pool, "_instance"):
                    Pool._instance = object.__new__(cls)
        return Pool._instance

    def __init__(self, *args, **kw):
        self._kw = kw

    def conn(self):
        ''' 从连接池获取一个连接
        '''
        if not hasattr(self, 'POOL'):
            with Pool._instance_lock:
                if not hasattr(self, 'POOL'):
                    self._connect()
        return self.POOL.connection()

    def _connect(self):
        raise Exception('请继承并覆写此方法')


class PostgrePool(Pool):
    def __init__(self, *args, **kw):
        ''' 获取配置中心数据。
            需要有一个application.py文件，该文件配置了配置中心的url,pwd。
            配置中心配置名为：conf_center，无默认值，必须配置。
            sql配置文件名为'mysql'
        '''
        self.conf = kw

    def _connect(self):
        if hasattr(self, 'POOL'):
            return
        from AliFCWeb.constant import getConfByName, FC_ENVIRON, CONF_CENTER_NAME, MY_SQL_CONF_FILE_NAME
        confCenter = getConfByName(CONF_CENTER_NAME)

        from AliFCWeb.fcutils import getConfigFromConfCenter
        res = getConfigFromConfCenter(
            confCenter['url'], MY_SQL_CONF_FILE_NAME, confCenter['pwd'])
        if res.status_code != 200:
            raise Exception('读取配置中心失败！')
        data = json.loads(res.text)

        data.update(self.conf)

        import psycopg2
        from psycopg2.extras import RealDictCursor
        data['creator'] = psycopg2
        data['cursor_factory'] = RealDictCursor
        # data['host'] = data.pop('url')
        data['port'] = data.get('port', 5432)
        # data['user'] = data.pop('username')
        # data['database'] = data.pop('dbname')

        self.POOL = PooledDB(**data)


class MysqlPool(Pool):

    def __init__(self, *args, **kw):
        ''' 获取配置中心数据。
            需要有一个application.py文件，该文件配置了配置中心的url,pwd。
            配置中心配置名为：conf_center，无默认值，必须配置。
            sql配置文件名为'mysql'
        '''
        self.conf = kw

    def _connect(self):
        if hasattr(self, 'POOL'):
            return
        from AliFCWeb.constant import getConfByName, FC_ENVIRON, CONF_CENTER_NAME, MY_SQL_CONF_FILE_NAME
        confCenter = getConfByName(CONF_CENTER_NAME)

        from AliFCWeb.fcutils import getConfigFromConfCenter
        res = getConfigFromConfCenter(
            confCenter['url'], MY_SQL_CONF_FILE_NAME, confCenter['pwd'])
        if res.status_code != 200:
            raise Exception('读取配置中心失败！')
        data = json.loads(res.text)

        data.update(self.conf)

        import pymysql
        data['creator'] = pymysql
        data['cursorclass'] = pymysql.cursors.DictCursor
        data['port'] = data.get('port', 3306)

        self.POOL = PooledDB(**data)
