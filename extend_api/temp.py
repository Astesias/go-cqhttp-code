import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = 2300000000
import time
import json
from pysl import easy_request
import requests
import cv2
import base64

from utils_api import url_imshow
from requests_toolbelt import MultipartEncoder

# https://yige.baidu.com/api/t2p/op/prize/confirm?t=1674288009419
# token: "Njk4OTYzMzA3MjA4OTIxODcxOTE2NzQyODgwMDcwNjk5MjQ="
# MjkyNjc4MDA4NjExNDEyMzc3NTE2NzQzMjA5OTc5MzUzMzI=

def ResizeImage(filein,fileout,maxlimit=1024):
    img = Image.open(filein)
    type_ = img.format
    
    width,height=img.size
    if width>height:
        height=maxlimit*height/width
        width=maxlimit
    else:
        width=maxlimit*width/height
        height=maxlimit
        
    out = cv2.resize((int(width), int(height)), Image.ANTIALIAS)
    cv2.imwrite(fileout,out)
    
# def cv_resize(filein, fileout,scale=1)
    
def img_size(img):
    img = Image.open(img)
    print(img.size)

def ResizeImage_stsize(img_file,temp_file='./temp.jpg',limit=1350,ulimit=200):
    print('ori',os.stat(img_file).st_size/1024)
    ResizeImage(img_file,'./temp.jpg')
    print('ori_',os.stat(temp_file).st_size/1024)
    if (os.stat(temp_file).st_size/1024)>limit:
        _=1
        scale=0.9
        while _ or (os.stat(temp_file).st_size/1024)>limit:
            _=0
            scale-=0.1
            ResizeImage(img_file,temp_file,scale=scale)
    if (os.stat(temp_file).st_size/1024)<ulimit:
        _=1
        scale=1.5
        while _ or (os.stat(temp_file).st_size/1024)>limit:
            _=0
            scale+=0.1
            ResizeImage(img_file,temp_file,scale=scale)
    else:
        pass


# 1362
# image_fs=os.listdir('D:/Desktop/Image')
# for img_file in image_fs:
#     print(img_file,end=' ')
#     img_file='D:/Desktop/Image/'+img_file
#     temp_file='./temp.jpg'
#     ResizeImage_stsize(img_file,temp_file)

temp_file='./temp.jpg'
img_file='D:/Desktop/Image/783b588e562353abbac6bd9d29521d3012ab770b_raw.jpg'
ResizeImage(img_file,temp_file)
kw="婚纱，少女，脸红，高清，唯美，白色手套"

img_size(img_file)
img_size(temp_file)
image=open(temp_file,'rb')
#   print(os.stat(temp_file).st_size/1024)

fields={
        'model': '模型3',
        'custom_style': '二次元',
        'art_modifier': '高清,精细刻画,明亮,辛烷渲染,丁达尔效应',
        'num_image': '1',
        'resolution': '1024x1024',
        'model_version': '2',
        'ref_image_type': '2',
        'image': ('blob',image,'image/jpeg'),
        'intensity': "3",
        'query': kw,
        }

fields_={
        'type': '1',
        'image': ('upload',image,'image/jpeg'),
        }

boundary='------WebKitFormBoundarynf7f3tIRSTnifssZ'

custom_data=MultipartEncoder(
                            fields=fields,
                            boundary=boundary
                            )

postdata={
        "scene": "平面", "style": "唯美二次元风格", "resolution": "1024x1024",
        "query": kw
        }

data={'activity_id': 2}

url='https://yige.baidu.com/api/t2p/op/prize/draw'
url='https://yige.baidu.com/api/t2p/creation/add_custom_task'
url='https://yige.baidu.com/api/t2p/creation/check_image'
# url='http://127.0.0.1:5000'
# with open('wenxin_post_custom_data.json') as fp:
#     header=json.load(fp)
# header['Content-Type']=custom_data.content_type
    
# r=requests.post(url,
#                 headers=header,
#                 data=custom_data,
#                 ).content

r=easy_request(url=url,header='wenxin_post_custom_data.json',form_data=(fields_,boundary))
print(r)


# tid=tid['data']['task_id']
# print(f'task_id : {tid}\nkeyword : {kw}')

# time.sleep(5)
# while 1:
#     try:
#         url='https://yige.baidu.com/api/t2p/creation/get_queue'
#         tasks=easy_request(url=url,header='wenxin_get_url_h.json',method='GET')['data']
#         for t in tasks:
#             task_id=t['task_id']
#             if task_id==tid:
#                 task=t
#         imgurl=task['image'][-1]['url']
        
#     except:
#         time.sleep(2)
#         print('.',end='')   

# r=easy_request(url=imgurl,header='wenxin_get_img_h.json',method='GET',pic=1)
# url_imshow(r.content)


    



# https://aigc-t2p.cdn.bcebos.com/artist-long/1535188_0_final.png?x-bce-process=style/r_l&v=1
# https://aigc-t2p.cdn.bcebos.com/artist-long/1535285_0_final.png?x-bce-process=style/r_l&v=1

# https://yige.baidu.com/api/t2p/creation/get_queue?t=1674068297498
# https://yige.baidu.com/api/t2p/interact/view_image?t=1674068310610&image_id=c4217400
# https://yige.baidu.com/api/t2p/creation/get_status?t=1674070373855&task_id=2508582














