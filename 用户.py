from flask import Flask,session
import pymysql
import time
import hashlib
import random
from sql import 接口标准化
from sql import sqls,idtoken,tokenid,验证码判断
from sql import 手机验证
from sql import 短信
from sql import 视频地址解析
from sql import 批量视频解析

def url(name,data):
    if name=='getuserinfo':
        returndata = token(data)
    elif name=='text':
        returndata = 测试(data)
    elif name=='sms':
        returndata = 发短信(data)#
    elif name=='login':
        returndata = 登录(data)#
    elif name=='register':
        returndata = 注册(data)#
    elif name=='udateadd':
        returndata = 修改地址头像(data)
    elif name=='mycollection':
        returndata = 我的收藏(data)
        #收藏点赞需要核实
    elif name=='updatepassword':
        returndata = 修改密码(data)#
    elif name=='bank':
        returndata = 绑定银行卡(data)#
    elif name=='getbank':
        returndata = 获取银行信息(data)#
    elif name=='findpassword':
        returndata = 找回密码(data)#
    elif name == 'sign':
        returndata = 修改签名(data)
    else:
        returndata = "",-1,'你访问的接口不存在'
    returndata = 接口标准化(returndata)
    return returndata

def 测试(data):
    #钱包
    #安全
    return '',

def 修改签名(data):
    签名="UPDATE `dy`.`user` SET `sign` = '%s' WHERE `id` = %s" % (data['sign'],data['id'])
    签名=sqls(签名)
    if 签名=="sqlbug":
        return '',-1,'未找到id'
    else:
        return '',0,'签名修改成功'


def 找回密码(data):
    #判断手机是否注册
    查手机="select * from user where phone = '%s' " %(data['phone'])
    查手机=sqls(查手机)
    if len(查手机)!=1:
        return '',-1,'手机号不存在。'
    #判断验证码是否正确
    if 验证码判断(data['phone'],data['code'],3)<0:
        return '', -3, '验证码不正确'
    else:
        password = data['password']
        password = password.encode(encoding='utf-8')
        password = hashlib.md5(password).hexdigest()
        更新密码 = "UPDATE `user` SET `password` = '%s' WHERE `id` = %s" % (password, data['phone'])
        更新密码 = sqls(更新密码)
        if 更新密码 == "sqlbug":
            return '[]', -3, '修改失败'
        else:
            return '[]', 1, '修改成功'
    #修改密码


def 获取银行信息(data):
    查="select `username`, `bankname`,`bankaddress`, `bankcardno`,`alipay` from bank  where userid = %s order by id desc" % data['id']
    #bankCardNo: "", bankName: "", bankAddress: ""
    值=sqls(查)
    if 值 == "sqlbug":
        return '', -1,'token解析异常'
    if len(值)==0:
        空值=dict()
        空值['username']="未绑定"
        空值['bankname'] = "未绑定"
        空值['bankaddress'] = "未绑定"
        空值['bankcardno'] = "未绑定"
        空值['alipay'] = "未绑定"
        return 空值,0,''
    else:
        return 值[0],

def 绑定银行卡(data):
    if len(data['code'])!=6:
        return '',-1,"验证码错误"
    更新银行卡 = "INSERT INTO `dy`.`bank`(`userid`,`username`, `bankname`,`bankaddress`, `bankcardno`,`alipay`,type) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
            % (data['id'],data['username'],data['bankname'], data['bankaddress'],data['bankcardno'],data['alipay'],1)
    更新银行卡 = sqls(更新银行卡)
    if 更新银行卡=="sqlbug":
        return '', -1, '修改失败'
    else:
        return '',0,'银行卡修改成功'



def 修改密码(data):
    if len(data['code'])!=6:
        return '[]', -1, '验证码不正确'
    password = data['password']
    password = password.encode(encoding='utf-8')
    password = hashlib.md5(password).hexdigest()
    更新密码 = "UPDATE `user` SET `password` = '%s' WHERE `id` = %s" % (password, data['id'])
    更新密码 = sqls(更新密码)
    if 更新密码 == "sqlbug":
        return '[]', -3, '修改失败'
    else:
        return '[]', 1, '修改成功'

def 我的收藏(data):
    # 1收藏2点赞3举报4关注
    #获取收藏列表，名字，点赞数
    if data['type']=='1':
        收藏 = "select b.id as video,name,img,goodnum,b.type,b.video as getvideo from likes a left join video b on a.video = b.id where a.user = %s and type=1" \
             % (data['id'])
        结果 = sqls(收藏)
        结果 = 批量视频解析(结果)
    elif data['type']=='4':
        #用户名字，粉丝量，最新视频，点赞，视频总数。
        关注="select b.nick,b.fans,b.id from likes a left join user b on a.video = b.id where type =4 and a.user = %s;" % (data['id'])
        关注 = sqls(关注)
        结果=list()
        for a in 关注:
            查="select count(*) as videonum from video where user = %s;" % (a['id'])
            查=sqls(查)
            a.update(查[0])
            结果.append(a)
    return 结果,

