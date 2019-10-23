import hashlib
from random import Random 


def createPwd(password, salt):
    ''' 生成加密密码
    :param password: 密码
    :param salt: 盐值
    '''
    md5_1 = hashlib.md5(password.encode('utf-8'))
    res_1 = md5_1.hexdigest()
    md5_2 = hashlib.md5((res_1 + salt).encode('utf-8'))
    res_2 = md5_2.hexdigest()
    return res_2
    
def createSalt(length = 6):
    ''' 生成由6位随机大小写字母、数字组成的salt值
    '''
    salt = ''  
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'  
    len_chars = len(chars) - 1  
    random = Random()  
    for i in range(length):  
        # 每次从chars中随机取一位  
        salt += chars[random.randint(0, len_chars)]  
    return salt
