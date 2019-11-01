
_aaa = {'a':'bbb'}


@property
def a():
    return _aaa['a']

@a.setter
def a(v):
    _aaa['a'] = v


if __name__ == "__main__":
    print(a)
    a = 'aaa'
    print(a)
