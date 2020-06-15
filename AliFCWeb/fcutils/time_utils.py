import datetime


def getNow():
    ''' 获取当前时间
    --
    '''
    return datetime.datetime.now() + datetime.timedelta(hours=8)


def getToday():
    ''' 获取当前日期
    --
    '''
    return (datetime.datetime.now() + datetime.timedelta(hours=8)).date()