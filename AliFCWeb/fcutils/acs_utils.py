######################################
#
# 阿里云短信验证
#
######################################
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

__all__ = ['sendMessage']


def sendMessage(accessKeyId, accessSecret, phoneNumbers, signName, templateCode, templateParam=None):
    ''' 发送短信
    --
        @param accessKeyId: accessKeyId
        @param accessSecret: accessSecret
        @param phoneNumbers: 接收短信的手机号码。
                                格式：
                                    国内短信：11位手机号码，例如15951955195。
                                    国际/港澳台消息：国际区号+号码，例如85200000000。
                                    支持对多个手机号码发送短信，手机号码之间以英文逗号（,）分隔。上限为1000个手机号码。批量调用相对于单条调用及时性稍有延迟。
                                    验证码类型短信，建议使用单独发送的方式。
        @param signName: 短信签名名称。请在控制台签名管理页面签名名称一列查看。
        @param templateCode: 短信模板ID。请在控制台模板管理页面模板CODE一列查看。
        @param templateParam: 短信模板变量对应的实际值，JSON格式。 
                                类型：
                                    1. 单个普通字符串，会默认以code封装
                                    2. json格式的字符串。如："{\"code\":\"abcd\"}"
                                    3. 字典或列表
    '''
    tp = {}
    if isinstance(templateParam, str):
        if templateParam[0] == '{' and templateParam[-1] == '}':
            tp = templateParam
        else:
            tp = json.dumps({'code': templateParam})
    elif isinstance(templateParam, dict):
        tp = json.dumps(templateParam)
    # else:
    #     return None

    client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phoneNumbers)
    request.add_query_param('SignName', signName)
    request.add_query_param('TemplateCode', templateCode)
    if tp:
        request.add_query_param('TemplateParam', tp)
    response = client.do_action(request)
    return response
