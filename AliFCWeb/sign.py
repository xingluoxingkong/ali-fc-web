import abc
import json
import pymysql
import importlib
from fcutils import getConfig, getConfigFromConfCenter

class Sign(metaclass = abc.ABCMeta):

    def __init__(self, func, *args, **kw):
        ''' 用于标记实际运行时需要被替换的方法，使用时继承该类并在replace方法中书写实际的运行方法
        --
        '''
        self.func = func
        self.args = args
        self.kw = kw

    @abc.abstractmethod
    def replace(self):
        ''' 覆盖此方法，实际运行时会调用该方法以替换掉被标记的方法
        --
        '''
        pass

class DBSign(Sign):
    def __init__(self, func, *args, **kw):
        ''' 获取配置中心数据。
            需要有一个application.py文件，该文件配置了配置中心的url,pwd。
            配置中心配置名为：conf_center，无默认值，必须配置。
            sql配置文件名为：sql_name，默认值为'sql'
        '''
        super().__init__(func, *args, **kw)
    
    def replace(self):
        '''@param environ: 函数计算环境变量
        '''
        from .constant import getEnviron, FC_ENVIRON, CONF_CENTER_NAME, SQL_CONF_FILE_NAME
        environ = getEnviron(FC_ENVIRON)
        confCenter = getEnviron(CONF_CENTER_NAME)

        res = getConfigFromConfCenter(confCenter['url'], SQL_CONF_FILE_NAME, confCenter['pwd'] )
        if res.status_code != 200:
            raise Exception('读取配置中心失败！')
        data = json.loads(res.text)
        conn = pymysql.connect(data['url'], data['username'], data['password'], data['database'], 
                                charset = data['charset'], cursorclass=pymysql.cursors.DictCursor)
        return conn

class RedisSign(Sign):
    def __init__(self, func, *args, **kw):
        ''' 获取配置中心数据。
            需要有一个application.py文件，该文件配置了配置中心的url,pwd。
            配置中心配置名为：conf_center，无默认值，必须配置。
            redis配置文件名为：redis_name，默认值为'redis'
        '''
        super().__init__(func, *args, **kw)
    
    def replace(self):
        '''@param environ: 函数计算环境变量
        '''
        from .constant import getEnviron, FC_ENVIRON, CONF_CENTER_NAME, SQL_CONF_FILE_NAME
        environ = getEnviron(FC_ENVIRON)
        confCenter = getEnviron(CONF_CENTER_NAME)

        res = getConfigFromConfCenter(confCenter['url'], SQL_CONF_FILE_NAME, confCenter['pwd'] )
        if res.status_code != 200:
            raise Exception('读取配置中心失败！')
        data = json.loads(res.text)
        import redis
        conn = redis.Redis(host=data['host'], port=data['port'], db=0, password=data['password'])
        return conn