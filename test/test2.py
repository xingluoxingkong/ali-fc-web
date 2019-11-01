from test import getA, getDict, setA, setDict

if __name__ == "__main__":
    print(getA())
    setA('bbb')
    print(getA())
    setDict('c', 'ccc')
    print(getDict('c'))