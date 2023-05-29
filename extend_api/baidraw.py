import re
import cv2
import time

try:
    from .utils_api import truepath,img_writer,easy_request,re_args_get
    # from utils import Fplog,logprint
    # path=truepath(__file__,'../log/extend_api/baidraw/log')
    # logger=Fplog(path)
    # def print(*log,logger=logger,**kw):
    #     logprint(*log,logger=logger,t=True,**kw)
except:
    from utils_api import truepath,img_writer,easy_request,re_args_get
    
def shape_choose_url(url):
    import numpy as np
    urlcontent=easy_request(url,pic=True).content
    img_array = np.array(bytearray(urlcontent), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    w,h,*_=img.shape
    w=int(144*w/h)
    size=list(map(lambda x:abs(x-w),[144,81,256,96,108]))
    size=size.index(min(size))
    print(["1:1","16:9","9:16","3:2","4:3"][size])
    return size,img

def ResizeImage(img, fileout,maxlimit=1024):
    width,height,*_=img.shape
    if width>1024 or height>1024:
        if width>height:
            height=maxlimit*height/width
            width=maxlimit
        else:
            width=maxlimit*width/height
            height=maxlimit
        img = cv2.resize(img,(int(height), int(width)))
        
    if not fileout.endswith('.jpg'):
        fileout=fileout+'.jpg'
    cv2.imwrite(fileout,img)
   
def bdraw_setting(msg):
    imagecq=re.search('\[CQ:image.+\]',msg)
    if imagecq:
        imagecq=imagecq[0]
        msg=msg.replace(imagecq,'')
        picurl=re.search('(?<=url=).+(?=])',imagecq)[0]
    
        sz,img=shape_choose_url(picurl)
        temp=truepath(__file__,'temp1.jpg')
        ResizeImage(img,temp)
    else:
        sz=None
 
    d= {"kw":('kw','str',''),
        "sty":('sty','str','二次元'),
        "art":('art','str','高清,精细刻画,明亮,辛烷渲染,丁达尔效应'),
        "sz":('sz','int',3),
        "ek":('ek','int',3),
        "ori":('ori','bool',False),
        }
    
    r=re_args_get(msg,d)
    if sz!=None:
        r['image']=open(temp,'rb')
        r["sz"]=sz
    return r    
   
def get_balance():
    url='https://yige.baidu.com/api/t2p/points/account_balance'
    balance=easy_request(url=url,header=truepath(__file__,'headers/baidraw_get_url.json'))
    return int(balance['data']['balance'])
    
def baidu_aidraw(msg):
    kws=bdraw_setting(msg)
    kw=kws.get('kw')
    assert kw
    assert get_balance()>=2
    
    if len(kws.items())==1:
        payload={"scene": "平面", "style": "唯美二次元风格", "resolution": "1024x1024","query":kw }
        url='https://yige.baidu.com/api/t2p/creation/add_task'
        tid=easy_request(url=url,header=truepath(__file__,'headers/baidraw_post_data.json'),
                         method='POST',data=payload)
    else: 
        url='https://yige.baidu.com/api/t2p/creation/add_custom_task'
        sz=kws.get('sz')
        if kws.get('ori'):
            sz+=5
        resolution_=['1024x1024','1280x720','720x1280','1152x768','1024x768',
                     '2048x2048','2560x1440','1440x2560','2304x1536','2048x1536']
        resolution=resolution_[sz]
        fields={'model': '模型3',
                'custom_style': kws.get('sty'),
                'art_modifier': kws.get('art'),
                'num_image': '1',
                'resolution': resolution,
                'model_version': '2',
                'ref_image_type': '2',
                'intensity': str(kws.get('ek')),
                'query': kw,}
        boundary='------WebKitFormBoundarynf7f3tIRSTnifssZ'
        
        image=kws.get('image')
        if image:
            fields['image']=('blob',image,'image/jpeg')
        print(resolution)

        tid=easy_request(url=url,
                       header=truepath(__file__,'headers/baidraw_post_data.json'),
                       form_data=(fields,boundary))
    try:
        tid=tid['data']['task_id']
    except:
        print(tid)
        return tid['message']
    print(f'task_id : {tid}\nkeyword : {kw}')
    
    time.sleep(5)
    retry=1
    while 1:
        try:
            url='https://yige.baidu.com/api/t2p/creation/get_queue'
            tasks=easy_request(url=url,header=truepath(__file__,'headers/baidraw_get_url.json'),
                               method='GET')['data']
            for t in tasks:
                task_id=t['task_id']
                if task_id==tid:
                    task=t
            imgurl=task['image'][-1]['url']
            break
        except:
            time.sleep(2)
            print('.',end='')   
        retry+=1
        if retry>10:
            return '生成失败'
    imgurl=imgurl.replace('r_l&v=1','origin&v=1&d=1')
    imgFile=img_writer(url=imgurl,headers='headers/baidraw_get_img.json')[0]
    
    return 0,imgFile


if __name__=='__main__':
    msg='baidraw kw=婚纱，露肩，红色瞳孔，白色长发，花束，长筒靴，白色手套  ek=2 sz=3 [CQ:image,file=2904d060798636b051444917f63d4ae9.image,subType=0,url=https://gchat.qpic.cn/gchatpic_new/2264168148/657696854-2372193464-11E91D4EB629E4E72501DB814C052E2D/0?term=3&amp;is_origin=0]'
    print(bdraw_setting(msg))
    # print(baidu_aidraw(msg))
    
    # print(get_balance())
    
    pass



# kw="婚纱，少女，脸红，高清，唯美"
# model: 模型3
# custom_style: 二次元
# art_modifier: 高清,精细刻画,明亮,辛烷渲染,丁达尔效应
# num_image: 1
# resolution: 1280x720
# model_version: 2
# ref_image_type: 2
# image: (binary)
# intensity: 5
# query: 唯美，少女，古风，女孩子，浅笑，城堡，白裙子，公主