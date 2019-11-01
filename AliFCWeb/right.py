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
from .connect import getDB
from .constant import getConfByName, RSA_PRIVATE_KEY_FILE_NAME, RSA_PUBLIC_KEY_FILE_NAME, getEnviron, FC_ENVIRON, FC_START_RESPONSE
from fcutils import getConfig, getDataForStr, decode, timeLater, encode

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
    environ = getEnviron(FC_ENVIRON)
    # 验证头信息
    if 'HTTP_3RD_SESSION' not in environ:
        return None
    
    http3RdSession = environ['HTTP_3RD_SESSION'].replace('\\n', '\n')
    return decode(http3RdSession, getConfByName(RSA_PUBLIC_KEY_FILE_NAME))

def getPayloadFromHeader():
    ''' 获取头部的token里的具体内容，本地解码，不验证是否可靠
    --
    '''
    environ = getEnviron(FC_ENVIRON)
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
    if payload['keep'] == 1:
        exp = timeLater(1, 'month')
        payload['exp'] = exp
        return payload
    else:
        exp = timeLater(0.5, 'hour')
        payload['exp'] = exp
        return payload

def authRight(token):
    ''' 权限验证，成功返回True，失败返回False
    '''
    environ = getEnviron(FC_ENVIRON)
    requestUri = environ['fc.request_uri'] 
    conn = getDB.replace(environ)
    cursor = conn.cursor()
    # seller_user, sellerId, roles, keep
    if token == None or 'roles' not in token:
        return False
    fcInterfaceURL = requestUri.split('proxy')[1].replace('.LATEST', '')
    if '?' in fcInterfaceURL:
        index = fcInterfaceURL.rfind('?')
        fcInterfaceURL = fcInterfaceURL[:index]
    
    roles = ','.join(str(r['id']) for r in token['roles'])
    # 获取该用户所有角色支持的接口集合
    sql = '''SELECT interface FROM ly_auth_interface WHERE id IN (
        SELECT interface_id FROM ly_auth_access_interface WHERE access_id IN (
            SELECT access_id FROM ly_auth_role_access WHERE role_id IN (%s))) AND `delete`="0"''' % roles
    cursor.execute(sql)
    roleUrls = cursor.fetchall()
    if roleUrls == None:
        return False
    cursor.close()
    interfaces = [rurl['interface'] for rurl in roleUrls]

    return fcInterfaceURL in interfaces

def getBodyAsJson():
    ''' 获取json格式的请求体
    '''
    environ = getEnviron(FC_ENVIRON)
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    return json.loads(environ['wsgi.input'].read(request_body_size)) if request_body_size > 0 else None

def getBodyAsStr():
    ''' 获取string格式的请求体
    '''
    environ = getEnviron(FC_ENVIRON)
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    return environ['wsgi.input'].read(request_body_size)
    
def encodeToken(data):
    ''' 加密token
    格式：header.payload.signature
    :param data 签名参数
    :return 成功返回加密值，失败返回None
    '''
    token_value = encode(data, getConfByName(RSA_PRIVATE_KEY_FILE_NAME))
    
    return token_value
