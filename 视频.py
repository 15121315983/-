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

def url(name,data):
    if name=='test':
        returndata = 测试(data)
    elif name=='myvideo':
        returndata = 我的视频(data)
    elif name=='videolist':
        returndata = 批量获取视频(data)
    elif name=='videoaouthor':
        returndata = 主播首页(data)
    else:
        returndata = "",-1,'你访问的接口不存在'
    returndata = 接口标准化(returndata)
    return returndata

def 测试(data):

    return '123',

def 我的视频(data):
    print(data)
    查="select looknum,goodnum,name,time,video as videourl,id as videoid from video where user = %s and state = 1" % data['id']
    查=sqls(查)
    查=批量视频解析(查)
    return 查,

def 主播首页(data):
    print(data)
    查="select looknum,goodnum,name,time,video as videourl,id as videoid from video where user = %s and state = 1" % data['id']
    查=sqls(查)
    查=批量视频解析(查)
    作者=list()
    作者信息="select nick,phone,sign,fans,picture from user"
    作者信息=sqls(作者信息)
    作者['user']=作者信息
    作者['video']=查
    return 作者,

def 批量获取视频(data):
    标签=data['type']
    页码=int(data['page'])
    每页数=int(data['num'])
    查="Select a.id as videoid,name,video as videourl,looknum,goodnum,nick as author from video a, user b where ( a.user=b.id ) and type in (select name from type where type in  (select name from type where type = '%s')) LIMIT %s,%s" \
      % (标签,(页码-1)*每页数,每页数)
    print(查)
    查=sqls(查)
    查 = 批量视频解析(查)
    return 查,