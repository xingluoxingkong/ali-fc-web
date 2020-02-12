import json
import logging
from .fcutils import getConfig, getConfigFromConfCenter

__all__ = ['CONF_CENTER_NAME', 'MY_SQL_CONF_FILE_NAME',
           'POSTGRE_SQL_CONF_FILE_NAME',
           'REDIS_CONF_FILE_NAME', 'RSA_PUBLIC_KEY_FILE_NAME',
           'RSA_PRIVATE_KEY_FILE_NAME', 'FC_ENVIRON',
           'FC_START_RESPONSE', 'getConfByName',
           'init']

_log = logging.getLogger()

# 配置中心参数名
CONF_CENTER_NAME = 'conf_center'

# mysql配置文件名字
MY_SQL_CONF_FILE_NAME = 'mysql'

# postgresql配置文件名
POSTGRE_SQL_CONF_FILE_NAME = 'postgresql'

# redis配置文件名
REDIS_CONF_FILE_NAME = 'redis'

# 公钥
RSA_PUBLIC_KEY_FILE_NAME = 'rsa_public_key'
# 私钥
RSA_PRIVATE_KEY_FILE_NAME = 'rsa_private_key'

FC_ENVIRON = 'environ'
FC_START_RESPONSE = 'start_response'

_dict = {}


def getConfByName(confName):
    ''' 获取配置
    --
    '''
    global _dict
    if confName in _dict:
        return _dict[confName]
    elif CONF_CENTER_NAME in _dict:
        confCenter = _dict[CONF_CENTER_NAME]
        res = getConfigFromConfCenter(
            confCenter['url'], confName, confCenter.get('pwd', None))
        data = res.text
        try:
            data = json.loads(data)
        except Exception as e:
            data = str(data)

        if res.status_code != 200:
            raise Exception('从配置中心获取{}失败！失败原因：{}'.format(confName,  data))

        _dict[confName] = data
        return data
    else:
        raise Exception('获取配置{}失败'.format(confName))


def init(environ, start_response):
    ''' 设置环境变量, 设置配置中心url和pwd
    '''
    global _dict
    _dict[FC_ENVIRON] = environ
    _dict[FC_START_RESPONSE] = start_response

    try:
        # 加载用户配置文件
        userConf = getConfig('application')
        _dict.update(userConf)
    except Exception as e:
        _log.info('用户未配置application文件，采用默认配置文件')

    # 取出配置中心url和密码，默认url：config/config/，默认无需密码
    confCenter = _dict.get(CONF_CENTER_NAME, {'url': 'config/config/'})

    # 如果不是以http开头，则从environ中拼接完整的url地址
    if not confCenter['url'].startswith('http'):
        httpHost = environ['HTTP_HOST'] if 'HTTP_HOST' in environ else environ['REMOTE_ADDR']
        confCenter['url'] = 'https://{}/2016-08-15/proxy{}'.format(
            httpHost, confCenter['url'] if confCenter['url'].startswith('/') else '/' + confCenter['url'])

    _dict[CONF_CENTER_NAME] = confCenter
