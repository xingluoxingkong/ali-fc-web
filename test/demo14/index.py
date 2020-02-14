import json
import logging

from AliFCWeb.fcorm import Orm, Example
from AliFCWeb import fcIndex, get, post, put, delete, mysqlConn, ResponseEntity

_log = logging.getLogger()
_conn = mysqlConn


@fcIndex(debug=True)
def handler(environ, start_response):
    pass


@get()
def testFC(data):
    try:
        res = testFC1(data)
        _conn.commit()
        return res
    except Exception as e:
        _conn.rollback()
        _log.error(e)
        return ResponseEntity.badRequest(e)

def testFC1(data):
    # 关闭自动提交
    userOrm = Orm(_conn, 'user', auto_commit=False)
    houseOrm = Orm(_conn, 'house', auto_commit=False)
    
    print('==============插入数据==============')
    userId = userOrm.insertData({'name':'张三', 'age':18})
    houseOrm.insertData(['user_id', 'address', 'price'], 
                        [[userId, '成都市武侯区', 100],
                         [userId, '成都市高新区', 200],
                         [userId, '北京市东城区', 300],
                         [userId, '北京市西城区', 400],
                         [userId, '北京市朝阳区', 500]])
    
    print('==============所有user数据==============')
    users = userOrm.selectAll()
    print(users)
    
    print('==============所有house数据==============')
    houses = houseOrm.selectAll()
    print(houses)
    
    print('==============所有位于成都的house数据==============')
    houses = houseOrm.selectByExample(Example().andLike('address', '成都%'))
    print(houses)
    
    print('==============所有不在成都的house数据==============')
    houses = houseOrm.selectByExample(Example().andNotLike('address', '成都%'))
    print(houses)
    
    print('==============所有user_id为1的house数据==============')
    houses = houseOrm.selectByExample(Example().andEqualTo({'user_id': 1}))
    print(houses)
    
    print('==============连接查询==============')
    userOrm.leftJoin('house', 'house.user_id=user.id')
    houses = userOrm.selectByExample(Example().andEqualTo({'price': 100}))
    print(houses)
    
    print('==============清除缓存==============')
    userOrm.clear()
    
    print('==============所有售价大于200小于400的house数据==============')
    houses = houseOrm.selectByExample(Example().andBetween('price', 200, 400))
    print(houses)
    
    print('==============所有北京的房子涨价10==============')
    houseOrm.updateByExample({'price': '+10'}, Example().andLike('address', '北京%'))
    houses = houseOrm.selectAll()
    print(houses)
    
    print('==============分页查询==============')
    num, houses = houseOrm.selectPageByExample(Example().andEqualTo({'user_id': userId}), 2, 3)
    print('符合条件的总条数：{}'.format(num))
    print('本页数据：')
    print(houses)
    
    print('==============多值查询==============')
    houses = houseOrm.selectByExample(Example().andInValues('price', [100, 200]))
    print(houses)
    
    return ResponseEntity.ok('请查看控制台日志')
