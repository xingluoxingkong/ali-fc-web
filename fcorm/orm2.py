import logging
from .constant import AUTO_INCREMENT_KEYS, PRIMARY_KEY
from fcutils import fieldStrAndPer, fieldSplit, joinList, pers

_log = logging.getLogger()

class Transaction(object):
    def __init__(self, conn):
        ''' 统一操作数据库
        --
            @param conn: 数据库连接
        '''
        self.conn = conn
        self.orms = []
    
    def add(self, orms):
        ''' 添加需要执行的Orm
        --
            @param orm: Orm2类型,或者Orm2的列表、元组
        '''
        if isinstance(orms, list) or isinstance(orms, tuple):
            self.orms.extend(orms)
        elif isinstance(orms, Orm2):
            self.orms.append(orms)
        return self
    
    def _run(self, cursor, sql, values, fetch):
        ''' 执行一条语句
        '''
        _log.info(sql)
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        
        if fetch == 'fetchone':
            return cursor.fetchone()
        elif fetch == 'fetchall':
            return cursor.fetchall()
        elif fetch == 'lastrowid':
            return cursor.lastrowid
        else:
            return True
    
    def commit(self):
        ''' 执行事务。按插入顺序依次返回结果集
        --
        '''
        cursor = self.conn.cursor()
        try:
            res = []
            for orm in self.orms:
                for s in orm.sqlStack:
                    if isinstance(s, tuple):
                        num = self._run(cursor, **s[0])['num']
                        dataList = self._run(cursor, **s[1])
                        res.append((num, dataList))
                    else:
                        res.append(self._run(cursor, **s))

            self.conn.commit()

            if len(res) == 1:
                return res[0]
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()

