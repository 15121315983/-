import json
import time
import random
from sql import sqls
from sql import 接口标准化
from sql import 视频地址解析
from sql import 批量视频解析
import ali

def url(name,data):
    if name=='测试':
        returndata = 测试(data)
    elif name=='sendmessage':
        returndata = 发消息(data)#
    elif name=='acceptmessage':
        returndata = 读消息(data)#
    elif name=='queue':
        returndata = 获取排行信息(data)#
    elif name=='banner':
        returndata = 顶部广告(data)#
    elif name=='type':
        returndata = 标签(data)#
    elif name=='usercount':
        returndata = 用户数据统计(data)#
    elif name=='shoolvideo':
        returndata = 获取视频列表(data)#
    elif name=='videoinfo':
        returndata = 获取视频内容(data)#
    elif name=='likes':
        returndata = 收藏点赞(data)#
    elif name=='referrer':
        returndata = 获取团队数量(data)#
    elif name=='referrerdirect':
        returndata = 获取直接下级(data)#
    elif name=='activationcode':
        returndata = 生成激活码(data)#
    elif name=='findcode':
        returndata = 激活码列表(data)#
    elif name=='uploadinfo':
        returndata = 获取上传信息(data)#
    elif name=='reportorlike':
        returndata = 收藏举报关注等(data)#
    else:
        returndata = "",-1,'你访问的接口不存在'
    returndata=接口标准化(returndata)
    return returndata

def 测试(data):

    return '',

def 获取上传信息(data):
    if len(data)>0:
        clt = ali.init_vod_client(None, None)
        if data['type'] == "1":
            凭证=ali.create_upload_video(clt)
            return 凭证,
        elif data['type'] == "2":
            凭证 = ali.create_upload_image(clt,'default',data['ext'])
            return 凭证,
        else:
            return '',-1,"type不存在"
    else:
        return "",-101,"token异常或者不存在"



def 收藏举报关注等(data):
    #1收藏2点赞3举报4关注
    #视频id，视频封面，视频点赞，
    if data['type']=="1":
        收藏="select c.nick as authorname,b.looknum,b.goodnum,b.name as videoname,b.id as videoid,b.img as videoimg,b.video as videourl from likes a  left join video b on a.video = b.id left join user c on b.user = c.id where a.type = 1 and a.user= %s" \
           % (data['id'])
        收藏 = sqls(收藏)

        收藏 = 批量视频解析(收藏)
        return 收藏,
    elif data['type']=="4":
        关注="select user.picture,user.fans,user.nick,user.vip from likes left join user on likes.video=user.id where likes.type=4 and likes.user =%s" \
           % (data['id'])
        关注 = sqls(关注)
        return 关注,
    else:
        return '',-1,'type不存在'

def 激活码列表(data):
    列表 = "select code,userid,useuser,code.time,user.nick from code left join user on code.userid=user.id where code.state = 2 and code.userid = %s " % data['id']
    列表=sqls(列表)
    return 列表,

def 生成激活码(data):
    判断使用情况="select code as code from code where state = 1 and userid = %s " % data['id']
    code=sqls(判断使用情况)
    vip="select vip from user where id = %s" % data['id']
    vip=sqls(vip)
    print(vip[0]['vip'])
    if int(vip[0]['vip']) ==1 or int(vip[0]['vip']) ==2:
        return '',-1,'您名下没有激活码'
    if len(code) == 0:
        sql="select max(id) as max from code"
        newid=sqls(sql)[0]['max']
        num = json.dumps(hex(newid))
        a = str(random.choice([random.randrange(10), chr(random.randrange(65, 91))]))
        c = str(random.choice([random.randrange(10), chr(random.randrange(65, 91))]))
        激活码 = a + num[3:8] + c
        激活码录入="INSERT INTO `code` (`code`,`userid`,`time`,`state`) select  '%s',%s,NOW(),1" \
              % (激活码,data['id'])
        激活码录入=sqls(激活码录入)
        return 激活码,
    else:
        return code[0]['code'],0,'有未使用的激活码'

