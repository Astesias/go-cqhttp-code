import os
import time
import json
import random
from pysl import easy_request

def truepath(file,*arg):
    return os.path.join(os.path.abspath(os.path.split(file)[0]),*arg)

def url_imshow(urlcontent,headers=None,show=True):
    import cv2
    import numpy as np
    # import urllib.request as request
    # response = request.urlopen(urlcontent)
    img_array = np.array(bytearray(urlcontent), dtype=np.uint8)
    if show:
        img_array = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        cv2.imshow('i',img_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
    else:
        return img_array

def random_name(n):
    st='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    st=st+st.lower()+'_0123456789'
    r=''
    for i in range(n):
        if i==0:  
            r+=random.choice(st[:-9])
        else:
            r+=random.choice(st)
    return r

def make_json(name):
    import re
    with open('temp.json') as fp:
        data=fp.read()
    # data='\n'.join(data)
    print(data)
    
    keys=re.findall('.+?(?=:): ',data)
    values=re.findall('(?<= ).+',data)
    
    with open(name+'.json','w') as fp:
        fp.write('{\n')
        for i,j in zip(keys,values):
            i=i.strip(': ')
            fp.write(f'\"{i}\": \"{j}\",\n')
        
        fp.write(r'"py": "ysl"')
        fp.write('\n}')

def cmd(command):
    import subprocess
    cmd=subprocess.getstatusoutput(command)
    print(('Success' if not cmd[0] else 'Fail') + ' Command:\n   '+command)
    print(cmd[1].replace('Active code page: 65001',''))

def img_writer(path='../../data/images',num=1,url=None,headers=None):
    names=[]
    if not url:
        url='https://api.yimian.xyz/img'
    if isinstance(headers,str):
        with open(truepath(__file__,headers)) as fp:
            headers=json.load(fp)
    
    for i in range(num):
        name=random_name(5)+'.jpg'
        names.append(name)
        r=easy_request(url,header=headers,pic=True)
        p=truepath(__file__,path,name)
        _=1
        while _ or os.stat(p).st_size<3000:
            if _:
                _=0
            else:
                time.sleep(1)
                print('.',end='')
                r=easy_request(url,header=headers,pic=True)
            with open(p, "wb") as f:
         	     f.write(r.content)
    print()
    return names

def img_writers(path='../../data/images',url=None,headers=None):
    names=[]
    if not url:
        url=['https://api.yimian.xyz/img']
    if isinstance(headers,str):
        with open(truepath(__file__,headers)) as fp:
            headers=json.load(fp)
    
    l=len(url)
    for n,i in enumerate(url):
        print(f'Downloading {n+1}/{l}')
        name=random_name(5)+'.jpg'
        names.append(name)
        r=easy_request(i,header=headers,pic=True)
        p=truepath(__file__,path,name)
        with open(p, "wb") as f:
     	     f.write(r.content)
        if os.stat(p).st_size<3000:
            names.remove(name)
            print('A file download failed')

    return names

def clear_img_cache(path='../../data/images',num=100):
    path=truepath(__file__,path)
    if len(os.listdir(path))>=num:
        cmd('rm '+path+'/*.jpg')

if __name__ == '__main__':
    
    # print(img_writer(url='https://proxy.pixivel.moe/c/540x540_70/img-master/img/2018/03/16/20/17/39/67763040_p0_master1200.jpg'))
    
    # print(img_writers(url=
    #                     ['https://o.acgpic.net/img-original/img/2020/11/13/01/32/47/85633671_p0.jpg', 
    #                      # 'https://o.acgpic.net/img-original/img/2020/11/13/01/32/47/85633671_p1.jpg', 
    #                      # 'https://o.acgpic.net/img-original/img/2020/11/13/01/32/47/85633671_p2.jpg', 
    #                      # 'https://o.acgpic.net/img-original/img/2020/11/13/01/32/47/85633671_p3.jpg', 
    #                      # 'https://o.acgpic.net/img-original/img/2020/11/13/01/32/47/85633671_p4.jpg', 
    #                      # 'https://o.acgpic.net/img-original/img/2020/11/13/01/32/47/85633671_p5.jpg', 
    #                      # 'https://o.acgpic.net/img-original/img/2020/11/13/01/32/47/85633671_p6.jpg', 
    #                      # 'https://o.acgpic.net/img-original/img/2020/11/13/01/32/47/85633671_p7.jpg', 
    #                      'https://o.acgpic.net/img-original/img/2020/11/13/01/32/47/85633671_p8.jpg'],
    #      ))
    
    make_json('draft_wallet')
    
    
    
    
    pass
    
    
    
    
    
    
    
    