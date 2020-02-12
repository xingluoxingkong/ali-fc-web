__all__ = ['Dict2XML']


class Dict2XML(object):

    def __init__(self, coding='UTF-8'):
        self.coding = coding

    def parse(self, data):
        xmlStr = ''
        if isinstance(data, dict):
            data = data.items()
        for k, v in data:
            if isinstance(v, str):
                xmlStr += '<' + k + '>'
                xmlStr += v.strip().encode(self.coding).decode(
                    self.coding)
                xmlStr += '</' + k + '>'
            elif isinstance(v, list):
                ks = [k for i in range(len(v))]
                cData = zip(ks, v)
                xmlStr += self.parse(cData)
            elif isinstance(v, dict):
                xmlStr += '<' + k + '>'
                xmlStr += self.parse(v)
                xmlStr += '</' + k + '>'
            else:
                xmlStr += ''

        return xmlStr
