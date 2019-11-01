#################################
#
# 常量文件，改一次增加一次版本号
# 版本号：6
#
#################################
#######################通用的的常量#######################
OK = '1'
NO = '0'
ALL = '-1'
CONF_HOST = 'https://1921668875657123.cn-zhangjiakou.fc.aliyuncs.com/2016-08-15/proxy/ly-config/getConfigByName/'
#######################支付相关的常量#######################
# 支付回调地址
NOTIFY_URL = 'https://1837732264572668.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/ly-order/notifyPay/'
# 支付宝扫码支付
ALI_QRCODE_PAY = 'A01'
# 微信小程序支付
WX_MINI_PROGRAM_PAY = 'W06'
# 通联支付返回码 —— 成功
PAY_SUCCESS = '0000'
# 通联支付返回码 —— 2开头表示交易进行中
PAY_ING = '2'
# 通联支付返回码 —— 3开头表示交易出错
PAY_ERROR = '3'

#######################订单相关的常量#######################
# 订单状态
# ly_order_status表status字段
## 未付款
NOT_PAY = '1'
## 待发货
WAIT_SEND = '2'
## 待确认收货
WAIT_CONFIRM_SEND = '3'
## 待二次确认
WAIT_SECOND_CONFIRM = '4'
## 待确认退款
WAIT_CONFIRM_REFUND = '5'
## 交易成功
TRANSACTION_SUCCESS = '6'
## 待退款
WAIT_REFUND = '7'
## 交易关闭
TRANSACTION_CLOSE = '8'
## 待评价
WAIT_COMMENT = '9'
## 评价完成
ORDER_COMMENT_SUCCESS = '10'

# 我购买的
MY_PAY = 'A01'
# 我卖出的
MY_SELL = 'B01'

#######################订单支付相关的常量#######################
# ly_pay_log表，status字段
# 支付
PAY_STATUS_PAY = '1'
# 撤销（全额退款）
PAY_STATUS_CANCEL = '2'
# 退款（部分或全部）
PAY_STATUS_REFUND = '3'

# ly_pay_log表，retcode字段
# 发起交易
PAY_RETCODE_READY = '1'
# 交易成功
PAY_RETCODE_SUCCESS = '2'
# 交易失败
PAY_RETCODE_ERROR = '3'

# 类型。0：商家；1：用户
PEOPLE_TYPE_CUSTOMER = '1'
PEOPLE_TYPE_SELLER = '0'

#######################商品相关的常量#######################
# ly_spu表的audit_status
# 正常
AUDIT_STATUS_OK = '1'
# 非正常
AUDIT_STATUS_BAD = '0'
# 缺货
AUDIT_STATUS_OUT = '2'

# ly_spk表的marketable
# 上架
MARKETABLE_OK = '1'
# 下架
MARKETABLE_BAD = '0'
# 等待上架
MARKETABLE_WAIT = '2'

# ly_spu表realname
# 需要实名下单
REALNAME_OK = '1'
# 不需要实名下单
REALNAME_BAD = '0'

#######################订单相关的常量#######################
# ly_order表customer_type
CUSTOMER_TYPE_USER = '1'
CUSTOMER_TYPE_SELLER = '0'

#######################优惠券相关的常量#######################
# 满减
COUPON_TYPE_REDUCE = '1'
# 折扣
COUPON_TYPE_DISCOUNT = '2'
# 未到使用时间
DATETIME_NOT = '0'
# 正常
DATETIME_ING = '1'
# 过期
DATETIME_EXP = '2'

#######################导游接团相关的常量#######################
# 0：等待接受；1：已接受未结工资；2：已取消; 3：取消确认中；4:已结工资
GUIDE_STATUS_WAIT = '0'
GUIDE_STATUS_ING = '1'
GUIDE_STATUS_CLOSE = '2'
GUIDE_STATUS_CLOSE_ING = '3'
GUIDE_STATUS_FINISH = '4'
#######################签到相关的常量#######################
# ly_trip_clock_in的status字段0：创建；1：完成
TRIP_CLOCK_IN__STATUS_CREATE = '0'
TRIP_CLOCK_IN__STATUS_FINISH = '1'
#######################二维码相关的常量#######################
# 0:导游码，1：商品码
QRCODE_TYPE_GUIDE = '0'
QRCODE_TYPE_GOODS = '1'