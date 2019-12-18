import oss2

__all__ = ['OSSUtils', 'ShanghaiOSS',
           'HangzhouOSS', 'QingdaoOSS',
           'BeijingOSS', 'ZhangjiakouOSS',
           'HuhehaoteOSS', 'ShenzhenOSS',
           'ChengduOSS', 'HongkongOSS']

_SHANGHAI = 'https://oss-cn-shanghai.aliyuncs.com'
_HANGZHOU = 'https://oss-cn-hangzhou.aliyuncs.com'
_QINGDAO = 'https://oss-cn-qingdao.aliyuncs.com'
_BEIJING = 'https://oss-cn-beijing.aliyuncs.com'
_ZHANGJIAKOU = 'https://oss-cn-zhangjiakou.aliyuncs.com'
_HUHEHAOTE = 'https://oss-cn-huhehaote.aliyuncs.com'
_SHENZHEN = 'https://oss-cn-shenzhen.aliyuncs.com'
_CHENGDU = 'https://oss-cn-chengdu.aliyuncs.com'
_HONGKONG = 'https://oss-cn-hongkong.aliyuncs.com'

class OSSUtils(object):
    """ 封装OSS中的常用操作
    """
    def __init__(self, accessKeyId, accessKeySecret, bucketName, endpoint):
        """ 
        :param accessKeyId: 阿里云accessKeyId
        :param accessKeySecret: 阿里云accessKeySecret
        :param bucketName: bucket名字
        """
        super(OSSUtils, self).__init__()
        auth = oss2.Auth(accessKeyId, accessKeySecret)
        self.bucket = oss2.Bucket(auth, endpoint, bucketName)
    
    def getFileList(self, path = ''):
        """ 获取配置列表
        :param dirName: 父路径
        :return status：成功返回200，失败返回错误码
        :return files：成功返回配置列表，失败返回错误信息
        """
        files = []
        for obj in oss2.ObjectIterator(self.bucket, path, ''):
            if obj.key != path and obj.key != path + '/':
                files.append(obj.key)
        return files
    
    def getFileByName(self, path):
        """ 获取文件内容,utf-8编码
        :param path: 文件路径
        :return 成功返回数据，失败返回None
        """
        try:
            remote_stream = self.bucket.get_object(path)
            data = str(remote_stream.read(), encoding = 'utf-8')
            return data
        except Exception as err:
            return None
    
    def updateFile(self, data, path):
        """ 修改或者新增文件
        :param data: 文件内容
        :param path: 文件路径
        """
        return self.bucket.put_object(path, data)

class ShanghaiOSS(OSSUtils):
    def __init__(self, accessKeyId, accessKeySecret, bucketName):
        super(ShanghaiOSS, self).__init__(accessKeyId, accessKeySecret, bucketName, _SHANGHAI)
class HangzhouOSS(OSSUtils):
    def __init__(self, accessKeyId, accessKeySecret, bucketName):
        super(HangzhouOSS, self).__init__(accessKeyId, accessKeySecret, bucketName, _HANGZHOU)
class QingdaoOSS(OSSUtils):
    def __init__(self, accessKeyId, accessKeySecret, bucketName):
        super(QingdaoOSS, self).__init__(accessKeyId, accessKeySecret, bucketName, _QINGDAO)
class BeijingOSS(OSSUtils):
    def __init__(self, accessKeyId, accessKeySecret, bucketName):
        super(BeijingOSS, self).__init__(accessKeyId, accessKeySecret, bucketName, _BEIJING)
class ZhangjiakouOSS(OSSUtils):
    def __init__(self, accessKeyId, accessKeySecret, bucketName):
        super(ZhangjiakouOSS, self).__init__(accessKeyId, accessKeySecret, bucketName, _ZHANGJIAKOU)
class HuhehaoteOSS(OSSUtils):
    def __init__(self, accessKeyId, accessKeySecret, bucketName):
        super(HuhehaoteOSS, self).__init__(accessKeyId, accessKeySecret, bucketName, _HUHEHAOTE)
class ShenzhenOSS(OSSUtils):
    def __init__(self, accessKeyId, accessKeySecret, bucketName):
        super(ShenzhenOSS, self).__init__(accessKeyId, accessKeySecret, bucketName, _SHENZHEN)
class ChengduOSS(OSSUtils):
    def __init__(self, accessKeyId, accessKeySecret, bucketName):
        super(ChengduOSS, self).__init__(accessKeyId, accessKeySecret, bucketName, _CHENGDU)
class HongkongOSS(OSSUtils):
    def __init__(self, accessKeyId, accessKeySecret, bucketName):
        super(HongkongOSS, self).__init__(accessKeyId, accessKeySecret, bucketName, _HONGKONG)
