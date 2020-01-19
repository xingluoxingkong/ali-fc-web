from .sign import Sign

class RedisSign(Sign):
    def __init__(self, func, *args, **kw):
        ''' 获取配置中心数据。
            需要有一个application.py文件，该文件配置了配置中心的url,pwd。
            配置中心配置名为：conf_center，无默认值，必须配置。
            redis配置文件名为：redis_name，默认值为'redis'
        '''
        super().__init__(func, *args, **kw)
    
    def replace(self):
        from AliFCWeb.fcutils import getConfigFromConfCenter
        from AliFCWeb.constant import getConfByName, FC_ENVIRON, CONF_CENTER_NAME, REDIS_CONF_FILE_NAME
        confCenter = getConfByName(CONF_CENTER_NAME)

        res = getConfigFromConfCenter(confCenter['url'], REDIS_CONF_FILE_NAME, confCenter['pwd'] )
        if res.status_code != 200:
            raise Exception('读取配置中心失败！')
        data = json.loads(res.text)
        
        import redis
        conn = redis.Redis(host=data['host'], port=data['port'], db=0, password=data['password'])
        return conn