class Orm2(object):
    def __init__(self, tableName, keyProperty = PRIMARY_KEY):
        ''' 操作数据库，默认是不自动提交事务，如需手动提交请调用Orm2.beginTransaction()方法开启事务
        --
            @param tableName: 表名
            @param keyProperty: 主键字段名。可以不填，不填默认主键名为id
        '''
        # 表名
        self.tableName = tableName
        # 主键名
        self.keyProperty = keyProperty
        # 主键策略
        self.generator = AUTO_INCREMENT_KEYS
        # 多表连接
        self.joinStr = ''
        # 查询字段
        self.properties = ' * '
        # 排序字段
        self.orderByStr = ''
        # 分组字段
        self.groupByStr = ''
        # HAVING字段
        self.havingStr = ''
        self.havingValues = []
        # 是否去重
        self.distinct = ''
        # 执行栈
        # 格式{sql='', values='', fetch='fetchone/fetchall/lastrowid/boolean'}
        self.sqlStack = []

    def setPrimaryGenerator(self, generator):
        ''' 设置表的主键生成策略，不设置则默认使用数据库自增主键
        --
            @param generator: 主键生成策略，默认自增。可传入一个方法，需要主键时自动调用该方法。
                            该方法不能传入参数，如果需要传参，请在外部调用后存入data
        '''
        if isinstance(generator, function):
            self.generator = generator
        return self

    #################################### 新增操作 ####################################
    def insertData(self, *args):
        ''' 向数据库中写入数据
        --
            @example
                orm.insertData({'name':'张三', 'age':18})
                orm.insertData(['name', 'age'], [['张三', 18], ['李四', 19]])
                orm.insertData([{'name':'张三', 'age':18}, {'name':'李四', 'age':19}])
            
            @param args: 要写入的数据，可以有以下三种形式：
                        1. dict: 单条数据key,value键值对形式
                        2. list, list: 两个数组形式。第一个数据传入数据库中对应的字段。第二个数组传入需要写入的数据，可以是单条数据（一维数组），也可以是多条数据（二维数组）
                        3. list: 多条数据，数组里面是多个字典，每个字典代表一条数据
        '''
        n = len(args)
        if n == 1:
            if isinstance(args[0], list):
                insertDictList(args[0])
               
            elif isinstance(args[0], dict):
                insertOne(args[0])
            else:
                return -1
        elif n == 2:
            insertList(args[0], args[1])
        
        return self

    def insertOne(self, data):
        ''' 向数据库写入一条数据
        --
            @example
                orm.insertOne({'name':'张三', 'age':18})
                
            @param data: 要插入的数据 字典格式
        '''
        if not data:
            raise Exception('数据为空！')

        # 如果主键不是自增，则生成主键
        if self.generator != AUTO_INCREMENT_KEYS:   
            if self.keyProperty not in data or data[self.keyProperty] == 0:    # 传入的data里面没有主键或者主键值为0
                data[self.keyProperty] = self.generator()
        
        keys, ps, values = fieldSplit(data)
        sql = 'INSERT INTO `{}`({}) VALUES({})'.format(self.tableName, keys, ps)

        self.sqlStack.append({'sql':sql, 'values': values, 'fetch': 'lastrowid'})

        return self

    def insertList(self, keys, dataList):
        ''' 插入一组数据，注意：返回的是第一条数据的ID
        --
            @example
                orm.insertList(['name', 'age'], [['张三', 18], ['李四', 19]])

            @param keys: 插入的字段名
            @param dataList: 插入的数据列表，和字段名一一对应
        '''
        if not dataList or not dataList[0]:
            raise Exception('数据为空！')

        
        # 如果主键不是自增，则生成主键
        if self.generator != AUTO_INCREMENT_KEYS:   
            if self.keyProperty not in keys:    # 传入的keys里面没有主键
                keys.append(self.keyProperty)
                for data in dataList:
                    data.append(self.generator())

        sql = 'INSERT INTO `{}`({}) VALUES({})'.format(self.tableName, joinList(keys), pers(len(keys)))
        
        self.sqlStack.append({'sql':sql, 'values': dataList, 'fetch': 'lastrowid'})
        
        return self

    def insertDictList(self, dataList):
        ''' 插入一组数据，注意：返回的是第一条数据的ID
        --
            @example
                orm.insertDictList([{'name':'张三', 'age':18}, {'name':'李四', 'age':19}])

            @param dataList: 插入的数据列表
        '''
        if not dataList or not dataList[0]:
            raise Exception('数据为空！')

        
        values = []
        keys = ''
        ps = ''

        for data in dataList:
            if self.keyProperty not in data or data[self.keyProperty] == 0:    # 没有主键
                if self.generator != AUTO_INCREMENT_KEYS:   # 如果主键不是自增，则生成主键
                    data[self.keyProperty] = self.generator
            keys, ps, vs = fieldSplit(data)
            values.append(vs)
        
        sql = 'INSERT INTO `{}`({}) VALUES({})'.format(self.tableName, keys, ps)

        self.sqlStack.append({'sql':sql, 'values': values, 'fetch': 'lastrowid'})

        return self

    #################################### 更新操作 ####################################
    def updateByPrimaryKey(self, data, primaryValue = None):
        ''' 根据主键更新数据
        --
            @param data: 要更新的数据，字典格式
            @param primaryValue: 主键值，为None则从data中寻找主键
        '''
        if not primaryValue:
            primaryValue = data.pop(self.keyProperty, None)
        
        if not primaryValue:
            raise Exception('未传入主键值！')
        
        if not data:
            raise Exception('数据为空！')

        fieldStr, values = fieldStrAndPer(data)
        values.append(primaryValue)
        sql = 'UPDATE `{}` SET {} WHERE `{}`=%s'.format(self.tableName, fieldStr, self.keyProperty)

        self.sqlStack.append({'sql':sql, 'values': values, 'fetch': 'boolean'})

        return self

    def updateByExample(self, data, example):
        ''' 根据Example条件更新
        --
        '''
        if not example:
            raise Exception('未传入更新条件！')
        
        if not data:
            raise Exception('数据为空！')

        whereStr, values1 = example.whereBuilder()
        fieldStr, values2 = fieldStrAndPer(data)
        values2.extend(values1)
        sql = 'UPDATE `{}` SET {} WHERE {}'.format(self.tableName, fieldStr, whereStr)
        
        self.sqlStack.append({'sql':sql, 'values': values2, 'fetch': 'boolean'})
        
        return self
        
    #################################### 查询操作 ####################################
    def orderByClause(self, key, clause = 'DESC'):
        ''' ORDER BY key clause
        --
            @param key 排序字段
            @param clause DESC或者ASC
        '''
        if not self.orderByStr:
            self.orderByStr = ' ORDER BY ' + key + ' ' + clause + ' '
        else:
            self.orderByStr = self.orderByStr + ' , ' + key + ' ' + clause + ' '
        return self
    
    def groupByClause(self, key):
        ''' GROUP BY key clause
        --
            @param key 分组字段
        '''
        if not self.groupByStr:
            self.groupByStr = ' GROUP BY ' + key + ' '
        else:
            self.groupByStr = self.groupByStr + ' , ' + key
        return self
    
    def havingByExample(self, example):
        ''' HAVING
        --
        '''
        self.havingStr, self.havingValues = example.whereBuilder()
        return self
    
    def join(self, tName, onStr):
        ''' 多表连接查询，内连接
        --
            @param tName: 表名
            @param onStr: 条件
        '''
        self.joinStr = self.joinStr + ' JOIN ' + tName + ' ON ' + onStr + ' '
        return self

    def leftJoin(self, tName, onStr):
        ''' 多表连接查询，内连接
        --
            @param tName: 表名
            @param onStr: 条件
        '''
        self.joinStr = self.joinStr + ' LEFT JOIN ' + tName + ' ON ' + onStr + ' '
        return self

    def rightJoin(self, tName, onStr):
        ''' 多表连接查询，内连接
        --
            @param tName: 表名
            @param onStr: 条件
        '''
        self.joinStr = self.joinStr + ' RIGHT JOIN ' + tName + ' ON ' + onStr + ' '
        return self
    
    def setDistinct(self):
        ''' 设置去重
        '''
        self.distinct = ' DISTINCT '
        return self

    def setSelectProperties(self, properties):
        ''' 设置查询的列名，不设置默认采用【SELECT * FROM】
        --
            @param properties: 查询的列，list格式和dict格式
                @example:
                    ['name', 'age'] => SELECT `name`, `age` FROM
                    {'user':['name', 'age'], 'order':['orderId']}  => SELECT `user`.`name`, `user`.`age`, `order`:`orderId` FROM
                    {'user':[('name', 'user_name'), 'age'], 'order':['orderId']}  => SELECT `user`.`name` `user_name`, `user`.`age`, `order`:`orderId` FROM
        '''
        if isinstance(properties, list):
            for i, v in enumerate(properties):
                if isinstance(v, tuple):
                    vTuple1 = v[0]
                    vTuple2 = v[1]
                    if '.' in vTuple1:
                        vTuple1s = vTuple1.split('.')
                        vTuple1 = '`' + vTuple1s[0] + '`.`' + vTuple1s[1] + '`'
                    properties[i] = ' {} {} '.format(vTuple1, vTuple2)
                elif '.' in v:
                    vs = v.split('.')
                    properties[i] = '`' + vs[0] + '`.`' + vs[1] + '`'
                else:
                    properties[i] = '`' + v + '`'
            self.properties = joinList(properties, prefix='', suffix='')
        elif isinstance(properties, dict):
            arr = []
            for k, v1 in properties.items():
                for v2 in v1:
                    if isinstance(v2, tuple):
                        arr.append('`{}`.`{}` `{}`'.format(k, v2[0], v2[1]))
                    else:
                        arr.append('`{}`.`{}`'.format(k, v2))
            self.properties = joinList(arr, prefix='', suffix='')
        return self

    def selectAll(self):
        ''' 查询所有
        --
        '''
        strDict = {
            'distinctStr':self.distinct,
            'propertiesStr': self.properties,
            'tableName': self.tableName,
            'joinStr': self.joinStr,
            'groupByStr': self.groupByStr,
            'orderByStr': self.orderByStr
        }
        sql = '''SELECT {distinctStr} {propertiesStr} FROM {tableName} {joinStr} {groupByStr} {orderByStr}'''.format(**strDict)
        
        self.sqlStack.append({'sql':sql, 'values': None, 'fetch': 'fetchall'})

        return self

    def selectByPrimaeyKey(self, primaryValue):
        ''' 根据主键查询
        --
            @param primaryValue: 主键值
        '''
        strDict = {
            'distinctStr':self.distinct,
            'propertiesStr': self.properties,
            'tableName': self.tableName,
            'joinStr': self.joinStr,
            'whereStr':'`{}`=%s'.format(self.keyProperty),
            'groupByStr': self.groupByStr,
            'orderByStr': self.orderByStr
        }
        sql = '''SELECT {distinctStr} {propertiesStr} FROM {tableName} {joinStr} 
            WHERE {whereStr} {groupByStr} {orderByStr}
            '''.format(**strDict)

        self.sqlStack.append({'sql':sql, 'values': primaryValue, 'fetch': 'fetchone'})

        return self

    def selectByExample(self, example):
        ''' 根据Example条件进行查询
        --
        '''
        
        whereStr, values = example.whereBuilder()
        strDict = {
            'distinctStr':self.distinct,
            'propertiesStr': self.properties,
            'tableName': self.tableName,
            'joinStr': self.joinStr,
            'whereStr': whereStr,
            'groupByStr': self.groupByStr,
            'orderByStr': self.orderByStr
        }
        sql = '''SELECT {distinctStr} {propertiesStr} FROM {tableName} {joinStr} 
            WHERE {whereStr} {groupByStr} {orderByStr}
            '''.format(**strDict)

        self.sqlStack.append({'sql':sql, 'values': values, 'fetch': 'fetchall'})

        return self

    def selectTransactByExample(self, transactProperties, example, transactName = '', transact = 'COUNT'):
        ''' 根据Example条件聚合查询
        --
            @param transactProperties: 统计字段
            @param example: 条件
            @param transactName: 重命名统计字段
            @param transact: 使用哪个函数，默认COUNT。可选SUM，MAX，MIN等
        '''
        whereStr, values = example.whereBuilder()
        strDict = {
            'distinctStr':self.distinct,
            'propertiesStr': self.properties,
            'countStr': '{}({}) {}'.format(transact, transactProperties, transactName),
            'tableName': self.tableName,
            'joinStr': self.joinStr,
            'whereStr': whereStr,
            'groupByStr': self.groupByStr,
            'orderByStr': self.orderByStr
        }
        sql = '''SELECT {distinctStr} {propertiesStr} , {countStr} FROM {tableName} {joinStr} 
            WHERE {whereStr} {groupByStr} {orderByStr}
            '''.format(**strDict)
        self.sqlStack.append({'sql':sql, 'values': values, 'fetch': 'fetchall'})
        return self

    def selectGroupHavingByExample(self, transactProperties, example, transactName = '', transact = 'COUNT'):
        ''' 根据Example条件聚合查询
        --
            @param transactProperties: 统计字段
            @param example: 条件
            @param transactName: 重命名统计字段
            @param transact: 使用哪个函数，默认COUNT。可选SUM，MAX，MIN等
        '''
        if not self.groupByStr:
            return False

        whereStr, values = example.whereBuilder()
        strDict = {
            'distinctStr':self.distinct,
            'propertiesStr': self.properties,
            'countStr': '{}({}) {}'.format(transact, transactProperties, transactName),
            'tableName': self.tableName,
            'joinStr': self.joinStr,
            'whereStr': whereStr,
            'groupByStr': self.groupByStr,
            'orderByStr': self.orderByStr
        }
        if self.havingStr and self.havingValues:
            strDict['havingStr'] = ' HAVING ' + self.havingStr
            values.extend(self.havingValues)
        sql = '''SELECT {distinctStr} {propertiesStr} , {countStr} FROM {tableName} {joinStr} 
            WHERE {whereStr} {groupByStr} {havingStr} {orderByStr}
            '''.format(**strDict)
        self.sqlStack.append({'sql':sql, 'values': values, 'fetch': 'fetchall'})
        
        return self

    def selectPageAll(self, page = 1, pageNum = 10):
        ''' 分页查询
        --
        '''
        startId = (page - 1) * pageNum

        strDict1 = {
            'propertiesStr': self.keyProperty,
            'tableName': self.tableName,
            'joinStr': self.joinStr,
            'groupByStr': self.groupByStr,
            'orderByStr': self.orderByStr
        }
        
        sql1 = '''SELECT COUNT(`{propertiesStr}`) num FROM {tableName} {joinStr} 
                {groupByStr} {orderByStr}
                '''.format(**strDict1)

        strDict2 = {
            'distinctStr':self.distinct,
            'propertiesStr': self.properties,
            'tableName': self.tableName,
            'joinStr': self.joinStr,
            'groupByStr': self.groupByStr,
            'orderByStr': self.orderByStr,
            'limitStr':'LIMIT {}, {}'.format(startId, pageNum)
        }
        sql2 = '''SELECT {distinctStr} {propertiesStr} FROM {tableName} {joinStr} 
                {groupByStr} {orderByStr} {limitStr}
                '''.format(**strDict2)

        self.sqlStack.append(({'sql':sql1, 'values': None, 'fetch': 'fetchone'}, {'sql':sql2, 'values': None, 'fetch': 'fetchall'}))
        return self

    def selectPageByExample(self, example, page = 1, pageNum = 10):
        ''' 根据Example条件分页查询
        --
        '''
        startId = (page - 1) * pageNum

        whereStr, values = example.whereBuilder()
        strDict1 = {
            'propertiesStr': self.keyProperty,
            'tableName': self.tableName,
            'joinStr': self.joinStr,
            'whereStr': whereStr,
            'groupByStr': self.groupByStr,
            'orderByStr': self.orderByStr
        }
        
        sql1 = '''SELECT COUNT(`{propertiesStr}`) num FROM {tableName} {joinStr} 
                WHERE {whereStr} {groupByStr} {orderByStr}
                '''.format(**strDict1)
        
        strDict2 = {
            'distinctStr':self.distinct,
            'propertiesStr': self.properties,
            'tableName': self.tableName,
            'joinStr': self.joinStr,
            'whereStr': whereStr,
            'groupByStr': self.groupByStr,
            'orderByStr': self.orderByStr,
            
            'limitStr':'LIMIT {}, {}'.format(startId, pageNum)
        }
        sql2 = '''SELECT {distinctStr} {propertiesStr} FROM {tableName} {joinStr} 
                WHERE {whereStr} {groupByStr} {orderByStr} {limitStr}
                '''.format(**strDict2)
        self.sqlStack.append(({'sql':sql1, 'values': values, 'fetch': 'fetchone'}, {'sql':sql2, 'values': values, 'fetch': 'fetchall'}))
        return self
            

    #################################### 删除操作 ####################################
    def deleteByPrimaryKey(self, primaryValue):
        ''' 根据主键删除 
        '''
        
        if not primaryValue:
            raise Exception('未传入主键值！')

        sql = 'DELETE FROM `{}` WHERE `{}`=%s'.format(self.tableName, self.keyProperty)

        self.sqlStack.append({'sql':sql, 'values': primaryValue, 'fetch': 'boolean'})
        return self

    def deleteByExample(self, example):
        ''' 根据Example条件删除数据
        '''
        if not example:
            raise Exception('未传入更新条件！')

        whereStr, values = example.whereBuilder()
        sql = 'DELETE FROM `{}` WHERE {}'.format(self.tableName, whereStr)
        self.sqlStack.append({'sql':sql, 'values': values, 'fetch': 'boolean'})
        return self
            
    #################################### 原生SQL操作 ####################################
    def selectOneBySQL(self, sql, values = None):
        ''' 查询单个
        --
        '''
        self.sqlStack.append({'sql':sql, 'values': values, 'fetch': 'fetchone'})
        return self

    def selectAllBySQL(self, sql, values = None):
        ''' 查询所有
        --
        '''
        self.sqlStack.append({'sql':sql, 'values': values, 'fetch': 'fetchall'})
        return self

    def executeBySQL(self, sql, values = None):
        ''' 根据sql进行更新删除或者新增操作， 不能用于执行查询操作，因为不会返回查询结果，查询使用selectAllBySQL或者selectOneBySQL
        --
            @param sql: sql语句
            @param values: 参数
            @rerturn: 失败返回-1
        '''
        self.sqlStack.append({'sql':sql, 'values': values, 'fetch': 'lastrowid'})
        return self
    
    #################################### 子查询 ####################################

    
    #################################### 清除数据 ####################################
    def clear(self):
        ''' 清除数据，只保留数据库连接、表名、主键。清除掉主键策略/查询字段/分组字段/排序字段/多表连接/HAVING字段/去重等
        --
        '''
        # 多表连接
        self.joinStr = ''
        # 查询字段
        self.properties = ' * '
        # 排序字段
        self.orderByStr = ''
        # 分组字段
        self.groupByStr = ''
        # HAVING字段
        self.havingStr = ''
        self.havingValues = []
        # 是否去重
        self.distinct = ''
        # 执行栈
        # 格式{sql='', values='', fetch='fetchone/fetchall/lastrowid/boolean'}
        self.sqlStack = []
        return self
    
    