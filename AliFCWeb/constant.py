# 配置文件地址
CONF_HOST = 'https://1837732264572668.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/ly-config/getConfigByName/'

# mysql配置文件名字
SQL_CONF_FILE_NAME = 'ly_common_sql.json'

# redis配置文件名
REDIS_CONF_FILE_NAME = 'ly_common_redis.json'

# 导游微信配置文件名
WX_GUIDE_FILE_NAME = 'ly_common_wx_guide.json'

# 游客微信配置文件名
WX_USER_FILE_NAME = 'ly_common_wx.json'

# 公钥
RSA_PUBLIC_KEY_FILE_NAME = 'rsa_public_key.pem'
# 密钥
RSA_PRIVATE_KEY_FILE_NAME = 'rsa_private_key.pem'

# 微信open_Id请求地址
CODE2SESSION_HOST = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code'

# 自增主键
AUTO_INCREMENT_KEYS = 'AUTO_INCREMENT'
# 默认主键名
PRIMARY_KEY = 'id'