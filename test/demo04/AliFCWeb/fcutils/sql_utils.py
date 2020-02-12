import json

__all__ = ['joinList', 'pers', 'fieldStrFromList',
           'fieldStr', 'fieldStrAndPer',
           'fieldSplit', 'toJson', 'dataToJson',
           'dataToStr', 'dataToFloat']

def joinList(arr, prefix = '`', suffix = '`', delimiter=' , '):
    """ 用指定的分隔符连接数组，可以加上特定前缀和后缀
    --
        @example
            joinList(['a', 'b'])
        return: `a`, `b`
    
        @example 
            joinList(['a', 'b', 'c'], '"%', '%"', ' AND ')
        return: "%a%" AND "%b%" AND "%c%"
    
        @param arr: 数组
        @param prefix: 前缀，默认使用“`”
        @param suffix: 后缀，默认使用“`”
        @param delimiter: 分隔符，默认使用“ , ”
    """
    return delimiter.join(prefix + dataToStr(a) + suffix for a in arr)

def pers(n):
    """ 返回指定数量的%s，中间用逗号隔开
    --
        @example
            pers(5)
        return: %s, %s, %s, %s, %s

    """
    return ', '.join(['%s' for i in range(n)])

def fieldStrFromList(a, b, vPrefix = "'", vSuffix = "'", delimiter=' , '):
    """ 把两个列表拼成  `k1`="v1",`k2`="v2"... 形式的字符串
    --
        @example 
            fieldStrFromList(['name', 'age'], ['张三', 18])
        return: `name`="张三" , `age`="18"
    
        @example 
            fieldStrFromList(['a', 'b', 'c'],[1, 2, 3], '"%', '%"', ' AND ')
        return `a`="%1%"  AND  `b`="%2%"  AND  `c`="%3%"
    """
    c = list(zip(a, b))
    arr = [' `' + str(k) + '`=' + vPrefix + dataToStr(v) + vSuffix + ' ' for k, v in c if v != None]
    return joinList(arr, prefix = '', suffix = '', delimiter = delimiter)

def fieldStr(d, vPrefix = "'", vSuffix = "'", delimiter=' , '):
    """ 把字典中所有非空字段拼成 `k1`="v1",`k2`="v2"... 形式的字符串 
    --
        @example 
            fieldStr({'name':'张三', 'age':18})
        return: `name`="张三", `age`="18"
    
        @example 
            fieldStr({'a':1, 'b':2, 'c':3}, '"%', '%"', ' AND ')
        return: `a`="%1%"  AND  `b`="%2%"  AND  `c`="%3%"
    """
    arr = [' `' + str(k) + '`=' + vPrefix + dataToStr(v) + vSuffix + ' ' for k, v in d.items() if v != None]
    return joinList(arr, prefix = '', suffix = '', delimiter = delimiter)

def fieldStrAndPer(d):
    """ 把字典中所有非空字段拼成 `k1`=%s, `k2`=%s...和[v1, v2...]两个字段
    --
        @example
            fieldStrAndPer({'name':'张三', 'age':18})
        return: (' `name`=%s  ,  `age`=%s ', ['张三', '18'])
    """
    l1 = []
    lper = []
    l2 = []
    for k, v in d.items():
        if v != None:
            l1.append(k)
            noAppend = True # 标记lper和l2还未赋值
            if isinstance(v, str):
                if v.startswith('+') or v.startswith('-') or v.startswith('*') or v.startswith('/'):
                    vv = dataToFloat(v[1:])
                    if vv:
                        noAppend = False
                        lper.append('{}{}%s'.format(k, v[:1]))
                        l2.append(vv)
            if noAppend:
                lper.append('%s')
                l2.append(dataToStr(v))

    return fieldStrFromList(l1, lper, vPrefix='', vSuffix=''), l2

def fieldSplit(d):
    """ 把字典中所有非空字段拼成 "`k1`,`k2`..."","%s, %s..." 两个字符串 和 "v1","v2"... 列表
    --
        @example 
        	fieldSplit({'name':'张三', 'age':None, 'aaa':'bbb'})
        return: ("`name`, `aaa`", "%s, %s", ["张三", "bbb"])
    """
    l1 = []
    l2 = []
    for k, v in d.items():
        if v != None:
            l1.append(k)
            l2.append(dataToStr(v))

    return joinList(l1), pers(len(l2)), l2

def toJson(data):
    """ json强制转化方法
    """
    try:
        return json.loads(data.replace("'", '"'))
    except Exception as e:
        return {}

def dataToJson(data):
    """ 把list和dict中的所有元素转换成json库能识别的对象（如Decimal和日期类型转化为字符串）。 传入其他类型的数据转化成string返回
    --
        @param data 要格式化的数据

        @return list, dict 或 str类型
    """
    from collections import OrderedDict
    if isinstance(data, OrderedDict):
        data = dict(data)
    from decimal import Decimal
    if data == None or isinstance(data, int) or isinstance(data, float) or isinstance(data, bool):
        return data
    elif isinstance(data, str):
        if data.startswith('{') and data.endswith('}') or data.startswith('[') and data.endswith(']'):
            try:
                return json.loads(data.replace("'", '"'))
            except :
                return data
        return data
    elif isinstance(data, list) or isinstance(data, tuple):
        newList = []
        for item in data:
            newList.append(dataToJson(item))
        return newList
    elif isinstance(data, dict):
        for k, v in data.items():
            data[k] = dataToJson(v)
        return data
    elif isinstance(data, Decimal):
        return float(data)
    else:
        return str(data)

def dataToStr(data):
    """ 把list和dict中的所有元素转换成字符串
    --
        @param data 要格式化的数据

        @return 如果是对象转换成json字符串，其他类型转换成str
    """
    if isinstance(data, list) or isinstance(data, dict):
        return json.dumps(dataToJson(data))
    
    if isinstance(data, int) or isinstance(data, float):
        return data
    
    if not data:
        return ''
    
    return str(data)

def dataToFloat(data):
    try:
        return float(data)
    except Exception as e:
        return False
