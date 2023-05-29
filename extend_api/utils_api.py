import re
import os
import time
import json
import random


class Auto_model():
    def __init__(self,model_dir,model_name_like,model_extend_name='.pth'):
        self.model_dir=model_dir
        self.model_name_like=model_name_like
        self.model_extend_name=model_extend_name
        newpath(os.path.join(model_dir,model_name_like))
    
    def create_new(self,n=0):
        return os.path.join(self.model_dir,self.model_name_like+f'{n}{self.model_extend_name}')

    def auto_load(self,get_latest=False):
        all_model=os.listdir(self.model_dir)
        latest=None

        for _ in all_model:

            n=_.strip(self.model_name_like).strip(self.model_extend_name)
            n=int(n)
            if latest==None or n>latest:
                latest=n
        if get_latest:
            return latest
        if latest!=None:
            r=os.path.join(self.model_dir,self.model_name_like+f'{latest}{self.model_extend_name}')
            print(f'load model {r}')
            return r
        else:
            print('no model exist')
            return None
        
    def auto_save(self,n):
        r=os.path.join(self.model_dir,self.model_name_like+f'{n}{self.model_extend_name}')
        return r

def newpath(path,isfile=False):
    if path[0]=='/':
        Warning('your are editing the root directory')
    p=[]
    for i in range(10):
        if not os.path.exists(path):
            l,r=os.path.split(path)
            p.append(r)
        else:
            break
        path=l[:]
    if isfile:
        p=p[1:]
    for _ in p[::-1]:
        l=os.path.join(l,_)
        os.mkdir(l)   

def re_matchall(pattern,s):
    r=[]
    match=re.search(pattern,s)
    while match:
        r.append(match.group())
        s=s[0:match.span()[0]]+s[match.span()[1]:]
        match=re.search(pattern,s)
    return r

def re_args_get(msg,d,nolist=True):
    # dict{'arg_name':('as_name','type_name',default,is_single)}
    # types=['int','float_x','cnt','bool','str']
    result_d={}
    for i in list(d.items()):
        arg_name=i[0]
        as_name=i[1][0]
        type_name=i[1][1]
        default=i[1][2]
        try:
            is_single=i[1][3]
        except:
            is_single=True
        assert nolist==is_single
        
        if type_name=='cnt':
            match_=msg.count(as_name)
            result_d[arg_name]=match_ if nolist else [match_]
            continue
        elif type_name=='bool':
            match_=not default if msg.count(as_name) else default
            result_d[arg_name]=match_ if nolist else [match_]
            continue
        elif type_name=='bool+':
            match_=default[1] if msg.count(as_name) else default[0]
            result_d[arg_name]=match_ if nolist else [match_]
            continue
        else:
            matches=re_matchall(f'(?<!\w){as_name}(=| )?.+?( |$)',msg)
            if len(matches)==0:
                if type_name=='bool+':
                    result_d[arg_name]=default[0] if nolist else [default[0]]
                else:
                    result_d[arg_name]=default if nolist else [default]
                    
            elif is_single and len(matches)>=2:
                raise Exception(f'single err in arg {as_name}')
            else:
                arg_list=[]
                for match in matches:
                    msg=msg.replace(match,'')
                    match_=match.replace(f'{as_name}=','').\
                    replace(f'{as_name}','').replace(f'{as_name} ','')
                    if type_name=='int':
                        match_=int(match_)
                    elif type_name=='str':
                        match_=match_.strip(' ').strip('\n')
                    elif type_name.count('float'):
                        pcn=int(type_name[-1])
                        match_=round(float(match_),pcn)      
                    arg_list.append(match_)
                result_d[arg_name]=arg_list[0] if nolist else arg_list
    return result_d

def easy_request(url,header=None,format_url_args=None,
                 data=None,method='GET',driver=False,pic=False,form_data=None):
    
    from urllib.parse import quote
    import requests
    import json
    from bs4 import BeautifulSoup as bs
    
    if format_url_args:
        url=url.format(*list( map(quote,format_url_args) ))
    if header and isinstance(header,str):
        with open(header) as fp:
            header=json.load(fp)
    if data:
        data=json.dumps(data)
    
    if not driver:
        if pic:
            return requests.request(method,url,
                              headers=header,
                              data=data,
                              )
        if form_data:
            from requests_toolbelt import MultipartEncoder
            custom_data=MultipartEncoder(fields=form_data[0],boundary=form_data[1])
            if not header:
                header={}
            header['Content-Type']=custom_data.content_type
            response=requests.post(url,
                              headers=header,
                              data=custom_data,
                              ).content
        else:
            response=requests.request(method,url,
                                  headers=header,
                                  data=data,
                                  ).content
    else:
        from selenium import webdriver
        browser = webdriver.Chrome()
        browser.get(url)
        data = browser.page_source
        browser.quit()
        soup=bs(data,features="lxml")   
        response=soup.find('body').text
        return response
    
    try:
        if isinstance(response,bytes):
            response=str(response,encoding='utf8')
            return response
    except:
        pass
    try:
        data=json.loads(response)
        return data

    except :
        soup=bs(response,features='lxml')
        return soup

def truepath(file,*arg):
    return os.path.join(os.path.abspath(os.path.split(file)[0]),*arg)

def url_imshow(urlcontent,headers=None,show=True):
    from PIL import Image
    from io import BytesIO
    # import urllib.request as request
    # response = request.urlopen(urlcontent)
    image = Image.open(BytesIO(urlcontent))
    if show:
        image.show()
    else:
        return image

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
    
    make_json('chatGPT2_cookies')
    
    # s=easy_request('https://api.yimian.xyz/img',pic=True)
    # url_imshow(s.content)
    
    
    
    pass
    
    
    
    
    
    
    
    