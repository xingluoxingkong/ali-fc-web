
from .sign import Sign
class MysqlSign(Sign):
    def __init__(self, func, *args, **kw):
        ''' 获取配置中心数据。
            需要有一个application.py文件，该文件配置了配置中心的url,pwd。
            配置中心配置名为：conf_center，无默认值，必须配置。
            sql配置文件名为'mysql'
        '''
        super().__init__(func, *args, **kw)
    
    def replace(self):
        from AliFCWeb.constant import getConfByName, FC_ENVIRON, CONF_CENTER_NAME, MY_SQL_CONF_FILE_NAME
        confCenter = getConfByName(CONF_CENTER_NAME)

        from AliFCWeb.fcutils import getConfigFromConfCenter
        res = getConfigFromConfCenter(confCenter['url'], MY_SQL_CONF_FILE_NAME, confCenter['pwd'] )
        if res.status_code != 200:
            raise Exception('读取配置中心失败！')
        data = json.loads(res.text)
        
        import pymysql
        conn = pymysql.connect(data['url'], data['username'], data['password'], data['database'], 
                                charset = data['charset'], cursorclass=pymysql.cursors.DictCursor)
        return conn