def 获取团队数量(data):
    结果={}
    direct="select COUNT(*) as n1 from user where referrer = %s" %(data['id'])
    direct=sqls(direct)
    结果['direct']=direct[0]['n1']
    indirect="select COUNT(*) as n2 from (select * from user where referrer = %s)a, (select * from user)b where b.referrer = a.id;" %(data['id'])
    indirect=sqls(indirect)
    结果['indirect'] = indirect[0]['n2']
    结果['id'] = data['id']
    return 结果,

def 获取直接下级(data):
    结果=sqls("select nick,vip,phone,id from user where referrer = %s" % (data['id']))
    if 结果=="sqlbug":
        return '',-101,'token解析错误'
    k=0
    for a in 结果:
        m="select count(*) as n from user where referrer = %s" % (int(a['id']))
        m=sqls(m)
        结果[k]['num']=m[0]['n']
        k=k+1
    return 结果,

def 收藏点赞(data):
    #收藏点赞举报的增加
    用户=data['id']
    类型=data['type']
    if data['type']==4:
        视频=data['like']
    else:
        视频 = data['videoid']
    查询 = "SELECT * FROM likes WHERE user=%s and video =%s and type = %s" % (用户, 视频, 类型)
    查询结果 = sqls(查询)
    if len(查询结果) == 1:
        return '[]',-1,"已存在"
    else:
        sql = "INSERT INTO `likes` (`user`,`video`,`time`,`type`) select  %s,%s,NOW(),%s from DUAL WHERE NOT EXISTS(SELECT * FROM likes WHERE user=%s and video =%s and type = %s);" % (
            用户, 视频, 类型, 用户, 视频, 类型)
        结果 = sqls(sql)
        if 类型=="1":
            收藏增加=sqls("update video set goodnum=goodnum+'1' where id = %s;" %(视频))
            return '插入成功',
        elif 类型=="2":
            点赞增加 = sqls("update video set collectionnum=goodnum+'1' where id = %s;" %(视频))
            return '插入成功',
        elif 类型=="3":
            return '举报成功',
        elif 类型=="4":
            点赞增加 = sqls("update user set likenum=likenum+'1' where id = %s;" %(用户))
            return '插入成功',
        else:
            return '标签不存在',-1


#聊天消息
def 发消息(data):
    时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    sql = "INSERT INTO `speak` (`time`, `info`, `user`, `type`, `video`) VALUES ('%s', '%s','%s','%s','%s');" \
          % (时间,data['info'],data['id'],1,data['video'])
    s=sqls(sql)
    if len(s)>0:
        return "[]",0,'插入成功'
    else:
        return "[]", -201, '未知错误'

def 获取视频列表(data):
    #标题,作者,总观看数,视频封面,点赞数
    标签=data['type']
    页码=int(data['page'])
    每页数=int(data['num'])
    sql = "select a.id,a.name,b.nick as author,a.img,a.looknum,a.goodnum,a.type2,a.type,a.video as videourl from video a LEFT OUTER JOIN user b on a.user = b.id where type = '%s' LIMIT %s,%s" \
          % (标签,(页码-1)*每页数,每页数)
    结果 = sqls(sql)
    结果=批量视频解析(结果)
    return 结果,

