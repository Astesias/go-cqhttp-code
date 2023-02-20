import os
import re
import json
from urllib.parse import quote
from pysl import re_args_get,easy_request

try:
    from .utils_api import truepath,img_writer
    from utils import Fplog,logprint
    path=truepath(__file__,'../log/extend_api/pixivel/log')
    logger=Fplog(path)
    def print(*log,logger=logger,**kw):
        logprint(*log,logger=logger,t=True,**kw)
except:
    from utils_api import truepath,img_writer

def img_args(msg):

    d={
        'keyword':('kw','str',-1),
        'pn':('pn','int',1),
        'page':('pg','int',1),
        'index':('ix','int',1),
        'nocache':('nc','bool',False)
      }
    
    r=re_args_get(msg, d)

    return r

def image_msg(t):
    pid=t.get('pid')
    author=t.get('author')
    title=t.get('title')
    tag=t.get('tag')
    likers=t.get('likers')
    markers=t.get('markers')
    totalPn=t.get('totalPn')
    totalIndex=t.get('totalIndex')
    pageHaveNext=t.get('pageHaveNext')
    rank=t.get('rank')
    reload=t.get('reload')

    s=('Request failed and load next\n' if reload else '')+\
f'ID:{pid} 作者:{author}\n\
标题:{title} 主标签:{tag}\n\
喜欢:{likers} 收藏:{markers}\n\
页数:{totalPn} 搜索结果:{totalIndex}\n\
级别:{rank} 尾页:{pageHaveNext}'
    return s

def load_cache(kw,page,root='../cache/pixivel'):
    cache_name='kw_{}_{}.txt'.format(kw,page)
    path=truepath(__file__,root,cache_name)
    with open(path,'r') as fp:
        response=fp.read()
    print('load cache',cache_name)
    return response

def save_cache(kw,page,response,root='../cache/pixivel'):
    cache_name='kw_{}_{}.txt'.format(kw,page)
    path=truepath(__file__,root,cache_name)
    # if not os.path.exists(path):
    with open(path,'w') as fp:
        fp.write(response)
    print('save cache',cache_name)

def search(keyword,index=1,pn=1,page=1,nocache=False,response=None,reload=False):
    
    index-=1
    pn-=1
    page-=1
    url='https://api.pixivel.moe/v2/pixiv/tag/search/{}?page={}&sortpop=true&sortdate=false'.format(quote(keyword),page)
    

    try:
        if not nocache:
            response=load_cache(keyword,page)
    except:
        pass
        
    if not response:

        response=easy_request(url,driver=True)
        # browser = webdriver.Chrome()
        # browser.get(url)
        # data = browser.page_source
        # browser.quit()
        # soup=bs(data,features="lxml")   
        # response=soup.find('body').text
        
    h=json.loads(response)['data']['illusts']
    h.sort(key=lambda x:x['statistic']['likes'],reverse=True)
    pageHaveNext='是' if not json.loads(response)['data']['has_next'] else '否'
    totalIndex=len(h)

    image=h[index]['image']
    pid=h[index]['id']
    totalPn=h[index]['pageCount']
    title=h[index]['title']
    rank=h[index]['sanity']
    likers=h[index]['statistic']['likes']
    markers=h[index]['statistic']['bookmarks']
    tag=h[index]['tags'][0]['name']
    try:
        try:
            author=re.search('- .+的插画',h[index]['altTitle'])[0].strip('的插画').strip('- ')
        except:
            author=re.search('.+的插画',h[index]['altTitle'])[0].strip('的插画').strip('- ')
    except:
        print(h[index]['altTitle'])
        author='Unkonwn'
    
    for _ in ('T','-',':'): 
        image=image.replace(_,'/')
     # 2021/02/05/09/49/44
    
    base=f'https://proxy.pixivel.moe/img-master/img/{image}/{pid}_p{pn}_master1200.jpg'
    
    save_cache(keyword,page,response)
    if rank>=0:
        urlbase=base
        print(base)
        base=img_writer(url=base)[0]
        if os.stat(truepath(__file__,'../../data/images',base)).st_size<3000:
            if index+1>=totalIndex:
                index=1
                pn=1
                page+=2
            else:
                index+=2
                pn=1
                page+=1
            print(f'Fail load and load next,try page:{page} index:{index} pn:{pn} (web image loss)')
            
            return search(keyword,index,pn,page,response=response,reload=True)
    
    return  {
            'file_name':base,
            'pid':pid,
            'author':author,
            'title':title,
            'tag':tag,
            'likers':likers,
            'markers':markers,
            'totalPn':totalPn,
            'totalIndex':totalIndex,
            'pageHaveNext':pageHaveNext,
            'rank':rank,
            'reload':reload,
            'url':urlbase,
            }

if __name__ == '__main__':
    # print(img_args('pie kw=洛天依 ix5  pg4 pn2 nc'))
    
    # print(search(keyword='洛天依',index=6,pn=1,page=1,nocache=True))

    pass












