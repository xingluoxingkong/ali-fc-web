######################################
#
# 进行jwt加解密工具
#
######################################
import jwt
import time

__all__ = ['encode', 'decode', 'timeLaterForDay',
           'timeLaterForHour', 'timeLater']


def encode(payload, priv_key):
    ''' 加密
    :param payload:有效载荷
    :param priv_key:私钥
    '''
    encoded = jwt.encode(payload, priv_key, algorithm='RS256')
    return str(encoded, encoding='utf-8')


def decode(encoded_str, pub_key):
    ''' 解密
    :param encoded_str:加密后的文件
    :param pub_key:公钥
    '''
    try:
        info = jwt.decode(encoded_str, pub_key, algorithm='RS256')
        return info
    except Exception as e:
        return None


def timeLaterForDay(day=30):
    """ 生成签名过期时间，默认一个月
    """
    return int(time.time() + 3600 * 24 * day)


def timeLaterForHour(hour=0.5):
    """ 生成签名过期时间，默认半小时
    """
    return int(time.time() + 3600 * hour)


def timeLater(num=0.5, unit='hour'):
    ''' 生成签名时间，自定义时间单位，默认半小时
    :param num:时长
    :param unit:时间单位， hour：小时， day：日， month：月， year：年
    '''
    if unit == 'hour':
        return int(time.time() + 3600 * num)
    elif unit == 'day':
        return int(time.time() + 3600 * 24 * num)
    elif unit == 'month':
        return int(time.time() + 3600 * 24 * 30 * num)
    elif unit == 'year':
        return int(time.time() + 3600 * 24 * 30 * 12 * num)
    else:
        return -1
