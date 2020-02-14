from AliFCWeb.sign import Sign

class MySign(Sign):
    
    def replace(self):
        from AliFCWeb.constant import getConfByName, FC_ENVIRON
        environ = getConfByName(FC_ENVIRON)

        return environ['fc.request_uri']