def 修改地址头像(data):
    if data['type']=="1":
        更新头像="UPDATE `user` SET `nick` = '%s' WHERE `id` = %s" % (data['name'],data['id'])
        更新头像=sqls(更新头像)
        if 更新头像=="sqlbug":
            return '[]',-3,'修改失败'
        else:
            return '[]',1,'修改成功'
    elif data['type']=="2":
        password = data['password']
        password = password.encode(encoding='utf-8')
        password = hashlib.md5(password).hexdigest()
        更新密码 = "UPDATE `user` SET `password` = '%s' WHERE `id` = %s" % (password, data['id'])
        更新密码 = sqls(更新密码)
        if 更新密码 == "sqlbug":
            return '[]', -3, '修改失败'
        else:
            return '[]', 1, '修改成功'

def 登录(data):
    if data['password']==None or data['phone']==None:
        return '账号密码不能为空',-1
    if 手机验证(data['phone'])<0:
        return '手机格式不正确',-1
    password=data['password']
    password = password.encode(encoding='utf-8')
    password = hashlib.md5(password).hexdigest()
    登录="select id as token,phone,address,referrer,vip,gold,lasttime,authentication,picture,nick from user where phone = '%s' and password='%s'" % (data['phone'],password)
    登录=sqls(登录)
    if len(登录)>0:
        登录[0]['token']=idtoken(登录[0]['token'])
        return 登录,
    else:
        return "[]",-1,"账号密码错误"

def 注册(data):
    if 手机验证(data['phone'])<0:
        return '手机格式不正确',-1
    if len(data['referrer'])== 0:
        推荐人 = None
    else:
        data['referrer']=int(data['referrer'])-168000
        查询="select * from user where id = '%s' " % (data['referrer'])
        查询 = sqls(查询)
        if len(查询)==0:
            return '',-1,"推荐人不存在"
        else:
            推荐人=data['referrer']
    if 验证码判断(data['phone'], data['code'],1) < 0:
        return '', -3, '验证码不正确'
    password = data['password']
    password = password.encode(encoding='utf-8')
    password = hashlib.md5(password).hexdigest()
    注册= "INSERT INTO `user` (`phone`, `password`, `address`, `referrer`, `vip`, `nick`,`picture`,`province`,`city`,`area`) VALUES ('%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s');"% \
        (data['phone'],password,data['address'],推荐人,1,'抖云会员',"https://douyunzhibo.oss-cn-chengdu.aliyuncs.com/index/%E5%A4%B4%E5%83%8F1.jpg",data['province'],data['city'],data['area'])
    注册 = sqls(注册)
    sqls("UPDATE `dy`.`smscode` SET `state` = '2' WHERE phone = %s and type =1" % (data['phone']))
    token={}
    token['token']=idtoken(注册[0]['id'])
    return token,0,'恭喜您注册成功，实名认证之后获取更多收益。'

def token(data):
    查="select id as token,phone,address,referrer,vip,gold,lasttime,authentication,picture,nick,sign from user where id = '%s'" % data['id']
    查=sqls(查)
    if len(查)==0:
        return '[]',-2,'用户id异常，请查询是否异常。'
    else:
        查[0]['userid'] = int(查[0]['token'])+168000
        查[0]['token']=idtoken(查[0]['token'])
    return 查,


def 发短信(data):
    if int(data['type'])==1:
        查询=sqls("select count(*) as n from user where phone = %s" % data['tel'])
        if 查询[0]['n']>0:
            return data['tel']+'已注册',-1,'手机号已注册。'
    elif int(data['type'])==3:
        查询=sqls("select count(*) as n from user where phone = %s" % data['tel'])
        if 查询[0]['n']==0:
            return data['tel']+'不存在',-1,'手机号尚未注册。'
    code = random.randrange(100000, 999999)
    sqls("UPDATE `dy`.`smscode` SET `state` = '2' WHERE phone = %s" % (data['tel']))
    sqls("INSERT INTO `dy`.`smscode`(`code`, `type`, `phone`, `time`, `state`) VALUES ('%s', '%s', '%s', NOW(), '1')" % (code,data['type'],data['tel']))
    a = 短信(data['tel'], int(data['type']), code)
    return a,0,"验证码发送成功"





