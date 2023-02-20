import re
import cv2
import time
import json
from pysl import easy_request,re_args_get

try:
    from .utils_api import truepath,img_writer
    from utils import Fplog,logprint
    path=truepath(__file__,'../log/extend_api/daidraw/log')
    logger=Fplog(path)
    def print(*log,logger=logger,**kw):
        logprint(*log,logger=logger,t=True,**kw)
except:
    from utils_api import truepath,img_writer

def get_db_available():
    url='https://pay.draft.art/api/wallet/get'
    r=easy_request(url,method='GET',
                        header=truepath(__file__,'draft_wallet.json'))
    amount=r['data']['amount']
    return int(amount)-18

def get_template(ix=0,alltp=False):
    template=json.load(open(truepath(__file__,'./draft_template_data.json')))
    if alltp:
        return template
    t=template[ix]
    print(t['name'])
    ss=[]
    for s in t['sizes']:
        w=int(s['width'])
        h=int(s['height'])
        # print(s['name'],f'{w}x{h}')
        ss.append((144,int(144*h/w),s['name'],f'{w}x{h}',w,h))
    return ss
    
def shape_choose_url(url,sizes):
    import numpy as np
    urlcontent=easy_request(url,pic=True).content
    img_array = np.array(bytearray(urlcontent), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    w,h,*_=img.shape
    # print(img.shape)
    h=int(144*h/w)
    sized=list(map(lambda x:abs(x-h),[144*i[-2]/i[-1] for i in sizes]))
    # print(sized)
    size=sized.index(min(sized))
    
    # print(sizes[size])
    
    return sizes[size][-2:],img
    
def ScaleImage(img, fileout,sz):
    width,height,*_=img.shape
    img=cv2.resize(img,sz)
    cv2.imwrite(fileout,img)
   
def bdraw_setting(msg):
    d= {
        "kw":('kw','str',''),
        "sz":('sz','int',0), 
        "ek":('ek','float_1',0.3),
        "md":('md','int',18),
        }
    r=re_args_get(msg,d)
    
    
    md=r['md']
    md_detail=get_template(md)
    if len(md_detail)<r['sz']:
        r['sz']=0
    r['sz']-=1
    r['sz']=md_detail[r['sz']][-2:]
    for _ in md_detail:
        print(_[-2:])
    
    imagecq=re.search('\[CQ:image.+\]',msg)
    if imagecq:
        imagecq=imagecq[0]
        msg=msg.replace(imagecq,'')
        picurl=re.search('(?<=url=).+(?=])',imagecq)[0]
        
        sz,img=shape_choose_url(picurl,md_detail)
        temp=truepath(__file__,'temp2.jpg')
        ScaleImage(img,temp,sz)
    else:
        sz=None

    if sz!=None:
        r['image']=open(temp,'rb')
        r["sz"]=sz
    return r    

def daidu_aidraw(msg):
    kws=bdraw_setting(msg)
    kw=kws.get('kw')
    if not kw:
        return 'kw is not found'
    if not get_db_available()>=1:
        return '余额不足'
    assert get_db_available()>=1
    
    url='https://api.draft.art/api/util/aiDraw/createByTemplate'
    image=kws.get('image')
    w,h=kws.get('sz')
    field={
            'keyword': kw,
            'height': str(h),
            'width': str(w),
            'initImage': ('blob',image,'image/jpeg') if image else 'null',
            'language': 'zh',
            'initImageStrength': str(kws.get('ek')),
            'templateId': '100{:0>3}'.format(kws.get('md')),
          }
    print(field)
    boundary='----WebKitFormBoundaryUPArSBBqP1BHwcV8'
    
    tid=easy_request(url,form_data=(field,boundary),
                     method='POST',header=truepath(__file__,'draft_post.json'))
    img_id=tid['data']['id']
    print('task id',img_id)
    keyword,height,width=field['keyword'],field['height'],field['width']
    print(f'keyword: {keyword}\nsize: {width}x{height}')
    
    url=f'https://api.draft.art/api/util/image/download/4xhd?id={img_id}'
    while 1:
        try:
            imgurl=easy_request(url,method='GET',header=truepath(__file__,'draft_download.json'))
            imgurl=imgurl['data']['url']
            break
        except:
            time.sleep(1)
    # print(imgurl)
    return 0,img_writer(url=imgurl)
    

if __name__=='__main__':
    
    print(get_db_available())
    tp=get_template(18,alltp=True)
    
    msg='daidraw kw=婚纱，露肩，红色瞳孔，白色长发，花束，长筒靴，白色手套  ek=0.1 sz=3 md0 [CQ:image,file=2904d060798636b051444917f63d4ae9.image,subType=0,url=https://gchat.qpic.cn/gchatpic_new/1767557815/572675295-3067516242-CA1EC2E5574584B472591BAE4B47E83E/0?term=3&amp;is_origin=0]'
    # print(bdraw_setting(msg))
    # print(daidu_aidraw(msg))












# https://oss-cdn-main.draft.art/aiDraw/predict/output_hd/uF3LZgISC5XztYFbHirouBivBfHeXL8R.jpg

# https://api.draft.art/api/util/image/listCommunity
# https://api.draft.art/api/template/list
# https://api.draft.art/api/util/image/listMine
# https://pay.draft.art/api/wallet/get
# https://api.draft.art/api/util/image/download/4xhd?id=70668850
# https://api.draft.art/api/util/image/get?id=70668850

# current: 1
# mode: "afterCreation"
# modelId: null
# needCollectStatus: true
# search: "    "
# size: 30

# current: 1
# mode: "myCreation"
# needCollectStatus: true
# search: null
# size: 30

# createId: 1838860


# keyword: 羽毛饰品，蓝色长发
# height: 576
# width: 1024
# initImage: null
# language: zh
# templateId: 100018


# keyword: 羽毛饰品，蓝色长发
# height: 576
# width: 1024
# initImage: (binary)
# language: zh
# initImageStrength: 0.50
# templateId: 100018









