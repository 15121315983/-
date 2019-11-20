# -*- coding: UTF-8 -*-
import json
import datetime
import time
import traceback
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.client import AcsClient
from aliyunsdkvod.request.v20170321 import CreateUploadVideoRequest
from aliyunsdkvod.request.v20170321 import GetPlayInfoRequest
from aliyunsdkvod.request.v20170321 import GetVideoListRequest
from aliyunsdkvod.request.v20170321 import CreateUploadImageRequest

#初始化程序
def init_vod_client(accessKeyId, accessKeySecret):
    accessKeyId = "LTAI4FsswRJma4LNZrNPNyrs"
    accessKeySecret = "YmYYLxGc3GupseZzNc7GTkIESAuGa1"
    regionId = 'cn-shanghai'   # 点播服务接入区域
    connectTimeout = 5         # 连接超时，单位为秒
    return AcsClient(accessKeyId,accessKeySecret, regionId, auto_retry=True, max_retry_time=3, timeout=connectTimeout)

#获取上传凭证
def create_upload_video(clt):
    request = CreateUploadVideoRequest.CreateUploadVideoRequest()
    request.set_Title('Video Title')
    request.set_FileName('/opt/video/sample/video_file.mp4')
    request.set_Description('Video Description')
    request.set_CoverURL('http://img.alicdn.com/tps/TB1qnJ1PVXXXXXCXXXXXXXXXXXX-700-700.png')
    request.set_Tags('tag1,tag2')
    request.set_CateId(0)
    request.set_accept_format('JSON')
    response = json.loads(clt.do_action_with_exception(request))
    return response
    try:
        clt = init_vod_client('<AccessKeyId>', '<AccessKeySecret>')
        uploadInfo = create_upload_video(clt)
        print('ok')
        print(uploadInfo['UploadAuth'])
        print(json.dumps(uploadInfo, ensure_ascii=False, indent=4))
    except Exception as e:
        print(e)
        print(traceback.format_exc())


#获取播放连接
def get_play_info(clt, videoId):
    request = GetPlayInfoRequest.GetPlayInfoRequest()
    request.set_accept_format('JSON')
    request.set_VideoId(videoId)
    request.set_AuthTimeout(3600*5)
    response = json.loads(clt.do_action_with_exception(request))
    return response
    try:
        clt = init_vod_client("LTAI4FsswRJma4LNZrNPNyrs", "YmYYLxGc3GupseZzNc7GTkIESAuGa1")
        playInfo = get_play_info(clt, videoId)
        print(json.dumps(playInfo, ensure_ascii=False, indent=4))
    except Exception as e:
        print(e)
        print(traceback.format_exc())


#获取图片上传凭证
def create_upload_image(clt, imageType, imageExt):
    request = CreateUploadImageRequest.CreateUploadImageRequest()
    request.set_ImageType(imageType)
    request.set_ImageExt(imageExt)
    request.set_accept_format('JSON')
    return json.loads(clt.do_action_with_exception(request))
    try:
        clt = init_vod_client('<AccessKeyId>', '<AccessKeySecret>')
        imageInfo = create_upload_image(clt, 'cover', 'jpg')
        print(json.dumps(imageInfo, ensure_ascii=False, indent=4))
    except Exception as e:
        print(e)
        print(traceback.format_exc())

#获取视频列表
def get_video_list(clt):
    request = GetVideoListRequest.GetVideoListRequest()
    # 以获取最近30天的视频列表为例
    utcNow = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    utcMonthAgo = datetime.datetime.utcfromtimestamp(time.time() - 30*86400).strftime("%Y-%m-%dT%H:%M:%SZ")
    request.set_StartTime(utcMonthAgo)   # 视频创建的起始时间，为UTC格式
    request.set_EndTime(utcNow)          # 视频创建的结束时间，为UTC格式
    #request.set_Status('Uploading,Normal,Transcoding')  # 视频状态，默认获取所有状态的视频，多个用逗号分隔
    #request.set_CateId(0)               # 按分类进行筛选
    request.set_PageNo(4)
    request.set_PageSize(100)
    request.set_accept_format('JSON')
    response = json.loads(clt.do_action_with_exception(request))
    return response
    try:
        clt = init_vod_client('<AccessKeyId>', '<AccessKeySecret>')
        videoList = get_video_list(clt)
        print(json.dumps(videoList, ensure_ascii=False, indent=4))
    except Exception as e:
        print(e)
        print(traceback.format_exc())











# clt=init_vod_client(None,None)
# a= get_video_list(clt)
# print(a)
# print(a['Total'])
# print("-----")
# # print(a['VideoList']['Video'])
# print("-----")
# for v in a['VideoList']['Video']:
#     # print(v['VideoId'])
#     # if v['VideoId']=="b11f974fc64946b3ad026e1e08d5e920":
#     # print(v)
#     print(v['Title'])
#     # print(v)
