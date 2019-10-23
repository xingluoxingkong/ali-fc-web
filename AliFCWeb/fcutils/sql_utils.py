import json
from .utils import dataToStr

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
        return: (' `name`=%  ,  `age`=s ', ['张三', '18'])
    """
    l1 = []
    lper = []
    l2 = []
    for k, v in d.items():
        if v != None:
            l1.append(k)
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