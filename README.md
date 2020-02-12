## 一、安装
``` shell
# 本地安装
pip install AliFCWeb
# fun安装
fun install --save --runtime python3 --package-type pip AliFCWeb
```

## 二、快速入门
### 本地配置fun
由于AliFCWeb是第三方库，所以需要自己上传，为了使用方便，我们使用阿里云官方调试工具fun进行代码编写和调试。
- 安装fun，安装教程参考[官方文档](https://github.com/alibaba/funcraft/blob/master/docs/usage/installation-zh.md?spm=a2c4g.11186623.2.18.30a8130772dyyb&file=installation-zh.md)
- 配置fun环境
    - 配置方法1：在命令台键入 fun config，然后按照提示，依次配置 Account ID、Access Key Id、Secret Access Key、 Default Region Name
    - 配置方法2：在C:\Users\当前用户\.fcli文件夹下创建config.yaml文件并输入以下内容（注意将其中的配置替换成你自己的配置）
    ```yaml
    endpoint: 'https://AccountID.RegionName.fc.aliyuncs.com'
    api_version: '2016-08-15'
    access_key_id: AccessKeyId
    access_key_secret: SecretAccessKey
    security_token: ''
    debug: false
    timeout: 10
    retries: 3
    sls_endpoint: RegionName.fc.aliyuncs.com
    report: true
    ```
### 编写HelloWorld
import logging
from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
import json

def authTest(environ):
    return False

@fcIndex(auth = authTest)
def handler(environ, start_response):
   pass

@get('/demo/text-application/{id}')
def testGet(id):
    return ResponseEntity.ok('收到GET请求，请求内容%d' % id)

@post()
def testPost(user):
    return ResponseEntity.ok('收到POST请求,请求内容%s' % user)

@put()
def testPut(user):
    return ResponseEntity.ok('收到PUT请求,请求内容%s' % user)

@delete()
def testDelete(user):
    return ResponseEntity.ok('收到DELETE请求,请求内容%s' % user)