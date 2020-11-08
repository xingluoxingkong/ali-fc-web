import logging
from .constant import AUTO_INCREMENT_KEYS, PRIMARY_KEY
from AliFCWeb.fcutils import fieldStrAndPer, fieldSplit, joinList, pers, dataToStr

__all__ = ['Orm']

_log = logging.getLogger()

_POSTGRE = 'psycopg2'
_MYSQL = 'mysql'


class Orm(object):
    def __init__(self, conn, tableName, keyProperty=PRIMARY_KEY, auto_commit=True):
        ''' 操作数据库，默认自动提交；如设置为手动提交请自己使用conn.commit()提交
        --
            @param conn: 数据库连接
            @param tableName: 表名
            @param keyProperty: 主键字段名。可以不填，不填默认主键名为id
            @param auto_commit: 自动提交
        '''
        if 'psycopg2' in str(type(conn)):
            self.dbType = _POSTGRE
        elif 'mysql' in str(type(conn)):
            self.dbType = _MYSQL
        else:
            try:
                if 'psycopg2' in conn._pool._creator.__name__:
                    self.dbType = _POSTGRE
                elif 'mysql' in conn._pool._creator.__name__:
                    self.dbType = _MYSQL
                else:
                    raise Exception('数据库类型暂不支持！')
            except Exception as e:
                raise Exception('数据库类型暂不支持！')
        # 数据库连接
        self.conn = conn
        # 表名
        if tableName.startswith('`') and tableName.endswith('`'):
            self.tableName = tableName
        elif '.' in tableName:
            tableNameSplit = tableName.split('.')
            self.tableName = '`' + \
                tableNameSplit[0] + '`.`' + tableNameSplit[1] + '`'
        else:
            self.tableName = '`' + tableName + '`'
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
        # 自动提交
        self.auto_commit = auto_commit

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
    def insertData(self, *args, **kw):
        ''' 向数据库中写入数据
        --
            @example
                orm.insertData({'name':'张三', 'age':18})
                orm.insertData(['name', 'age'], [['张三', 18], ['李四', 19]])
                orm.insertData([{'name':'张三', 'age':18}, {'name':'李四', 'age':19}])
                orm.insertData(['name', 'age'], [{'name':'张三', 'age':18}, {'name':'李四', 'age':19}])
                orm.insertData(['name', 'age'], {'name':'张三', 'age':18})

            @param args: 要写入的数据，可以有以下三种形式：
                        1. dict: 单条数据key,value键值对形式
                        2. list, list: 两个数组形式。第一个数据传入数据库中对应的字段。第二个数组传入需要写入的数据，可以是单条数据（一维数组），也可以是多条数据（二维数组）
                        3. list: 多条数据，数组里面是多个字典，每个字典代表一条数据
            
            以下参数仅在插入单条数据时有效：
            @param kw.ignore: 不存在则新增，存在则不改变
            @param kw.replace: 不存在则新增，存在则删除并新增
            @param kw.update: 不存在则新增，存在则更新
        '''
        n = len(args)
        if n == 0:
            return -1
        elif n == 1:
            if isinstance(args[0], list):
                return self.insertDictList(args[0])
            elif isinstance(args[0], dict):
                return self.insertOne(args[0], **kw)
            else:
                return -1
        elif n == 2:
            return self.insertMany(args[0], args[1])
        else:
            return -1

    def insertOne(self, data, ignore=False, replace=False, update=False):
        ''' 向数据库写入一条数据，返回自增id（主键必须是自增并且名字为id），或者受影响的条数（没有自增id）
        --
            @example
                orm.insertOne({'name':'张三', 'age':18})

            @param data: 要插入的数据 字典格式
            @param ignore: 不存在则新增，存在则不改变
            @param replace: 不存在则新增，存在则删除并新增
            @param update: 不存在则新增，存在则更新
        '''
        if not data:
            raise Exception('数据为空！')

        if ignore and replace and update:
            raise Exception('ignore,replace和update只能有一个为true')

        if ignore:
            ignore = 'IGNORE'
        else:
            ignore = ''

        if replace:
            replace = 'REPLACE'
        else:
            replace = ''

        cursor = self.conn.cursor()
        try:
            # 如果主键不是自增，则生成主键
            if self.generator != AUTO_INCREMENT_KEYS:
                # 传入的data里面没有主键或者主键值为0
                if self.keyProperty not in data or data[self.keyProperty] == 0:
                    data[self.keyProperty] = self.generator()

            keys, ps, values = fieldSplit(data)
            sql = '{} INSERT {} INTO {}({}) VALUES({})'.format(replace, ignore,
                                                               self.tableName, keys, ps)
            if update:
                fieldStr, values2 = fieldStrAndPer(data)
                sql += ' ON DUPLICATE KEY UPDATE {}'.format(fieldStr)
                values.extend(values2)

            if self.dbType == _POSTGRE and self.keyProperty == PRIMARY_KEY:
                sql += ' RETURNING {}'.format(self.keyProperty)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            affectedRows = cursor.execute(sql, values)
            if self.keyProperty == PRIMARY_KEY:
                lastId = cursor.lastrowid
                # 获取postgre的自增id
                if self.dbType == _POSTGRE:
                    idRow = cursor.fetchone()
                    if idRow:
                        lastId = idRow[self.keyProperty]
                if self.auto_commit:
                    self.conn.commit()
                return lastId
            else:
                if self.auto_commit:
                    self.conn.commit()
                return affectedRows
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception('insertOne error; values:{}'.format(data))
        finally:
            cursor.close()

    def insertMany(self, keys, data):
        ''' 插入一组数据，可以指定字段名，返回自增id（单条数据且有自增id）或者受影响的条数
        --
            @example
                orm.insertMany(['name', 'age'], [{'name':'张三', 'age':18}, {'name':'李四', 'age':19}])
                orm.insertMany(['name', 'age'], {'name':'张三', 'age':18})
                orm.insertMany(['name', 'age'], [['张三', 18], ['李四', 19]])

            @param keys: 插入的字段名
            @param data: 插入的数据, 字典格式（单条）， 列表（列表里包含字典）格式（多条）
        '''
        if not data:
            raise Exception('数据为空！')

        cursor = self.conn.cursor()
        try:
            dataList = []
            columns = []
            if isinstance(data, dict):
                for k in keys:
                    if k in data:
                        dataList.append(dataToStr(data[k]))
                        columns.append(k)

            elif isinstance(data, list):
                if isinstance(data[0], list):
                    for l in data:
                        d = list(map(dataToStr, l))
                        dataList.append(d)
                    columns = keys
                elif isinstance(data[0], dict):
                    sign = True
                    for d in data:
                        dd = []
                        for k in keys:
                            if k in data:
                                dd.append(dataToStr(d[k]))
                                if sign:
                                    columns.append(k)
                        sign = False
                        if dd:
                            dataList.append(dd)

            if self.generator != AUTO_INCREMENT_KEYS:
                if self.keyProperty not in columns:
                    columns.append(self.keyProperty)
                    if isinstance(dataList[0], list):
                        for data in dataList:
                            data.append(self.generator())
                    else:
                        dataList.append(self.generator())

            sql = 'INSERT  INTO {}({}) VALUES({})'.format(
                self.tableName, joinList(columns), pers(len(columns)))

            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, dataList))
            affectedRows = 0
            if isinstance(dataList[0], list):
                affectedRows = cursor.executemany(sql, dataList)
                if self.auto_commit:
                    self.conn.commit()
                return affectedRows
            else:
                if self.dbType == _POSTGRE and self.keyProperty == PRIMARY_KEY:
                    sql += ' RETURNING {}'.format(self.keyProperty)
                affectedRows = cursor.execute(sql, dataList)
                if self.keyProperty == PRIMARY_KEY:
                    lastId = cursor.lastrowid
                    # 获取postgre的自增id
                    if self.dbType == _POSTGRE:
                        idRow = cursor.fetchone()
                        if idRow:
                            lastId = idRow[self.keyProperty]
                    if self.auto_commit:
                        self.conn.commit()
                    return lastId
                else:
                    if self.auto_commit:
                        self.conn.commit()
                    return affectedRows
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception('insertList error; values:{}'.format(dataList))
        finally:
            cursor.close()

    def insertDictList(self, dataList):
        ''' 插入一组数据，返回受影响的条数
        --
            @example
                orm.insertDictList([{'name':'张三', 'age':18}, {'name':'李四', 'age':19}])

            @param dataList: 插入的数据列表
        '''
        if not dataList or not dataList[0]:
            raise Exception('数据为空！')

        cursor = self.conn.cursor()
        try:
            values = []
            keys = ''
            ps = ''

            for data in dataList:
                # 没有主键
                if self.keyProperty not in data or data[self.keyProperty] == 0:
                    if self.generator != AUTO_INCREMENT_KEYS:   # 如果主键不是自增，则生成主键
                        data[self.keyProperty] = self.generator
                keys, ps, vs = fieldSplit(data)
                values.append(vs)

            sql = ' INSERT INTO {}({}) VALUES({})'.format(
                self.tableName, keys, ps)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            affectedRows = cursor.executemany(sql, values)
            if self.auto_commit:
                self.conn.commit()
            return affectedRows
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception('insertDictList error; values:{}'.format(dataList))
        finally:
            cursor.close()

    #################################### 更新操作 ####################################
    def updateByPrimaryKey(self, data, primaryValue=None, keys=None):
        ''' 根据主键更新数据
        --
            @param data: 要更新的数据，字典格式
            @param primaryValue: 主键值，为None则从data中寻找主键
            @param keys: 更新哪些列，如果此项有值则只更新data中指定的列，多余的列不会被更新
        '''
        if not primaryValue:
            primaryValue = data.pop(self.keyProperty, None)

        if not primaryValue:
            raise Exception('未传入主键值！')

        if not data:
            raise Exception('数据为空！')

        if keys:
            data2 = {}
            for k in keys:
                if k in data:
                    data2[k] = data[k]
            data = data2

        cursor = self.conn.cursor()
        try:
            fieldStr, values = fieldStrAndPer(data)
            values.append(primaryValue)
            sql = 'UPDATE {} SET {} WHERE `{}`=%s'.format(
                self.tableName, fieldStr, self.keyProperty)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            res = cursor.execute(sql, values)
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception('updateByPrimaryKey error; values:{}'.format(data))
        finally:
            cursor.close()

    def updateByExample(self, data, example, keys=None):
        ''' 根据Example条件更新
        --
            @param data: 要更新的数据，字典格式
            @param example: 更新条件
            @param keys: 更新哪些列，如果此项有值则只更新data中指定的列，多余的列不会被更新
        '''
        if not example:
            raise Exception('未传入更新条件！')

        if not data:
            raise Exception('数据为空！')

        if keys:
            data2 = {}
            for k in keys:
                if k in data:
                    data2[k] = data[k]
            data = data2

        cursor = self.conn.cursor()
        try:
            whereStr, values1 = example.whereBuilder()
            fieldStr, values2 = fieldStrAndPer(data)
            values2.extend(values1)
            sql = 'UPDATE {} SET {} WHERE {}'.format(
                self.tableName, fieldStr, whereStr)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, values2))
            res = cursor.execute(sql, values2)
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception('updateByExample error; values:{}'.format(data))
        finally:
            cursor.close()

    #################################### 查询操作 ####################################
    def orderByClause(self, key, clause='DESC'):
        ''' ORDER BY key clause
        --
            @param key 排序字段
            @param clause DESC或者ASC
        '''
        if '.' in key:
            keys = key.split('.')
            key = '`' + keys[0] + '`.`' + keys[1] + '`'
        else:
            key = '`' + key + '`'
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
        if '.' in key:
            keys = key.split('.')
            key = '`' + keys[0] + '`.`' + keys[1] + '`'
        else:
            key = '`' + key + '`'
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
                    else:
                        vTuple1 = '`' + vTuple1 + '`'
                    vTuple2 = '`' + vTuple2 + '`'
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
        cursor = self.conn.cursor()

        try:
            strDict = {
                'distinctStr': self.distinct,
                'propertiesStr': self.properties,
                'tableName': self.tableName,
                'joinStr': self.joinStr,
                'groupByStr': self.groupByStr,
                'orderByStr': self.orderByStr
            }
            sql = '''SELECT {distinctStr} {propertiesStr} FROM {tableName} {joinStr} {groupByStr} {orderByStr}'''.format(
                **strDict)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}'.format(sql))
            cursor.execute(sql)
            res = cursor.fetchall()
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception('selectAll error; ')
        finally:
            cursor.close()

    def selectByPrimaeyKey(self, primaryValue):
        ''' 根据主键查询
        --
            @param primaryValue: 主键值
        '''
        try:
            import psycopg2
        except Exception as e:
            pass

        cursor = self.conn.cursor()

        try:
            strDict = {
                'distinctStr': self.distinct,
                'propertiesStr': self.properties,
                'tableName': self.tableName,
                'joinStr': self.joinStr,
                'whereStr': '{}.`{}`=%s'.format(self.tableName, self.keyProperty),
                'groupByStr': self.groupByStr,
                'orderByStr': self.orderByStr
            }
            sql = '''SELECT {distinctStr} {propertiesStr} FROM {tableName} {joinStr} 
                WHERE {whereStr} {groupByStr} {orderByStr}
                '''.format(**strDict)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, primaryValue))
            cursor.execute(sql, [primaryValue])
            res = cursor.fetchone()
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception(
                'selectByPrimaeyKey error; values:{}'.format(primaryValue))
        finally:
            cursor.close()

    def selectByExample(self, example):
        ''' 根据Example条件进行查询
        --
        '''
        cursor = self.conn.cursor()

        try:
            whereStr, values = example.whereBuilder()
            strDict = {
                'distinctStr': self.distinct,
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
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            cursor.execute(sql, values)
            res = cursor.fetchall()
            # if res and len(res) == 1:
            #     res = res[0]
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception('selectByExample error; values:{}'.format(example))
        finally:
            cursor.close()

    def selectTransactByExample(self, transactProperties, example, transactName='', transact='COUNT'):
        ''' 根据Example条件聚合查询
        --
            @param transactProperties: 统计字段
            @param example: 条件
            @param transactName: 重命名统计字段
            @param transact: 使用哪个函数，默认COUNT。可选SUM，MAX，MIN等
        '''
        cursor = self.conn.cursor()

        try:
            whereStr, values = example.whereBuilder()
            strDict = {
                'distinctStr': self.distinct,
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
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            cursor.execute(sql, values)
            res = cursor.fetchall()
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception(
                'selectTransactByExample error; values:{}'.format(transactProperties))
        finally:
            cursor.close()

    def selectGroupHavingByExample(self, transactProperties, example, transactName='', transact='COUNT'):
        ''' 根据Example条件聚合查询
        --
            @param transactProperties: 统计字段
            @param example: 条件
            @param transactName: 重命名统计字段
            @param transact: 使用哪个函数，默认COUNT。可选SUM，MAX，MIN等
        '''
        if not self.groupByStr:
            return False

        cursor = self.conn.cursor()

        try:
            whereStr, values = example.whereBuilder()
            strDict = {
                'distinctStr': self.distinct,
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
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            cursor.execute(sql, values)
            res = cursor.fetchall()
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception(
                'selectGroupHavingByExample error; values:{}'.format(transactProperties))
        finally:
            cursor.close()

    def selectPageAll(self, page=1, pageNum=10):
        ''' 分页查询
        --
        '''
        cursor = self.conn.cursor()

        startId = (page - 1) * pageNum

        try:
            strDict = {
                'propertiesStr': '{}.`{}`'.format(self.tableName, self.keyProperty),
                'tableName': self.tableName,
                'joinStr': self.joinStr,
                # 'groupByStr': self.groupByStr,
                # 'orderByStr': self.orderByStr
            }

            sql = '''SELECT COUNT({propertiesStr}) num FROM {tableName} {joinStr} 
                    '''.format(**strDict)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}'.format(sql))
            cursor.execute(sql)
            numRes = cursor.fetchone()
            num = numRes['num']

            if num == 0 or num < startId:
                return num, []

            strDict = {
                'distinctStr': self.distinct,
                'propertiesStr': self.properties,
                'tableName': self.tableName,
                'joinStr': self.joinStr,
                'groupByStr': self.groupByStr,
                'orderByStr': self.orderByStr,
                'limitStr': self._limit(startId, pageNum)
            }
            sql = '''SELECT {distinctStr} {propertiesStr} FROM {tableName} {joinStr} 
                    {groupByStr} {orderByStr} {limitStr}
                    '''.format(**strDict)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}'.format(sql))
            cursor.execute(sql)
            res = cursor.fetchall()
            if self.auto_commit:
                self.conn.commit()
            return num, res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception('selectPageAll error')
        finally:
            cursor.close()

    def selectPageByExample(self, example, page=1, pageNum=10):
        ''' 根据Example条件分页查询
        --
        '''
        cursor = self.conn.cursor()

        startId = (page - 1) * pageNum

        try:
            whereStr, values = example.whereBuilder()
            strDict = {
                'propertiesStr': '{}.`{}`'.format(self.tableName, self.keyProperty),
                'tableName': self.tableName,
                'joinStr': self.joinStr,
                'whereStr': whereStr,
                # 'groupByStr': self.groupByStr,
                # 'orderByStr': self.orderByStr
            }

            sql = '''SELECT COUNT({propertiesStr}) num FROM {tableName} {joinStr} 
                    WHERE {whereStr}
                    '''.format(**strDict)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            cursor.execute(sql, values)
            numRes = cursor.fetchone()
            num = numRes['num']

            if num == 0 or num < startId:
                return num, []

            strDict = {
                'distinctStr': self.distinct,
                'propertiesStr': self.properties,
                'tableName': self.tableName,
                'joinStr': self.joinStr,
                'whereStr': whereStr,
                'groupByStr': self.groupByStr,
                'orderByStr': self.orderByStr,
                'limitStr': self._limit(startId, pageNum)
            }
            sql = '''SELECT {distinctStr} {propertiesStr} FROM {tableName} {joinStr} 
                    WHERE {whereStr} {groupByStr} {orderByStr} {limitStr}
                    '''.format(**strDict)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            cursor.execute(sql, values)
            res = cursor.fetchall()
            if self.auto_commit:
                self.conn.commit()
            return num, res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception(
                'selectPageByExample error; values:{}'.format(example))
        finally:
            cursor.close()

    #################################### 删除操作 ####################################
    def deleteByPrimaryKey(self, primaryValue):
        ''' 根据主键删除 
        '''

        if not primaryValue:
            raise Exception('未传入主键值！')

        cursor = self.conn.cursor()
        try:
            sql = 'DELETE FROM {} WHERE `{}`=%s'.format(
                self.tableName, self.keyProperty)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, primaryValue))
            res = cursor.execute(sql, [primaryValue])
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception(
                'deleteByPrimaryKey error; values:{}'.format(primaryValue))
        finally:
            cursor.close()

    def deleteByExample(self, example):
        ''' 根据Example条件删除数据
        '''
        if not example:
            raise Exception('未传入更新条件！')

        cursor = self.conn.cursor()
        try:
            whereStr, values = example.whereBuilder()
            sql = 'DELETE FROM {} WHERE {}'.format(self.tableName, whereStr)
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            res = cursor.execute(sql, values)
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception('deleteByExample error; values:{}'.format(example))
        finally:
            cursor.close()

    #################################### 原生SQL操作 ####################################
    def selectOneBySQL(self, sql, values=None):
        ''' 查询单个
        --
        '''
        cursor = self.conn.cursor()

        try:
            sql = self._encodeSql(sql)
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            if values:
                cursor.execute(sql, values)
            else:
                cursor.execute(sql)
            res = cursor.fetchone()
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception(
                'selectOneBySQL error; sql:{} values:{}'.format(sql, values))
        finally:
            cursor.close()

    def selectAllBySQL(self, sql, values=None):
        ''' 查询所有
        --
        '''
        cursor = self.conn.cursor()

        try:
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            if values:
                cursor.execute(self._encodeSql(sql), values)
            else:
                cursor.execute(self._encodeSql(sql))
            res = cursor.fetchall()
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception(
                'selectAllBySQL error; sql:{} values:{}'.format(sql, values))
        finally:
            cursor.close()

    def executeBySQL(self, sql, values=None):
        ''' 根据sql进行更新删除或者新增操作， 不能用于执行查询操作，因为不会返回查询结果，查询使用selectAllBySQL或者selectOneBySQL
        --
            @param sql: sql语句
            @param values: 参数
            @rerturn: 失败返回-1
        '''
        cursor = self.conn.cursor()
        try:
            _log.info('执行sql语句：{}；值：{}'.format(sql, values))
            if values:
                cursor.execute(self._encodeSql(sql), values)
            else:
                cursor.execute(self._encodeSql(sql))

            res = cursor.lastrowid
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception(
                'executeBySQL error; sql:{} values:{}'.format(sql, values))
        finally:
            cursor.close()

    #################################### 子查询 ####################################
    #################################### 清空表 ####################################
    def truncateTable(self):
        ''' 清空表
        --
        '''
        cursor = self.conn.cursor()
        sql = f'TRUNCATE TABLE {self.tableName}'
        try:
            
            _log.info('执行sql语句：{}'.format(sql))
            res = cursor.execute(sql)
            if self.auto_commit:
                self.conn.commit()
            return res
        except Exception as e:
            _log.error(e)
            self.conn.rollback()
            raise Exception(
                'selectOneBySQL error; sql:{}'.format(sql))
        finally:
            cursor.close()

    #################################### 清除关闭 ####################################

    def autoCommit(self, auto_commit=True):
        ''' 打开/关闭自动提交
        --
        '''
        self.auto_commit = auto_commit
        return self

    def clear(self):
        ''' 清除数据，只保留数据库连接、表名、主键。清除掉主键策略/查询字段/分组字段/排序字段/多表连接/HAVING字段/去重等；但不会重置自动提交
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
        return self

    def close(self):
        ''' 关闭数据库连接
        --
        '''
        self.conn.close()

    ###################################解决postgresql的兼容性问题#####################################

    def _encodeSql(self, sql):
        ''' 编码sql语句
        --
        '''
        if self.dbType == _POSTGRE:
            new_sql = sql.replace('`', '"')
            # 如果是自增id，添加返回值
            # if 'INSERT' in sql.upper() and self.keyProperty == PRIMARY_KEY:
            #     new_sql += ' RETURNING {}'.format(self.keyProperty)
            return new_sql
        return sql

    def _limit(self, startId, pageNum):
        if self.dbType == _POSTGRE:
            return 'LIMIT {} offset {}'.format(pageNum, startId)
        return 'LIMIT {}, {}'.format(startId, pageNum)
