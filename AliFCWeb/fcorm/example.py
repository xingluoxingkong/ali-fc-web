from AliFCWeb.fcutils import pers

__all__ = ['Example']


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

    def whereFromStr(self, whereStr):
        ''' 直接从字符串中读取where条件，暂不支持带子查询的语句
        --
        '''
        import re
        keyword = ''
        # 前面是否有NOT关键字
        haveNot = False
        # 圆括号
        parentheses = False
        # 符号
        sign = ''
        key = ''
        value = ''
        whereSplit = re.split(r'\s+', whereStr.strip())
        for s in whereSplit:
            if (s.upper() == 'AND' or s.upper() == 'OR') and not parentheses:
                if sign and (sign.upper() == 'BETWEEN' or sign.upper() == 'NOT BETWEEN'):
                    continue
                keyword = s.upper()
                continue

            if s.startswith('('):
                parentheses = True
                if len(s) > 1:
                    s = s[1:]
                else:
                    continue

            if parentheses:
                if s.endswith(')'):
                    if len(s) > 1:
                        value += s[:-1]
                else:
                    value += s + ' '
                    continue
            else:
                if s.upper() == 'NOT':
                    haveNot = True
                    continue
                elif s.upper() == 'IN' or s.upper() == 'LIKE' or s.upper() == 'BETWEEN':
                    if haveNot:
                        sign = 'NOT ' + s
                    else:
                        sign = s
                    continue
                else:
                    s = s.replace('`', '')
                    if '=' in s and '=' != s:
                        sign = '='
                        key, value = s.split('=')
                    elif '<>' in s and '<>' != s:
                        sign = '<>'
                        key, value = s.split('<>')
                    elif '>' in s and '>' != s:
                        sign = '>'
                        key, value = s.split('>')
                    elif '<' in s and '<' != s:
                        sign = '<'
                        key, value = s.split('<')
                    elif '>=' in s and '>=' != s:
                        sign = '>='
                        key, value = s.split('>=')
                    elif '<=' in s and '<=' != s:
                        sign = '<='
                        key, value = s.split('<=')
                    else:
                        if sign and key:
                            if sign.upper() == 'BETWEEN' or sign.upper() == 'NOT BETWEEN':
                                if value:
                                    value.append(s)
                                else:
                                    value = [s]
                                    continue
                            else:
                                value = s
                        elif key:
                            sign = s
                            continue
                        else:
                            key = s
                            continue

            if not sign:
                self._append(keyword, Example().whereFromStr(value))
            elif sign.upper() == 'IN' or sign.upper() == 'NOT IN':
                import json
                value = json.loads('[' + value + ']')
                print(type(value))
                print((keyword, (key, value, sign)))
                self._append(keyword, (key, value, sign))
            else:
                if isinstance(value, str) and value.startswith('"') and value.endswith('"') and len(value) > 1:
                    value = value[1:-1]
                value = value
                self._append(keyword, (key, value, sign))
            sign = ''
            key = ''
            value = ''
            haveNot = False
            parentheses = False
            keyword = ''
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
                    k = '`' + kSplit[0] + '`.`' + kSplit[1] + '`'
            else:
                k = '`' + k + '`'
            if p.upper() == 'IN' or p.upper() == 'NOT IN':
                whereStr = ' ' + k + ' ' + p.upper() + ' (' + pers(len(v)) + ') '
                return whereStr, v
            elif p.upper() == 'BETWEEN' or p.upper() == 'NOT BETWEEN':
                whereStr = ' ' + k + ' ' + p.upper() + ' %s AND %s '
                return whereStr, v
            else:
                whereStr = ' ' + k + ' ' + p.upper() + ' %s '
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

    def __str__(self):
        return str(self.whereBuilder())
