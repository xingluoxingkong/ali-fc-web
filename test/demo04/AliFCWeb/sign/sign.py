import abc
import json
import importlib

__all__ = ['Sign', 'DBSign', 'RedisSign']

class Sign(metaclass = abc.ABCMeta):

    def __init__(self, func, *args, **kw):
        ''' 用于全局变量的赋值，使用时继承该类并在replace方法中书写实际的运行方法
        --
        '''
        self.func = func
        self.args = args
        self.kw = kw

    @abc.abstractmethod
    def replace(self):
        ''' 覆盖此方法，实际运行时会调用该方法以替换掉被标记的方法
        --
        '''
        pass

