import json

def dataToJson(data):
    """ 把list和dict中的所有元素转换成json库能识别的对象（如Decimal和日期类型转化为字符串）。 传入其他类型的数据转化成string返回
    --
        @param data 要格式化的数据

        @return list, dict 或 str类型
    """
    if data == None:
        return data
    elif isinstance(data, str):
        if data.startswith('{') and data.endswith('}') or data.startswith('[') and data.endswith(']'):
            try:
                return json.loads(data.replace("'", '"'))
            except :
                return data
        return data
    elif isinstance(data, list):
        for item in data:
            item = dataToJson(item)
        return data
    elif isinstance(data, dict):
        for k, v in data.items():
            data[k] = dataToJson(v)
        return data
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
    
    return str(data)