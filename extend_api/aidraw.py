import re
import time
from pysl import easy_request,re_args_get

try:
    from .utils_api import truepath
    from utils import Fplog,logprint
    path=truepath(__file__,'../log/extend_api/aidraw/log')
    logger=Fplog(path)
    def print(*log,logger=logger,**kw):
        logprint(*log,logger=logger,t=True,**kw)
except:
    from utils_api import truepath

def shape_choose_url(url):
    import numpy as np
    import cv2
    
    urlcontent=easy_request(url,pic=True).content
    img_array = np.array(bytearray(urlcontent), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    w,h,*_=img.shape
    w=int(144*w/h)
    size=list(map(lambda x:abs(x-w),[144,256,81,-1000,192,108]))
    s=size.index(min(size))+1
    
    print(["err","1:1" , "9:16", "16:9",'errxx', "3:4" ,"4:3"][s])
    return s

def draw_setting(msg):
    imagecq=re.search('\[CQ:image.+\]',msg)
    if imagecq:
        imagecq=imagecq[0]
        msg=msg.replace(imagecq,'')
        picurl=re.search('(?<=url=).+(?=;)',imagecq)[0]
        sz=shape_choose_url(picurl)
    else:
        sz=None
        picurl=''
 
    d= {
        "inputText":('kw','str',''),
        "imageFactors":('ek','float_2',0.3),
        "multiple":('ori','bool+',(2,4)),
        "imageSizeId":('sz','int',3),
        "reverseWords":('ukw','str',''),
        }
    r=re_args_get(msg,d)
    r["picurl"]=picurl
    if sz:
         r["imageSizeId"]=sz
    return r

def get_available():
    url='https://cg-api.heyfriday.cn/v1/star/getUserStartTotal'
    r=easy_request(url=url,header=truepath(__file__,'aidraw_detail.json'),method='GET',)
    try:
        left=r['result']['starNum']
        return int(left)
    except:
        print('err')
        print(r)
        
        
def draw(inputText='',reverseWords='',
         picurl='',artistId=10,styleId=34,imageFactors=0.5,
         imageSizeId=6,multiple=2):
    
    assert get_available()>=2
    kw1='油画,水彩,厚涂,水墨,彩墨,壁纸,(精致的插画),(非常精细的cg),'                 # 插画类型
    kw2='8k画质,最高画质,最高品质,超高分辨率,(((杰作))),(大师之作),'                 # 插画质量
    kw3='(美少女),'                                                                # 人物
    kw4='灵动明亮的大眼睛,长睫毛,(极其精致的五官),(细致刻画脸部),(细致刻画人体),'     # 人物细节
    kw5='(人物特写),((单人)),'                                                     # 画面主体
    kw6=''                                                                         # 景象
    kw7='远景,景深,景物特写,精致背景,广角,极其详细的背景描写,'                       # 景象描写
    kw8='唯美的景象,氤氲,绝美的,(二次元),精细细节,超细致,'                           # 整体描述
    kw9='cygames,商业作品,'                                                        # 作者相关
    kw=''.join([kw1,kw2,kw3,kw4,kw5,kw6,kw7,kw8,kw9])

    payload={"inputText":kw+inputText,
             "styleId":34,
             "artistId":10,
             "imageSizeId":imageSizeId,
             "picUrl":picurl,
             "multiple":multiple,
             "nid":1,
             "picRefType":1,
             "imageFactors":imageFactors,
             "reverseWords":"多人,双人,两个人,粗线条,低画质,低质量,最差质量,模糊,模糊不清,不清晰,最低画质,细线条,低饱和度,奇怪的手部,错误的人体结构,错误的肢体,"+reverseWords,
             "modelId":1
             }
    
    print(payload)
    print(get_available())

    
    url= 'https://cg-api.heyfriday.cn/v1/generate/generateImageV3'
    js=easy_request(url,method='POST',
                    header=truepath(__file__,'aidraw_v3.json'),data=payload)
    
    try:
        id=js['result']['id']
    except:
        try:
            return js['message']
        except:
            return js['result']
     
    url= 'https://cg-api.heyfriday.cn/v1/generate/myPictureDetail?id={}'.format(id)
    js=easy_request(url,header=truepath(__file__,'aidraw_detail.json'),data=payload)
    while not js['result']['pictureUrl']:
        js=easy_request(url,header=truepath(__file__,'aidraw_detail.json'),data=payload)
        print(
            # js['result']['usedTime'],
            '.',
            end='')
        time.sleep(2)
    try:
        return (0,js['result']['pictureUrl'])
    except:
        print(js['data'])
        return '系统错误'


if __name__=='__main__':
    
    # kw_cg='斑驳的阳光,美丽的少女,木质桌椅,红宝石般的眼珠,纱裙,露肩,浅白色露肩长裙,幽静,低沉,暗色系,罗马柱,梅花,白花,兰花,鸟笼,复古色,丁达尔效应,红色瞳孔,白色长发'
    # print('\n',draw(''),sep='')
    
    # msg='aidraw kw=斑驳的阳光,美丽的少女,木质桌椅,红宝石般的眼珠 ukw=奇怪的手部 ek=0.7545 sz=6 [CQ:image,file=2904d060798636b051444917f63d4ae9.image,subType=0,url=https://gchat.qpic.cn/gchatpic_new/2264168148/657696854-2934150836-A1786D82697B16FF3E57030CAD284CA8/0?term=3&amp;is_origin=1]'
    # print(draw_setting(msg))
    
    # print(shape_choose_url('https://gchat.qpic.cn/gchatpic_new/2264168148/657696854-2965610982-38A51791350CE41288CDFDF01DCC2BAB/0?term=3&amp'))

    print(get_available())

    pass


# artistId: 10 不限定 
# imageFactors:  影响因子
# imageSizeId: 1:1  9:16 16:9 3:4 4:3 壁纸   index 1-6     144:144 144:256 144:81 144:192 144:108
# inputText: 关键词
# modelId: 模型id 只有1
# multiple: 2 4 质量
# nid: 1 数量
# picRefType: 1 固定
# picUrl: 参考图片
# reverseWords: 反向关键词
# styleId: 34 动漫


# 10 不限定
# 14 T·金凯德
# 16 精灵画师
# 18 徐悲鸿
# 4 莫奈
# 5 丰子恺
# 11 永井博
# 6 保罗·塞尚
# 8 托马斯·科尔
# 12 约翰·哈利斯
# 13 M·西莫内蒂
# 2 毕加索
# 15 S·塞瑞尔
# 17 大卫·霍克尼
# 3 梵高

# 1 智能
# 14 不限定
# 34 动漫风
# 31 足球宝贝
# 4 油画
# 3 水彩
# 15 哑光画
# 16 儿童画
# 17 素描
# 6 中国风
# 18 电影感
# 19 摄影
# 7 游戏场景
# 21 虚幻引擎
# 20 低聚艺术
# 30 异次元头像
# 26 剪纸
# 5 经典动漫风
# 39 手绘增强
# 8 吉卜力
# 10 像素艺术
# 11 CG渲染
# 2 赛博朋克
# 12 蒸汽波
# 22 印象主义
# 23 未来主义
# 13 超现实主义
# 9 浮世绘
# 24 室内设计










