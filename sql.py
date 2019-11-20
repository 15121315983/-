import json
import pymysql
import pymysql.cursors
import re
import time
import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
#阿里云帮助文档 https://help.aliyun.com/document_detail/53090.html?spm=a2c1g.8271268.10000.119.6f2ddf25TKEage
import os


import ali


def 视频地址解析(videoid):
    try:
        clt=ali.init_vod_client(None,None)
        data = ali.get_play_info(clt,videoid)
    except Exception as e:
        print(e)
        data=None
    return data

def 批量视频解析(data):
    clt = ali.init_vod_client(None, None)
    结果=list()
    for i in data:
        try:
            查=ali.get_video_info(clt,i['videourl'])
            i['videoimg']=查['Video']['CoverURL']
            结果.append(i)
        except Exception as e:
            print(e)
    return 结果

#根据id时间随机生成订单号
def goodid(userid):
    userid=userid+1600000
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]+str(userid)
    return order_no


def sqls(sql):
    db = pymysql.connect(
        host="47.106.156.241",
        user="douyun",
        passwd="douyun1024",
        db="dy",
        port=3306,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    # print(sql)
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
        if sql[0:6]=="INSERT" or sql[0:6]=="insert" or sql[0:6]=="UPDATE" or sql[0:6]=="update":
            re = db.cursor()
            re.execute("SELECT LAST_INSERT_ID() as id;")
            result = re.fetchall()
        # print(result)
        db.close()
    except:
        cursor.close()
        print(sql)
        return 'sqlbug'
    else:
        # print('sql结束')
        #print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        #print(sql)
        return result

def 接口标准化(data):
    if data==None:
        datas=''
        success = True
        code = 0
        message = '通讯正常'
    elif len(data)==1:
        datas=data[0]
        success = True
        code = len(data[0])
        message = '通讯正常'
    elif len(data)==2:
        datas = data[0]
        code = data[1]
        success = False
        message = '业务错误'
    elif len(data)==3:
        datas = data[0]
        code = data[1]
        success = False
        message = data[2]
    返回值= {'code':code,'success':success,'message':message,'data':datas}
    返回值 = json.dumps(返回值)
    print(返回值)
    return 返回值

def 输入处理(get,data):
    #循环判定是否为空
    pass

def 短信(tel,type,code):
    client = AcsClient('LTAI4FsswRJma4LNZrNPNyrs', 'YmYYLxGc3GupseZzNc7GTkIESAuGa1', 'cn-hangzhou')
    if type == 1:
        短信签名 = "SMS_176526266" #1注册短信
    elif type ==2:
        短信签名 = "SMS_176410120" #2修改密码
    elif type == 3:
        短信签名 = "SMS_176410120"  #3修改密码
    else:
        短信签名 = "SMS_176526266"
    codes={'code':code}
    codes= json.dumps(codes)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('http')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', tel)
    request.add_query_param('SignName', "抖云")
    request.add_query_param('TemplateCode', 短信签名)
    request.add_query_param('TemplateParam', codes)
    # python2:  print(response)
    response = client.do_action(request)
    response=str(response,encoding='utf-8')
    response=json.loads(response)
    if response['Message']=='OK':
        return str(code)
    else:
        return (response,-3,)

def idtoken(id):
    token=int(id)+168000
    return token

def tokenid(token,name):
    n=168000
    if name =='videoinfo' and token=='1':
        id=1
    elif token==None:
        return -101
    elif len(token)>6:
        return -102
    elif len(token)<6:
        return -103
    elif int(token)-n<0:
        return -104
    else:
        id=int(token)-n
    return id

def 手机验证(tel):
    ret = re.match(r"^1[35678]\d{9}$", tel)
    if ret:
        return 1
    else:
        return -1

#判断变量类型的函数
def typeof(variate):
    type=None
    if isinstance(variate,int):
        type = "int"
    elif isinstance(variate,str):
        type = "str"
    elif isinstance(variate,float):
        type = "float"
    elif isinstance(variate,list):
        type = "list"
    elif isinstance(variate,tuple):
        type = "tuple"
    elif isinstance(variate,dict):
        type = "dict"
    elif isinstance(variate,set):
        type = "set"
    return type
# 返回变量类型
def getType(variate):
    arr = {"int":"整数","float":"浮点","str":"字符串","list":"列表","tuple":"元组","dict":"字典","set":"集合"}
    vartype = typeof(variate)
    if not (vartype in arr):
        return "未知类型"
    return arr[vartype]

def 接口过滤(get,post,name):
    数据={}
    token=None
    for k,v in get.items():
        if k=="token":
            数据['id'] = tokenid(v,name)
            if 数据['id']<0:
                token='token错误'
        else:
            数据[k]=v
    for kk,vv in post.items():
        if kk == "token":
            数据['id'] = tokenid(vv,name)
            if 数据['id']<0:
                token='token错误'
        else:
            数据[kk] = vv
    if token=="token错误":
        return token
    else:
        print(数据)
        return 数据

def 验证码判断(phone,code,type):
    print(type)
    smscode = sqls("SELECT code FROM `dy`.`smscode`  where phone= '%s' and state = 1 and type = %s LIMIT 1" % (phone,type))
    print(smscode)
    if len(smscode)==0:
        return -1
    if int(smscode[0]['code'])==int(code):
        a=sqls("UPDATE `dy`.`smscode` SET `state` = '2' WHERE phone = %s and type =%s" % (phone,type))
        print(a)
        return 1
    else:
        return -1


