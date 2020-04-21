import json
import threading

from .PooledDB import PooledDB

from AliFCWeb.constant import getConfByName, FC_ENVIRON, CONF_CENTER_NAME, MY_SQL_CONF_FILE_NAME, POSTGRE_SQL_CONF_FILE_NAME


class CreatePool:

    def __init__(self, sql_name, **kw):
        ''' 使用的数据库名字，目前支持mysql和postgresql
        --
            @param kw 连接参数，可选以下参数:
                maxconnections:连接池允许的最大连接数，0和None表示不限制连接数
                mincached:初始化时，链接池中至少创建的空闲的链接，0表示不创建
                maxcached:链接池中最多闲置的链接，0和None不限制
                maxshared:链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
                blocking:连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                maxusage:一个链接最多被重复使用的次数，None表示无限制
                setsession:开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
                ping:MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
                host:服务器地址
                port：端口
                user：账户
                password：密码
                database：数据库名
                charset：字符集
        '''
        self._sql_name = sql_name
        self._kw = kw

    def conn(self):
        if self._sql_name == 'mysql':
            pool = MysqlPool(**self._kw)
        elif self._sql_name == 'postgresql':
            pool = PostgrePool(**self._kw)

        return pool.conn()


class Pool(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Pool, "_instance"):
            with Pool._instance_lock:
                if not hasattr(Pool, "_instance"):
                    Pool._instance = object.__new__(cls)
        return Pool._instance

    def conn(self):
        ''' 从连接池获取一个连接
        '''
        return self.POOL.connection()


class PostgrePool(Pool):
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
        data['port'] = data.get('port', 3306)

        self.POOL = PooledDB(**data)
