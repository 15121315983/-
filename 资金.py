import json
import pymysql
import time
import hashlib
import random
from sql import 接口标准化
from sql import sqls,idtoken,tokenid
from sql import 手机验证
from sql import 短信
from sql import 视频地址解析
from sql import 批量视频解析
import requests,urllib
import sql

def url(name,data):
    if name=='text':
        returndata = 测试(data)
    elif name=='yearcard':
        returndata = 年卡购买(data)
        # 重复购买续费提示，购买后增加vip等级
    elif name=='goldshop':
        returndata = 金币购买(data)
    elif name == 'alipayreturn':
        returndata = 支付宝回调(data)
        #年卡会员修改年卡
        #商品和充值修改商品订单状态
        #修正
    elif name == 'activenoshop':
        returndata = 使用激活码(data)
    elif name == 'curgold':
        returndata = 更新金币(data)
        #生成金币列表
    elif name == 'withdraw':
        returndata = 提现接口(data)
    elif name == 'recharge':
        returndata = 充值接口(data)
    elif name == 'rechargerecord':
        returndata = 充值记录查询(data)
        #生成提现记录
    else:
        returndata = "",-1,'你访问的接口不存在'
    returndata = 接口标准化(returndata)
    return returndata

def 测试(data):
    #钱包
    return '',

def 修改签名(data):
    签名="UPDATE `dy`.`user` SET `sign` = '%s' WHERE `id` = %s" % (data['sign'],data['id'])
    签名=sqls(签名)
    if 签名=="sqlbug":
        return '',-1,'未找到id'
    else:
        return '',0,'修改成功'

def 充值接口(data):
    name = "抖云充值"
    goodid = sql.goodid(data['id'])
    #goodid = "2019111118282550016571600001"
    money = data['money']
    goodinfo = "1元等于1金币"
    url="http://pay.dyzbed.com/wappay/apppay.php?goodid=%s&name=%s&goodinfo=%s&money=%s"  %(goodid,name,goodinfo,money)
    url = requests.get(url)
    url = url.text.replace("&amp;", "&");
    goodname="充值金币"
    增 = "INSERT INTO `dy`.`orderid`(`orderid`, `userid`, `goodname`, `money`, `type`, `status`, `pay`,`time`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s',NOW())" \
        % (goodid, data['id'], goodname, money, '支付中', 1,'支付宝')
    增 = sqls(增)
    return url,

def 支付接口生成(goodiname,goodid,money,goodinfo):
    #商户订单号，订单名称，付款金额，商品描述
    url="http://pay.dyzbed.com/wappay/pay.php?goodid=%s&goodiname=%s&goodinfo=%s&money=%s"  %(goodid,goodiname,goodinfo,money)
    return url,

def 年卡购买(data):
    name = "抖云智播年卡会员"
    goodid = sql.goodid(data['id'])
    money = 365
    goodinfo = "可以在一年之内免费观看抖云智播的所有视频"
    url = "http://pay.dyzbed.com/wappay/apppay.php?goodid=%s&name=%s&goodinfo=%s&money=%s" % (goodid, name, goodinfo, money)
    url = requests.get(url)
    url = url.text.replace("&amp;", "&");
    goodname = "充值金币"
    增 = "INSERT INTO `dy`.`orderid`(`orderid`, `userid`, `goodname`, `money`, `type`, `status`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" \
        % (goodid, data['id'], goodname, money, '支付中', 1)
    增 = sqls(增)
    #生成未付款订单
    return url,


def 支付宝回调(data):
    #根据订单号核实相关信息 http://pay.dyzbed.com/wappay/query.php?goodid=2019110910411229728051600001
    print(data['notify_time'])  # 通知的发送时间。格式为yyyy-MM-dd HH:mm:ss
    print(data['app_id'])  # 支付宝分配给开发者的应用Id
    print(data['sign'])  # 	签名
    print(data['trade_no']) # 支付宝交易号
    print(data['out_trade_no']) # 商户订单号
    print(data['buyer_id']) # 买家支付宝用户号
    print(data['trade_status']) # 交易状态
    print(data['total_amount']) # 订单金额
    print(data['receipt_amount']) # 实收金额
    print(data['buyer_pay_amount']) # 付款金额
    print(data['subject']) # 订单标题
    print(data['body'])  # 商品描述
    print(data['fund_bill_list'])  # 支付金额信息
    #print(data['timestamp'])
    if data['app_id']=="2019092667885024":
        #订单信息录入数据库
        增="INSERT INTO `dy`.`alipay`(`app_id`, `trade_no`, `out_trade_no`, `sign`, `buyer_id`, `trade_status`, `total_amount`, `receipt_amount`, `buyer_pay_amount`, `subject`, `body`, `fund_bill_list`, `statr`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
          %(data['app_id'],data['trade_no'],data['out_trade_no'],data['sign'],data['buyer_id'],data['trade_status'],data['total_amount'],data['receipt_amount'],data['buyer_pay_amount'],data['subject'],data['body'],data['fund_bill_list'],1)
        增 = sqls(增)
        订单成功="UPDATE `dy`.`orderid` SET `type` = '支付成功' WHERE `orderid` = '%s'" % (data['out_trade_no'])
        订单成功 = sqls(订单成功)
        return "恭喜支付成功",
    else:
        return "支付商户异常",-501,'订单异常'

def 金币购买(data):
    #type=1 金币购买，2提现，3充值
    if data['goodid']=="1":
        m=365
    else:
        return '',-1,'商品信息错误'
    gold=增剪金额(m,data['id'],'减金币')
    if gold>=0:

        改="UPDATE `dy`.`user` SET `vip` = 3,WHERE `id` = 25"
        改=sqls(改)
        return gold,0,'购买成功'
    else:
        return gold,-1,'金币不足购买失败'

def 使用激活码(data):
    print(data)
    查 = "select * from code where state = 1 and code = '%s'" % (data['code'])
    查 = sqls(查)
    if len(查)==1:
        改="UPDATE `dy`.`code` SET `useuser` = '%s', `state` = '2'" % (data['id'])
        sqls(改)
        return '',0,'购买成功'
    else:
        return '',-1,'激活码不正确或者已经被使用'

def 更新金币(data):
    return sqls("select gold from user where id = %s" % data['id'])[0],

def 提现接口(data):
    #金额，token,支付宝，号码，银行卡，
    gold=增剪金额(data['gold'],data['id'],'减金币')
    if gold>=0:
        return gold,0,'申请成功，银行会在24小时内处理'
    else:
        return gold,-1,'您的余额不足'

def 提现记录查询():
    # 时间，类目，金额，类型，结果
    pass

def 充值记录查询(data):
    #时间，类目，金额，类型
    查= "SELECT goodname,money,time,pay FROM `dy`.`orderid` where userid = %s and type = '支付成功'"% data['id']
    查=sqls(查)
    return 查,

def 收益查询():
    pass

def 增剪金额(num,userid,type):
    if type=="增金币":
        增="UPDATE `dy`.`user` SET `gold` =`gold`+ '%s' WHERE `id` = %s" % (num,userid)
    elif type == "增积分":
        增 = "UPDATE `dy`.`user` SET `gold` =`gold`+ '%s' WHERE `id` = %s" % (num, userid)
    elif type == "减金币":
        usergold = "select gold from user where id = %s;" % (userid)
        usergold=sqls(usergold)
        print(usergold[0]['gold'])
        g = int(usergold[0]['gold']) - int(num)
        if g>=0:
            提现 = "UPDATE `dy`.`user` SET `gold` = '%s' WHERE `id` = %s;" % (g,userid)
            提现 = sqls(提现)
            return g
        else:
            return g

