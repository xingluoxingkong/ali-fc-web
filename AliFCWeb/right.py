###############################################################
#
# 权限鉴定
#
#
#
###############################################################
import json
import base64
import logging
from .fcutils import getConfig, getDataForStr, decode, timeLater, encode, xml2dict
from .constant import getConfByName, RSA_PRIVATE_KEY_FILE_NAME, RSA_PUBLIC_KEY_FILE_NAME, getConfByName, FC_ENVIRON, FC_START_RESPONSE

__all__ = ['isLogin', 'getTokenFromHeader',
           'getPayloadFromHeader', 'updateToken',
           'encodeToken']

_log = logging.getLogger()


def isLogin(oldPayload):
    ''' 验证是否已登录，登录则更新token
    --
        @return 错误返回 False
        @return 成功返回 True
    '''
    if oldPayload == None:
        return False
    return True


def getTokenFromHeader():
    ''' 验证是否存在3RDSession，存在返回解码的值失败返回None
    --
    '''
    environ = getConfByName(FC_ENVIRON)
    # 验证头信息
    if 'HTTP_3RD_SESSION' not in environ:
        return None

    http3RdSession = environ['HTTP_3RD_SESSION'].replace('\\n', '\n')
    return decode(http3RdSession, getConfByName(RSA_PUBLIC_KEY_FILE_NAME))


def getPayloadFromHeader():
    ''' 获取头部的token里的具体内容，本地解码，不验证是否可靠
    --
    '''
    environ = getConfByName(FC_ENVIRON)
    # 验证头信息
    if 'HTTP_3RD_SESSION' not in environ:
        return None

    http3RdSession = environ['HTTP_3RD_SESSION'].replace('\\n', '\n')
    strPayload = {}

    ss = http3RdSession.split('.')[1]
    if len(ss) % 4:
        # not a multiple of 4, add padding:
        ss += '=' * (4 - len(ss) % 4)
    strPayload = str(base64.b64decode(ss, '-_'), "utf-8")
    return json.loads(strPayload)


def updateToken(payload):
    ''' 更新token
    '''
    # 一个月
    keep = payload.get('keep', 0.5)
    unit = payload.get('unit', 'hour')
    payload['exp'] = timeLater(keep, unit)
    return payload

def encodeToken(data):
    ''' 加密token
    格式：header.payload.signature
    :param data 签名参数
    :return 成功返回加密值，失败返回None
    '''
    data['exp'] = timeLater(data.pop('keep', 0.5), 'hour')
    token_value = encode(data, getConfByName(RSA_PRIVATE_KEY_FILE_NAME))
    return token_value