def 获取视频内容(data):
    #随机获取视频增加免费和收费的限定
    if data['videoid']=='1':
        随机查询 = 'SELECT t1.id FROM `video` AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM `video`)-(SELECT MIN(id) FROM `video`))+(SELECT MIN(id) FROM `video`)) AS id) AS t2 WHERE t1.id >= t2.id and state = 1 ORDER BY t1.id LIMIT %s;' % (
        data['pagesize'])
        随机 = sqls(随机查询)
        结果 = list()
        for i in 随机:
            视频 = i['id']
            sql = "select a.name as videoname,a.id as videoid,b.nick as username,b.id as userid, a.video,b.picture as userimg from video a  LEFT OUTER JOIN user b on a.user = b.id  where a.id = %s;" \
                  % (视频)
            随机结果 = sqls(sql)
            收藏情况 = sqls(
                "select count(*) from likes where user = %s and video = %s and type=1" % (data['id'], 视频))
            点赞情况 = sqls(
                "select count(*) from likes where user = %s and video = %s and type=2" % (data['id'], 视频))
            解析 = 视频地址解析(随机结果[0]['video'])
            #解析 = 视频地址解析("97d912bcaf354defb5177f8d54344bc4")
            随机结果[0]['type'] = 解析['VideoBase']['Title']
            随机结果[0]['video'] = 解析['PlayInfoList']['PlayInfo'][0]['PlayURL']
            随机结果[0]['img'] = 解析['VideoBase']['CoverURL']
            随机结果[0]['collection'] = 收藏情况[0]['count(*)']
            随机结果[0]['good'] = 点赞情况[0]['count(*)']
            结果.append(随机结果[0])
        return 结果,
    else:
        sql = "select a.id as videoid,b.id as userid, a.video,a.state,b.picture from video a  LEFT OUTER JOIN user b on a.user = b.id  where a.id = %s;" \
              % (int(data['videoid']))
        结果 = sqls(sql)
    #获取是否收藏,举报,点赞
        if len(结果)==1:
            收藏情况 = sqls(
                "select count(*) from likes where user = %s and video = %s and type=1" % (data['id'], data['videoid']))
            点赞情况 = sqls(
                "select count(*) from likes where user = %s and video = %s and type=2" % (data['id'], data['videoid']))
            结果[0]['collection'] = 收藏情况[0]['count(*)']
            结果[0]['good'] = 点赞情况[0]['count(*)']
            解析2 = 视频地址解析(结果[0]['video'])
            #解析2 = 视频地址解析("97d912bcaf354defb5177f8d54344bc4")
            结果[0]['videoname'] = 解析2['VideoBase']['Title']
            结果[0]['video'] = 解析2['PlayInfoList']['PlayInfo'][0]['PlayURL']
            结果[0]['picture'] = 解析2['VideoBase']['CoverURL']
        else:
            结果='视频未找到'
        return 结果,

def 读消息(data):
    sql = "SELECT info from speak where video = '%s' GROUP by time desc LIMIT %s" % (data['video'],int(data['num']))
    结果 = sqls(sql)
    a=dict()
    a['info']='123432'
    if len(结果)<4:
        结果.append(a)
    return 结果,

def 顶部广告(data):
    sql = "SELECT name,img,url from type where type = 'banner'"
    结果 = sqls(sql)
    return 结果,

def 标签(data):
    if str(data['type'])=="type":
        sql = "SELECT name,id as typeid from type where type = 'type'"
    else:
        sql = "SELECT name,id as typeid from type where type = '%s'" %(str(data['type']))
    结果 = sqls(sql)
    return 结果,

def 用户数据统计(data):
    #根据日期读取本周新会员量
    sql = "select count(*) from user WHERE YEARWEEK(date_format(addVipTime,'%Y-%m-%d'),1) = YEARWEEK(now(),1);"
    sql2 = "select count(*) from user WHERE( vip =3 or vip =2 ) and state=1"
    结果 = {}
    结果['newvip'] = sqls(sql)[0]['count(*)']
    结果['allvip'] = sqls(sql2)[0]['count(*)']
    #根据user标签读取本日会员量
    return 结果,

def 获取排行信息(data):
    #
    #排行榜需要精确到周,目前是所有的排行榜
    #
    if data['type']=='1':
        分类='looknum'
    elif data['type']=='2':
        分类='goodnum'
    elif data['type']=='3':
        分类='collectionnum'
    else:
        return '分类不存在'
    页码=int(data['page'])
    每页数=int(data['num'])
    sql = "select a.name,a.%s as num,b.phone  from video a LEFT OUTER JOIN user b on a.user = b.id ORDER BY %s DESC LIMIT %s,%s" % (分类,分类, (页码-1)*每页数,每页数)
    结果 = sqls(sql)
    return 结果,



