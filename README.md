## 一、安装
``` shell
# 本地安装
pip install AliFCWeb
# fun安装
fun install --save --runtime python3 --package-type pip AliFCWeb
```

## 二、快速入门
### 1. 本地配置fun
由于AliFCWeb是第三方库，所以需要自己上传，为了使用方便，我们使用阿里云官方调试工具fun进行代码编写和调试。
- 安装fun，安装教程参考[官方文档](https://github.com/alibaba/funcraft/blob/master/docs/usage/installation-zh.md?spm=a2c4g.11186623.2.18.30a8130772dyyb&file=installation-zh.md)
- 配置fun环境
    - 配置方法1：在命令台键入 fun config，然后按照提示，依次配置 Account ID、Access Key Id、Secret Access Key、 Default Region Name
    - 配置方法2：在C:\Users\当前用户\\.fcli文件夹下创建config.yaml文件并输入以下内容（注意将其中的配置替换成你自己的配置）
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
### 2. 编写HelloWorld
- 本地创建test目录，用于存放所有的demo
- 在test目录下创建demo01
- 在demo01目录下创建template.yml，内容如下：
    ```yaml
    ROSTemplateFormatVersion: '2015-09-01'
    Transform: 'Aliyun::Serverless-2018-04-03'
    Resources:
      fcweb-demo:
        Type: 'Aliyun::Serverless::Service'
        Properties:
          Description: '函数计算fcweb框架demo'
        demo01:
          Type: 'Aliyun::Serverless::Function'
          Properties:
            Description: 'HelloWorld'
            Handler: index.handler
            Runtime: python3
            CodeUri: '.'
            Timeout: 30
          Events:
            httpTrigger:
              Type: HTTP
              Properties:
                AuthType: ANONYMOUS
                Methods: 
                  - GET
                  - POST
                  - PUT
                  - DELETE
    ```
- 在demo01目录下创建index.py，代码如下:
	```python
    import json
    import logging
    from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity

    @fcIndex()
    def handler(environ, start_response):
        pass

    @get()
    def testFC(data):
        return ResponseEntity.ok('Hello World!')
	```
- 引包，控制台执行命令
	```shell
	fun install --save --runtime python3 --package-type pip AliFCWeb
	```
	![目录结构](./img//demo01/01.png)
- 上传，控制台执行命令
	```shell
	fun deploy
	```
- 进入函数计算控制台，点击执行查看运行结果
	![Hello World执行结果](./img//demo01/02.png)
## 三、获取参数
### 1. 获取地址栏参数
- 复制demo01，重命名为demo02
- 修改template.yml
	```yaml
	ROSTemplateFormatVersion: '2015-09-01'
    Transform: 'Aliyun::Serverless-2018-04-03'
    Resources:
      fcweb-demo:
        Type: 'Aliyun::Serverless::Service'
        Properties:
          Description: '函数计算fcweb框架demo'
        demo02:
          Type: 'Aliyun::Serverless::Function'
          Properties:
            Description: '获取地址栏参数'
            Handler: index.handler
            Runtime: python3
            CodeUri: '.'
            Timeout: 30
          Events:
            httpTrigger:
              Type: HTTP
              Properties:
                AuthType: ANONYMOUS
                Methods: 
                  - GET
                  - POST
                  - PUT
                  - DELETE
	```
- 修改index.py
	```python
    import json
    import logging
    
    from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
    
    @fcIndex(debug=True)
    def handler(environ, start_response):
        pass
        
    @get()
    def testFC(data):
        print('前端传来的参数：')
        print(data)
        return ResponseEntity.ok(data)
  ```
- 上传代码
	```shell
	fun deploy
	```
- 测试，在控制台随便传递几个参数
![](./img//demo02/01.png)
![](./img//demo02/02.png)
### 2. 获取body参数
- 复制demo02，重命名为demo03
- 修改template.yml文件
    ```yaml
    ROSTemplateFormatVersion: '2015-09-01'
    Transform: 'Aliyun::Serverless-2018-04-03'
    Resources:
      fcweb-demo:
        Type: 'Aliyun::Serverless::Service'
        Properties:
          Description: '函数计算fcweb框架demo'
        demo03:
          Type: 'Aliyun::Serverless::Function'
          Properties:
            Description: '获取body参数'
            Handler: index.handler
            Runtime: python3
            CodeUri: '.'
            Timeout: 30
          Events:
            httpTrigger:
              Type: HTTP
              Properties:
                AuthType: ANONYMOUS
                Methods: 
                  - GET
                  - POST
                  - PUT
                  - DELETE
    ```
- 修改index.py文件
    ```python
    import json
    import logging
    
    from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
    
    @fcIndex(debug=True)
    def handler(environ, start_response):
        pass
    
    # 改为post请求
    @post()
    def testFC(data):
        print('前端传来的参数：')
        print(data)
        return ResponseEntity.ok(data)
    ```
- 上传代码
	```shell
	fun deploy
	```
- 测试执行
![](./img//demo03/01.png)
![](./img//demo03/02.png)
### 3. 获取摸板参数
- 复制demo03，重命名为demo04
- 修改template.yml文件
    ```yaml
    ROSTemplateFormatVersion: '2015-09-01'
    Transform: 'Aliyun::Serverless-2018-04-03'
    Resources:
      fcweb-demo:
        Type: 'Aliyun::Serverless::Service'
        Properties:
          Description: '函数计算fcweb框架demo'
        demo04:
          Type: 'Aliyun::Serverless::Function'
          Properties:
            Description: '获取摸板参数'
            Handler: index.handler
            Runtime: python3
            CodeUri: '.'
            Timeout: 30
          Events:
            httpTrigger:
              Type: HTTP
              Properties:
                AuthType: ANONYMOUS
                Methods: 
                  - GET
                  - POST
                  - PUT
                  - DELETE
    ```
- 修改index.py文件
    ```python
    import json
    import logging
    
    from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
    
    @fcIndex(debug=True)
    def handler(environ, start_response):
        pass
    
    @get('/demo04/{name}')
    def testFC(data):
        print('前端传来的参数：')
        print(data)
        return ResponseEntity.ok(data)
    ```
- 上传代码
	```shell
	fun deploy
	```
- 测试执行
![](./img//demo04/01.png)
![](./img//demo04/02.png)
### 4. 获取混合参数
- 复制demo04，重命名为demo05
- 修改template.yml文件
    ```yaml
    ROSTemplateFormatVersion: '2015-09-01'
    Transform: 'Aliyun::Serverless-2018-04-03'
    Resources:
      fcweb-demo:
        Type: 'Aliyun::Serverless::Service'
        Properties:
          Description: '函数计算fcweb框架demo'
        demo05:
          Type: 'Aliyun::Serverless::Function'
          Properties:
            Description: '获取混合参数'
            Handler: index.handler
            Runtime: python3
            CodeUri: '.'
            Timeout: 30
          Events:
            httpTrigger:
              Type: HTTP
              Properties:
                AuthType: ANONYMOUS
                Methods: 
                  - GET
                  - POST
                  - PUT
                  - DELETE
    ```
- 修改index.py文件
    ```python
    import json
    import logging
    
    from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
    
    @fcIndex(debug=True)
    def handler(environ, start_response):
        pass
    
    @post('/demo05/{name}')
    def testFC(data):
        print('前端传来的参数：')
        print(data)
        return ResponseEntity.ok(data)
    ```
- 上传代码
	```shell
	fun deploy
	```
- 测试执行（为了方便查看结果，此处我们使用类似postman的工具进行测试）
![](./img//demo05/01.png)
![](./img//demo05/02.png)
### 5. 使用模块作为url路径
1. 你可以新建一个 module_name.py 的py文件，那么你就可以通过http://你的url/module_name 跳转到该文件中执行相应代码
2. 你也可以新建一个叫 module_name 的文件夹，在其中新建\_\_init\_\_.py文件，那么你就可以通过http://你的ur/module_name 跳转到该文件中执行相应代码
3. PS：module_name为你取的任意名字

## 四、使用配置中心

为了解决函数计算的配置问题，提供一个默认的配置中心，可以将配置统一写在这个配置中心供其他函数调用。

### 1. 创建配置中心

创建默认的配置中心只需要以下几个步骤

- 创建函数

  - 创建config目录

  - 在config目录下创建index.py，使用configCenter装饰器装饰handler函数

    ```python
    from AliFCWeb import configCenter
    
    @configCenter()
    def handler(environ, start_response):
        pass
    ```

  - 在config目录下创建template.yml

    ```yaml
    ROSTemplateFormatVersion: '2015-09-01'
    Transform: 'Aliyun::Serverless-2018-04-03'
    Resources:
      fcweb-demo:
        Type: 'Aliyun::Serverless::Service'
        Properties:
          Description: '函数计算fcweb框架demo'
        config:
          Type: 'Aliyun::Serverless::Function'
          Properties:
            Description: '配置中心'
            Handler: index.handler
            Runtime: python3
            CodeUri: '.'
            Timeout: 30
          Events:
            httpTrigger:
              Type: HTTP
              Properties:
                AuthType: ANONYMOUS
                Methods: 
                  - GET
                  - POST
                  - PUT
                  - DELETE
    ```

  - 引入AliFCWeb包

    ```shell
    fun install --save --runtime python3 --package-type pip AliFCWeb
    ```

- 添加配置文件，配置中心只需要一个application.py的配置文件用于存放配置

  - 在config目录创建application.py文件即可，创建后结构如下：

    ![](./img/config/01.png)

### 2. 使用配置中心

- 在application.py中新增一些配置

  ```python
  mysql = {
      'url': 'localhost',
      'username': 'root',
      'password': 'fcweb',
      'charset': 'utf-8'
  }
  ```

- 向配置中心发送请求获取配置

![](./img/config/02.png)

### 3. 为配置中心设置密码

- 在配置中心的application.py文件中设置pwd的值

  ![](./img/config/03.png)

- 测试

![](./img/config/04.png)

![](./img/config/05.png)

### 4. 在其他函数计算中获取配置

- 复制前面的demo05，重命名为demo06

- 修改template.yml中的函数名为demo06

  ```yaml
  ROSTemplateFormatVersion: '2015-09-01'
  Transform: 'Aliyun::Serverless-2018-04-03'
  Resources:
    fcweb-demo:
      Type: 'Aliyun::Serverless::Service'
      Properties:
        Description: '函数计算fcweb框架demo'
      demo06:
        Type: 'Aliyun::Serverless::Function'
        Properties:
          Description: '获取配置'
          Handler: index.handler
          Runtime: python3
          CodeUri: '.'
          Timeout: 30
        Events:
          httpTrigger:
            Type: HTTP
            Properties:
              AuthType: ANONYMOUS
              Methods: 
                - GET
                - POST
                - PUT
                - DELETE
  ```

- 添加application.py文件

  ```python
  conf_center = {
      # 配置中心url，可以是全路径如：https://xxx.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/fcweb-demo/config/
      'url': '/fcweb-demo/config/',
      # 配置中心密码
      'pwd': 'abc123'
  }
  ```

- 修改index.py

  ```python
  import json
  import logging
  
  from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
  
  # 引入获取配置的方法
  from AliFCWeb import getConfByName
  
  
  @fcIndex(debug=True)
  def handler(environ, start_response):
      pass
  
  @get()
  def testFC(data):
      # 获取配置
      mysqlConf = getConfByName('mysql')
      return ResponseEntity.ok(mysqlConf)
  ```

- 验证结果

  ![](./img/demo06/01.png)

### 5. 一次性获取多个配置

上面已经用geyConfByName方法获取了mysql的配置，该方法每次会先从本地缓存寻找配置，如果没有则会去配置中心拉取。优点是使用方便，缺点是只能一次获取一个配置。如果想批量获取，可以使用getConfigFromConfCenter方法

- 复制demo06，重命名为demo07

- 修改template.yml文件

  ```yaml
  ROSTemplateFormatVersion: '2015-09-01'
  Transform: 'Aliyun::Serverless-2018-04-03'
  Resources:
    fcweb-demo:
      Type: 'Aliyun::Serverless::Service'
      Properties:
        Description: '函数计算fcweb框架demo'
      demo07:
        Type: 'Aliyun::Serverless::Function'
        Properties:
          Description: '批量获取配置'
          Handler: index.handler
          Runtime: python3
          CodeUri: '.'
          Timeout: 30
        Events:
          httpTrigger:
            Type: HTTP
            Properties:
              AuthType: ANONYMOUS
              Methods: 
                - GET
                - POST
                - PUT
                - DELETE
  ```

- 修改index.py文件

  ```python
  import json
  import logging
  
  from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
  
  from AliFCWeb import getConfByName, CONF_CENTER_NAME
  # 引入getConfigFromConfCenter方法
  # 该方法在AliFCWeb.fcutils包下
  from AliFCWeb.fcutils import getConfigFromConfCenter
  
  
  @fcIndex(debug=True)
  def handler(environ, start_response):
      pass
  
  @get()
  def testFC(data):
      # 先获取配置中心url
      centerConfig = getConfByName(CONF_CENTER_NAME)
      # 获取配置
      myConf = getConfigFromConfCenter(centerConfig['url'], ['mysql', 'postgresql'], centerConfig['pwd'])
      return ResponseEntity.ok(myConf.text)
  ```

- 测试

  - 在配置中心（/feweb-demo/config/）的application.py文件中添加postgresql的配置信息

    ```python
    postgresql = {
        'dbname': 'cofree',
        'user': 'postgres',
        'password': '123456',
        'host': 'localhost'
    }
    ```

  - 测试demo07

    ![](./img/demo07/01.png)

## 五、自定义返回格式

### 1. ResponseEntity类

在前面我们使用了ResponseEntity类进行返回，该类已经对返回结果进行了处理和封装。你可以直接new一个ResponseEntity，也可以通过内置的常用静态方法快速获取一个ResponseEntity实例，下面是**部分**内置方法

| 方法名                      | 方法说明       | 备注      |
| --------------------------- | -------------- | --------- |
| ResponseEntity.ok()         | 操作正确时返回 | 返回码200 |
| ResponseEntity.badRequest() | 错误时返回     | 返回码400 |
| ResponseEntity.notFound()   | 返回404        |           |
| ResponseEntity.serverError()| 服务器发生错误 |  返回码500   |
| ResponseEntity.unauthorized() | 权限不足 | 返回码401 |

### 2. 自定义返回格式

- 更改ResponseEntity类的build()方法即可更改返回结果，但是不建议你这做

- 更好的方式是继承ResponseEntity类并重写build()方法

  - 新建demo08，并创建index.py，template.yml文件，导入AliFCWeb库

  - 在demo08目录下新建myResponseEntity.py文件，内容如下

    ```python
    from AliFCWeb import ResponseEntity
    from AliFCWeb import getConfByName, FC_START_RESPONSE
    class MyResponseEntity(ResponseEntity):
        
        def build(self, token = None):
            # 设置请求头和请求code
            # 这一步必须要
            start_response = getConfByName(FC_START_RESPONSE)
            start_response(self.statusCode, self.response_headers)
            
            # self.res中储存了要返回的数据
            res = 'Hello ' + self.res
            return [res.encode()]
    ```

  - 修改index.py文件

    ```python
    import json
    import logging
    
    from AliFCWeb import fcIndex, get, post, put, delete
    
    # 引入自定义的ResponseEntity
    from myResponseEntity import MyResponseEntity
    
    @fcIndex(debug=True)
    def handler(environ, start_response):
        pass
    
    @get()
    def testFC(data):
        res = MyResponseEntity('200', data.get('name', 'World'))
        return res
    
    ```

  - 上传并测试

    ![](./img/demo08/01.png)

## 六、安全和权限验证

### 1. 登录验证

在get, post, put, delete四种请求方式中都可以设置login，auth和uToken三个参数

- login：验证是否登录，需要引入pyjwt包并在配置中心配置密钥，前端需要在请求头中携带3RD_SESSION参数

- auth：权限验证，传入一个方法，框架会调用该方法并将3RD_SESSION作为参数传递给该方法。返回True则代表鉴权成功，否则鉴权失败

- uToken：是否自动更新token

#### 1.1 配置密钥

在配置中心配置RSA密钥，密钥可以找在线网站生成或者使用本地工具生成

修改配置中心的application.py文件，添加密钥

```python
# 公钥
rsa_public_key = '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANyrRZamov8MEpJf70ljWNrZxa7HbUhR
mTulmdc64tQ5Cjp5iIiJefAI8l9sJdj4RGwmJVuIVZJ4inWs0QRme1MCAwEAAQ==
-----END PUBLIC KEY-----
'''

# 私钥
rsa_private_key = '''-----BEGIN PRIVATE KEY-----
MIIBVgIBADANBgkqhkiG9w0BAQEFAASCAUAwggE8AgEAAkEA3KtFlqai/wwSkl/v
SWNY2tnFrsdtSFGZO6WZ1zri1DkKOnmIiIl58AjyX2wl2PhEbCYlW4hVkniKdazR
BGZ7UwIDAQABAkEA05di9a65EmgIEtTshGk/lTJF7G6LalHb5abH2eo8ABMd3LOx
Uu080HisRqMP7lRDYIl+pIvbn3JD3qQEU/6mWQIhAO51C3nzF+kcuAtxf6UBAAil
D+IbajDyeVnnTqb5H9wlAiEA7Oc3LMviG91RuNAhhnSojkbHqJPHXvn6kqL9Xxra
pBcCIQDkHsTj3VM6h2bqS6I5UEOgAYi4XlGwkcbV4xqzUhDQoQIgVqLMA77gBq6u
dzbuO7yn87ggxh6dF7e1kjC3FjO856sCIQChK4bPN58V2shUFSvxyNbcjzljajC2
KWhUrhfmSsmj0g==
-----END PRIVATE KEY-----'''
```

#### 1.2 编写测试demo

- 新建demo09

- 创建index.py文件和application.py文件以及template.yml文件

- 在demo09目录下打开控制台执行以下命令

  ```python
  fun install --save --runtime python3 --package-type pip AliFCWeb
  fun install --save --runtime python3 --package-type pip pyjwt
  ```
  
- 修改index.py文件

  ```python
  import json
  import logging
  
  from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
  
  from AliFCWeb import getPayloadFromHeader
  
  _log = logging.getLogger()
  
  @fcIndex(debug=True)
  def handler(environ, start_response):
      pass
  
  @get()
  def testFC(data):
      password = data['password']
      if password == 123456:
          # 获取Token
          userId = data.get('id', 1)
          return ResponseEntity.ok('登录成功！').setToken({'user_id': userId})
      else:
          return ResponseEntity.unauthorized('密码错误！')
  
  @post(login=True)
  def testPost(data):
      token = getPayloadFromHeader()
      _log.info(token)
      return ResponseEntity.ok('操作成功')
  ```

#### 1.3 模拟登录
- 先用get请求模拟登录

  ![](./img/demo09/01.png)

  - 登录成功后后端会返回加密的token
  - 以后每次请求将token放在请求头（名字为3RD_SESSION）即可

- 用post请求验证登录

  - 设置post请求的login=True

    ![](./img/demo09/02.png)

  - 你可以将一些有用的信息存入token，然后在代码中使用getPayloadFromHeader()方法获取了token中的信息
  
  - 你也可以用getTokenFromHeader()方法获取token，两个方法的返回结果是完全一样的，区别在于getTokenFromHeader()需要对token进行鉴定。
  
    - 如果设置了login=True参数建议使用getPayloadFromHeader()获取，效率更高。
    - 如果没有设置login=True建议使用getTokenFromHeader()以保证安全。
### 2. 权限验证

- 复制demo09为demo10，修改template.yml文件

- 修改index文件

  ```python
  import json
  import logging
  
  from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
  
  _log = logging.getLogger()
  
  @fcIndex(debug=True)
  def handler(environ, start_response):
      pass
  
  
  @post(login=True, auth=myAuth)
  def testPost(data):
      return ResponseEntity.ok('操作成功')
  
  def myAuth(token):
      if token['user_id'] == 1:
          return True
      return False
  ```

- 上传并测试

  - 先去demo09里面获取一个id为2的token

    ![](./img/demo10/01.png)

    ![](./img/demo10/02.png)
  - 再去demo09里面获取一个id为1的token

    ![](./img/demo10/03.png)

    ![](./img/demo10/04.png)

## 七、使用数据库

- 本示例使用mysql数据库，框架同时支持postgresql，使用方法完全一样，只需要配置好对应的配置文件即可

- 你需要先去配置中心配置好mysql的参数以供使用

- 使用mysql数据库只需要使用mysqlConn获取连接即可

- 使用postgresql数据库只需要使用postgresqlConn获取连接即可

- 需要引入对应的包

  ```shell
  # mysql
  fun install --save --runtime python3 --package-type pip pymysql
  # postgresql
  fun install --save --runtime python3 --package-type pip psycopg2
  ```

- 需要引入以下两个类

  ```python
  from AliFCWeb.fcorm import Orm, Example
  ```
### 1. 准备工作

- 这里默认你已经在配置中心配置好了mysql的配置信息

  ```python
  mysql = {
      'host': '',
      'user': '',
      'password': '',
      'database': '',
      'charset': 'utf8'
  }
  ```

- 在数据库中创建一张user表用作测试

  ```sql
  CREATE TABLE `user` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) DEFAULT NULL,
    `age` int(11) DEFAULT NULL,
    PRIMARY KEY (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
  ```

### 2. 使用ORM类

#### 2.1 新增数据

- 新建demo11，配置好template.yml，application.py

- 修改index.py文件如下：

  ```python
  import json
  import logging

  from AliFCWeb.fcorm import Orm, Example
  from AliFCWeb import fcIndex, get, post, put, delete, mysqlConn, ResponseEntity
  
  _log = logging.getLogger()
  _conn = mysqlConn
  
  
  @fcIndex(debug=True)
  def handler(environ, start_response):
      pass
  
  
  @post()
  def testFC(data):
      '''
      '''
      orm = Orm(_conn, 'user')
      userId = orm.insertData(data)
      return ResponseEntity.ok('新增用户成功，你的id：{}'.format(userId))
  ```
  
- 测试结果

  ![](./img/demo11/01.png)

insertData()方法可以用于插入数据，该方法接收以下几种类型的参数（以user表为例）

| 参数一                    |           参数二            | 参数说明                                  |
| ------------------------- | ------------------------- | ----------------------------------------- |
| {'name':'张三', 'age':18} | 无     | 向数据库中插入一条数据 |
| ['name', 'age'] | [['张三', 18], ['李四', 19]] | 向数据库中插入多条数据，参数一和参数二要一一对应 |
| [{'name':'张三', 'age':18}, {'name':'李四', 'age':19}] | 无 | 向数据库中插入多条数据，每条数据的字段要一致 |
| ['name', 'age'] | {'name':'张三', 'age':18} | 参数一表示插入哪些字段，参数二表示要插入的数据，该方法可以过滤掉多余字段，比如你可以给参数二传入{'name':'张三', 'age':18, 'delete': '1'}其中的delete字段会被过滤掉，数据库依然不会报错 |

#### 2.2 修改数据

- 复制demo11为demo12，修改对应的template.yml

- 修改index.py代码

  ```python
  import json
  import logging
  
  from AliFCWeb.fcorm import Orm, Example
  from AliFCWeb import fcIndex, get, post, put, delete, mysqlConn, ResponseEntity
  
  _log = logging.getLogger()
  _conn = mysqlConn
  
  @fcIndex(debug=True)
  def handler(environ, start_response):
      pass
  
  @post()
  def testFC(data):
      orm = Orm(_conn, 'user')
      userId = orm.updateByPrimaryKey({'age': 20}, 1)
      user = orm.selectByPrimaeyKey(1)
      return ResponseEntity.ok(user)
  ```

- 运行测试

![](./img/demo12/01.png)

updateByPrimaryKey()接收两个参数

- data：要更新的数据

- id：要更新的数据的键，如果为空则会去data中寻找键。比如使用orm.updateByPrimaryKey({'age': 20, 'id':1})也是一样的效果

#### 2.3 删除数据

- 复制demo12为demo13，修改对应的template.yml

- 修改index.py代码

  ```python
  import json
  import logging
  
  from AliFCWeb.fcorm import Orm, Example
  from AliFCWeb import fcIndex, get, post, put, delete, mysqlConn, ResponseEntity
  
  _log = logging.getLogger()
  _conn = mysqlConn
  
  
  @fcIndex(debug=True)
  def handler(environ, start_response):
      pass
  
  
  @post()
  def testFC(data):
      orm = Orm(_conn, 'user')
      userId = orm.deleteByPrimaryKey(1)
      users = orm.selectAll()
      return ResponseEntity.ok(users)
  ```

- 运行测试

![](./img/demo13/01.png)

deleteByPrimaryKey()接收一个参数

- id：要更新的数据的键，
这里还使用了selectAll()方法，该方法可以返回该表中的所有数据，同时你可以看到，如果返回的数据是一个列表会自动添加num，你也可以通过ResponseEntity类的setNum()方法指定num，这在分页查询中十分有用
### 3. 使用Example类进行高级查询

前面我们已经使用过selectByPrimaeyKey()和selectAll()两个方法进行查询操作了，如果想要更高级的查询，则需要使用Example类

- 在数据库新建一张表house

  ```sql
  CREATE TABLE `house` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) DEFAULT NULL,
    `address` varchar(255) DEFAULT NULL,
    `price` int(10) DEFAULT NULL,
    PRIMARY KEY (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
  ```

- 复制demo13重命名为demo14

- 修改demo14的template.yml文件

- 修改index.py文件

  ```python
  import json
  import logging
  
  from AliFCWeb.fcorm import Orm, Example
  from AliFCWeb import fcIndex, get, post, put, delete, mysqlConn, ResponseEntity
  
  _log = logging.getLogger()
  _conn = mysqlConn
  
  
  @fcIndex(debug=True)
  def handler(environ, start_response):
      pass
  
  
  @get()
  def testFC(data):
      try:
          res = testFC1(data)
          _conn.commit()
          return res
      except Exception as e:
          _conn.rollback()
          _log.error(e)
          return ResponseEntity.badRequest(e)
  
  def testFC1(data):
      # 关闭自动提交
      userOrm = Orm(_conn, 'user', auto_commit=False)
      houseOrm = Orm(_conn, 'house', auto_commit=False)
      
      print('==============插入数据==============')
      userId = userOrm.insertData({'name':'张三', 'age':18})
      houseOrm.insertData(['user_id', 'address', 'price'], 
                          [[userId, '成都市武侯区', 100],
                           [userId, '成都市高新区', 200],
                           [userId, '北京市东城区', 300],
                           [userId, '北京市西城区', 400],
                           [userId, '北京市朝阳区', 500]])
      
      print('==============所有user数据==============')
      users = userOrm.selectAll()
      print(users)
      
      print('==============所有house数据==============')
      houses = houseOrm.selectAll()
      print(houses)
      
      print('==============所有位于成都的house数据==============')
      houses = houseOrm.selectByExample(Example().andLike('address', '成都%'))
      print(houses)
      
      print('==============所有不在成都的house数据==============')
      houses = houseOrm.selectByExample(Example().andNotLike('address', '成都%'))
      print(houses)
      
      print('==============所有user_id为1的house数据==============')
      houses = houseOrm.selectByExample(Example().andEqualTo({'user_id': 1}))
      print(houses)
      
      print('==============连接查询==============')
      userOrm.leftJoin('house', 'house.user_id=user.id')
      houses = userOrm.selectByExample(Example().andEqualTo({'price': 100}))
      print(houses)
      
      print('==============清除缓存==============')
      userOrm.clear()
      
      print('==============所有售价大于200小于400的house数据==============')
      houses = houseOrm.selectByExample(Example().andBetween('price', 200, 400))
      print(houses)
      
      print('==============所有北京的房子涨价10==============')
      houseOrm.updateByExample({'price': '+10'}, Example().andLike('address', '北京%'))
      houses = houseOrm.selectAll()
      print(houses)
      
      print('==============分页查询==============')
      num, houses = houseOrm.selectPageByExample(Example().andEqualTo({'user_id': userId}), 2, 3)
      print('符合条件的总条数：{}'.format(num))
      print('本页数据：')
      print(houses)
      
      print('==============多值查询==============')
      houses = houseOrm.selectByExample(Example().andInValues('price', [100, 200]))
      print(houses)
      
      return ResponseEntity.ok('请查看控制台日志')
  ```
### 4. 使用连接池连接数据库
```python
  import json
  import logging
  
  from AliFCWeb.fcorm import Orm, Example
  from AliFCWeb import fcIndex, get, post, put, delete, mysqlConn, ResponseEntity
  from AliFCWeb.engine import CreatePool
  
  _log = logging.getLogger()
  _mysql = CreatePool('mysql', 
                    maxconnections=10,  # 连接池允许的最大连接数，0和None表示不限制连接数
                    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
                    maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享
                    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。
                    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
                    )
  
  @fcIndex(debug=True)
  def handler(environ, start_response):
      pass
  
  @post()
  def testFC(data):
      # 每次使用前必须获取连接，之后和正常使用方式一致
      _conn = _mysql.conn()
      orm = Orm(_conn, 'user')
      userId = orm.updateByPrimaryKey({'age': 20}, 1)
      user = orm.selectByPrimaeyKey(1)
      return ResponseEntity.ok(user)
```
## 八、自定义锚点

在使用数据库时，我们用到的mysqlConn、redisConn和postgresqlConn其实就是锚点。锚点的作用是在运行时加载全局变量。**当你需要在全局变量中使用environ中的数据或者在全局变量中使用配置中心时可以派上用场。**

- 拷贝demo14重命名为demo15

- 修改template.yml文件

- 新增锚点文件mySign.py

  - 首先引入

    ```python
    from AliFCWeb.sign import Sign
    ```

  - 新建MySign类并继承Sign重写replace()方法即可

- 修改index.py文件

  ```python
  import json
  import logging
  
  from AliFCWeb import fcIndex, get, post, put, delete, ResponseEntity
  from mySign import MySign
  
  _log = logging.getLogger()
  
  
  @fcIndex(debug=True)
  def handler(environ, start_response):
      pass
  
  # 使用锚点
  @MySign
  def getUrl():
      pass
  
  @get()
  def testFC(data):
      return ResponseEntity.ok(getUrl)
  ```

- 测试结果
![](./img/demo15/01.png)



  