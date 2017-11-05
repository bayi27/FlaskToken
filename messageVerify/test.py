# coding:utf-8
import redis
import random

phonenumber=188888888
#这里可以利用正则过滤一下电话号码,比如：
#/^(13[0-9]|14[5-9]|15[0-9]|16[6]|17[0-8]|18[0-9]|19[8-9])\d{8}$/

conn=redis.StrictRedis(host='127.0.0.1',port=6379)
pipe=conn.pipeline()

def producCode():
	verifyCode=str(random.randint(100000,999999))

	pipe.set("phone%s"%phonenumber,verifyCode)
	pipe.expire("phone%s"%phonenumber,60) #设置过期时间一分钟
	pipe.execute()

def checkCode():
	pipe.set('postNum%s'%phonenumber,'0')
	validate_number = request.get_json().get('validate_number')
	pipe.incr('postNum%s'%phonenumber) #记录提交次数防止爆破
	if conn.get('postNum%s'%phonenumber)>3:
		pass
	...
	if validate_number != validate_number_in_redis:
		return jsonify({'code': 0, 'message': '验证没有通过'})
	pipe.set('is_validate:%s' % phone_number, '1') #通过验证码设置value为1
	pipe.expire('is_validate:%s' % phone_number, 120)
	pipe.execute()

	return jsonify({'code': 1, 'message': '验证通过'})
def postMessage():
	result=conn.get("phone%s"%phonenumber)
	#此时如果通过验证码,result为1,否则为0
	...
	#剩下的其他操作
	
#前辈具体文章http://www.cnblogs.com/yueerwanwan0204/p/5460668.html	