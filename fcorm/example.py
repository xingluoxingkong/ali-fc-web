from fcutils import pers
class Example(object):
    def __init__(self):
        ''' SQL语句条件
        --
        '''
        # 条件连接符， or或者and
        self.orAnd = []
        # 连接字段
        self.where = []
    
    def andExample(self, example):
        ''' 添加条件组
        --
            @param example 不为空则example中的所有条件用一对括号表示
        '''
        self._append('AND', example)
        return self
    
    def orExample(self, example):
        ''' 添加条件组
        --
            @param example 不为空则example中的所有条件用一对括号表示
        '''
        self._append('OR', example)
        return self
    
    def andEqualTo(self, params):
        ''' key1=value1 AND key2=value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('AND', (k, v, '='))
        return self

    
    def andNotEqualTo(self, params):
        ''' key1<>value1 AND key2<>value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('AND', (k, v, '<>'))
        return self
    
    def orEqualTo(self, params):
        ''' key1=value1 OR key2=value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('OR', (k, v, '='))
        return self
    
    def orNotEqualTo(self, params):
        ''' key1<>value1 OR key2<>value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('OR', (k, v, '<>'))
        return self

    def andGreaterThan(self, params):
        ''' key1>value1 AND key2>value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('AND', (k, v, '>'))
        return self
    
    def orGreaterThan(self, params):
        ''' key1>value1 OR key2>value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('OR', (k, v, '>'))
        return self
    
    def andLessThan(self, params):
        ''' key1<value1 AND key2<value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('AND', (k, v, '<'))
        return self

    
    def orLessThan(self, params):
        ''' key1<value1 OR key2<value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('OR', (k, v, '<'))
        return self
    
    def andGreaterThanOrEqualTo(self, params):
        ''' key1>value1 AND key2>value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('AND', (k, v, '>='))
        return self
    
    def orGreaterThanOrEqualTo(self, params):
        ''' key1>value1 OR key2>value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('OR', (k, v, '>='))
        return self
    
    def andLessThanOrEqualTo(self, params):
        ''' key1<value1 AND key2<value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('AND', (k, v, '<='))
        return self
    
    def orLessThanOrEqualTo(self, params):
        ''' key1<value1 OR key2<value2
        --
            @param params 字典格式的键值对
        '''
        for k, v in params.items():
            self._append('OR', (k, v, '<='))
        return self
    
    def andInValues(self, key, values):
        ''' AND key IN (value1, values...)
        --
        '''
        self._append('AND', (key, values, 'IN'))
        return self

    def orInValues(self, key, values):
        ''' OR key IN (value1, values...)
        --
        '''
        self._append('OR', (key, values, 'IN'))
        return self
    
    def andNotInValues(self, key, values):
        ''' AND key NOT IN (value1, values...)
        --
        '''
        self._append('AND', (key, values, 'NOT IN'))
        return self
    
    def orNotInValues(self, key, values):
        ''' OR NOT IN (value1, values...)
        --
        '''
        self._append('OR', (key, values, 'NOT IN'))
        return self
    
    def andLike(self, key, value):
        ''' AND key LIKE value
        --
        '''
        self._append('AND', (key, value, 'LIKE'))
        return self
    
    def orLike(self, key, value):
        ''' OR key LIKE value
        --
        '''
        self._append('OR', (key, value, 'LIKE'))
        return self
    
    def andNotLike(self, key, value):
        ''' AND key NOT LIKE value
        --
        '''
        self._append('AND', (key, value, 'NOT LIKE'))
        return self
    
    def orNotLike(self, key, value):
        ''' OR key NOT LIKE value
        --
        '''
        self._append('OR', (key, value, 'NOT LIKE'))
        return self
    
    def andBetween(self, key, v1, v2):
        ''' AND key BETWEEN v1 AND v2
        --
        '''
        self._append('AND', (key, [v1, v2], 'BETWEEN'))
        return self
    
    def orBetween(self, key, v1, v2):
        ''' OR key BETWEEN v1 AND v2
        --
        '''
        self._append('OR', (key, [v1, v2], 'BETWEEN'))
        return self
    
    def andNotBetween(self, key, v1, v2):
        ''' AND key BETWEEN v1 AND v2
        --
        '''
        self._append('AND', (key, [v1, v2], 'NOT BETWEEN'))
        return self
    
    def orNotBetween(self, key, v1, v2):
        ''' OR key BETWEEN v1 AND v2
        --
        '''
        self._append('OR', (key, [v1, v2], 'NOT BETWEEN'))
        return self
    
    def setWhereFromStr(self, whereStr):
        ''' 直接从字符串中读取where条件
        --
        '''
        ################################## TODO ####################################
        # temp = ''
        # for s in whereStr:
        #     if s == ' ':
        #         if len(temp) > 0:
        #             pass
        #     elif s >= 'a' and s <='z' or s >= 'A' and s <= 'Z':
        #         print('字母')
        #     elif s >= '0' and s <= '9':
        #         print('数字')
        #     else:
        #         print('符号') 
        return self
    
    def _append(self, orAnd, where):
        ''' 添加标记
        '''
        if not self.orAnd and not self.where:
            self.where.append(where)
        else:
            self.orAnd.append(orAnd)
            self.where.append(where)

    def _builder(self, w):
        ''' 单个条件编译
        '''
        if isinstance(w, tuple):
            k, v, p = w
            if '.' in k:
                kSplit = k.split('.')
                if len(kSplit) == 2:
                    k = '`' + kSplit[0] + '`.`' + kSplit[1] +'`'
            else:
                k = '`' + k + '`'
                
            if p == 'IN' or p == 'NOT IN':
                whereStr = ' ' + k + ' ' + p + ' (' + pers(len(v)) + ') '
                return whereStr, v
            elif p == 'BETWEEN' or p == 'NOT BETWEEN':
                whereStr = ' ' + k + ' ' + p + ' %s AND %s '
                return whereStr, v
            else:
                whereStr = ' ' + k + ' ' + p + ' %s '
                return whereStr, v
        elif isinstance(w, Example):
            s, v = w.whereBuilder()
            whereStr = ' (' + s + ') '
            return whereStr, v
    
    def whereBuilder(self):
        ''' 编译生成where后面的语句
        --
            @example
                Example().andEqualTo({'name':'张三', 'age':18}).andInValues('id', [1, 2, 3]).orLike('title', '%a%').whereBuilder()
                @print (' name = %s  AND  age = %s  AND  id IN (%s, %s, %s)  OR  title LIKE %s ', ['张三', 18, 1, 2, 3, '%a%'])
        '''
        if len(self.where) == 0:
            raise Exception('你还没有设置查询条件！') 
        
        whereStr = ''
        values = []
        for i, w in enumerate(self.where):
            s, v = self._builder(w)

            if i == 0:
                whereStr += s
            else:
                whereStr += (' ' + self.orAnd[i - 1] + ' ' + s)
            
            if isinstance(v, list):
                values.extend(v)
            else:
                values.append(v)

        return whereStr, values