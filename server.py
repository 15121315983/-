from flask import Flask,session
from flask import request
from flask import render_template
from flask_cors import CORS
import json,os,base64
import random
import time
from sql import 接口标准化
from sql import 接口过滤
from sql import sqls
from sql import tokenid
from 用户 import url as 用户路由
from 交互 import url as 交互路由
from 视频 import url as 视频路由
from 资金 import url as 资金路由
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app, supports_credentials=True)
@app.route('/')
def main():
    return '404'

@app.route('/jh/<name>', methods=['GET', 'POST'])
def 交互端(name,value=None):
    #传入数据处理
    数据 = 接口过滤(request.args, request.form.to_dict(),name)
    if 数据=="token错误":
        结果 = "[]",-101,"token错误"
        return 接口标准化(结果)
    else:
        return 交互路由(name, 数据)

@app.route('/money/<name>', methods=['GET', 'POST'])
def 资金端(name,value=None):
    #传入数据处理
    数据 = 接口过滤(request.args, request.form.to_dict(),name)
    if 数据=="token错误":
        结果 = "[]",-101,"token错误"
        return 接口标准化(结果)
    else:
        return 资金路由(name, 数据)

@app.route('/video/<name>', methods=['GET', 'POST'])
def 阿里视频(name,value=None):
    #传入数据处理
    数据 = 接口过滤(request.args, request.form.to_dict(),name)
    if 数据=="token错误":
        结果 = "[]",-101,"token错误"
        return 接口标准化(结果)
    else:
        return 视频路由(name, 数据)

@app.route('/yh/<name>', methods=['GET', 'POST'])
def 用户端(name,value=None):
    #传入数据处理
    数据 = 接口过滤(request.args, request.form.to_dict(),name)
    if 数据=="token错误":
        结果 = "[]",-101,"token错误"
        return 接口标准化(结果)
    else:
        return 用户路由(name, 数据)

@app.route('/money/<name>', methods=['GET', 'POST'])
def 支付接口(name,value=None):
    数据 = 接口过滤(request.args, request.form.to_dict(),name)
    if 数据=="token错误":
        结果 = "[]",-101,"token错误"
        return 接口标准化(结果)
    else:
        if name=='alipay':
            return "alipay"
        else:
            结果 = "[]", -404, "访问当连接不存在"
            return 接口标准化(结果)

@app.route('/yh/<name>', methods=['GET', 'POST'])
def 用户端(name,value=None):
    #传入数据处理
    数据 = 接口过滤(request.args, request.form.to_dict(),name)
    if 数据=="token错误":
        结果 = "[]",-101,"token错误"
        return 接口标准化(结果)
    else:
        return 接口标准化(name, 数据)


@app.route('/system/<name>', methods=['GET', 'POST'])
def 更新(name,value=None):
    data=request.form.to_dict()
    if name =="up":
        get=request.args
        更新="INSERT INTO `updates` (`ver_ios`, `ver_apk`) VALUES ('%s', '%s')" % (get['ver_ios'],get['ver_apk'])
        更新=sqls(更新)
        return json.dumps('更新成功')
    elif name =="update":
        读取="select * from updates order by id desc limit 0,1"
        读取 = sqls(读取)
        版本={"sysver_apk":读取[0]['ver_apk'],"downurl_apk":'https://douyunzhibo.oss-cn-chengdu.aliyuncs.com/updata/douyun.apk',
            "sysver_ios":读取[0]['ver_ios'],"downurl_ios":'',"ver_info": 读取[0]['ver_info']}
        return json.dumps(版本)

# 上传专用
@app.route("/upimg/<name>", methods=['GET', 'POST'])
def get_frame(name):
    #读取路径
    url="http://47.106.156.241:8080"
    if name=='sfz':
        # 接收图片
        数据 = 接口过滤(request.args, request.form.to_dict(), name)
        file1 = request.files['file1']
        file2 = request.files['file2']
        # # 文件保存目录（桌面）
        file_path=r'D:\img'
        #file_path=r'/Users/zuolongxiang/Desktop'
        if file1:
            # 地址拼接™
            name1 = str(数据['id']) + str(random.randrange(100000000, 999999999)) + file1.filename[-4:]
            paths1= os.path.join(file_path,name1)
            # 保存接收的图片到桌面
            file1.save(paths1)
            路径1 = url+"/"+name1
        if file2:
            # 地址拼接
            name2 = str(数据['id']) + str(random.randrange(100000000, 999999999)) + file2.filename[-4:]
            paths2 = os.path.join(file_path,name2)
            # 保存接收的图片到桌面
            file2.save(paths2)
            路径2 = url+"/"+name2
        # print(路径)
        更新 = "INSERT INTO `sfz` (`userid`,`url`, `url2`) VALUES ('%s', '%s', '%s')" % (数据['id'], 路径1,路径2)
        更新 = sqls(更新)
        更新 = "UPDATE `dy`.`user` SET `authentication` = '%s' WHERE `id` = %s" % ('审核中', 数据['id'])
        更新 = sqls(更新)
        return 接口标准化(None)
    elif name=='mp4':
        # 接收图片
        数据 = 接口过滤(request.args, request.form.to_dict(), name)
        upload_file = request.files['file']
        # 获取图片名
        file_name = upload_file.filename
        # 文件保存目录
        file_path=r'D:\mp4'
        #file_path=r'/Users/zuolongxiang/Desktop'
        if upload_file:
            # 地址拼接
            file_name=str(数据['id'])+str(random.randrange(100000000, 999999999))+'.mp4'
            file_paths = os.path.join(file_path, file_name)
            # 保存接收的图片到桌面
            upload_file.save(file_paths)
        路径 = url+"/"+file_name
        更新 = "INSERT INTO `video` (`user`, `name`, `video`, `state`, `type`, `time`) VALUES ('%s', '%s', '%s', '%s', '%s', NOW())" \
             % (数据['id'], 数据['name'],路径,2, 数据['type'])
        #print(更新)
        更新 = sqls(更新)
        return 接口标准化(None)
    elif name=='headurl':
        # 接收图片
        数据 = 接口过滤(request.args, request.form.to_dict(), name)
        upload_file = request.files['file']
        # 获取图片名
        file_name = upload_file.filename
        格式=file_name[-4:]
        # 文件保存目录
        file_path=r'D:\img'
        #file_path=r'/Users/zuolongxiang/Desktop'
        if upload_file:
            # 地址拼接
            file_name=str(数据['id'])+str(random.randrange(100000000, 999999999))+格式
            file_paths = os.path.join(file_path, file_name)
            # 保存接收的图片到桌面
            upload_file.save(file_paths)
            路径 = url+"/"+file_name
            更新 = "UPDATE `dy`.`user` SET `picture` = '%s' WHERE `id` = %s" % (路径, 数据['id'])
            更新 = sqls(更新)
        return 接口标准化(None)
    else:
        a="[]",-404,"接口不存在"
        return 接口标准化(a)



@app.errorhandler(404)
def miss(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    #调试模式
    app.threaded=True
    app.processes=20
    app.debug = True
    app.run()