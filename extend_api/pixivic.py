import re
from datetime import datetime,timedelta

try:
    from .utils_api import truepath,re_args_get,easy_request
    from utils import Fplog,logprint
    path=truepath(__file__,'../log/extend_api/pixivic/log')
    logger=Fplog(path)
    def print(*log,logger=logger,**kw):
        logprint(*log,logger=logger,t=True,**kw)
except:
    from utils_api import truepath,re_args_get,easy_request

def flatten(l):
    r=[]
    for i in l:
        r.extend(i)
    return r

def search_setting(msg):

    date=re.search('date(=| )?.+?( |$)',msg)
    if date: 
        date=date[0]
        msg=msg.replace(date,'')
        date=date.replace('date=','').replace('date','').replace('date ','')   
        date=f'20{date[:2]}-{date[2:4]}-{date[4:6]}'
    else:
        date=(datetime.now()-timedelta(days=2)).strftime('%Y-%m-%d')
        
    d={
       'pg':('pg','int',1),
       'pz':('pz','int',5),
       'mode':('mode','str','male'),
       'maxpn':('maxpn','int',5),
       'allpn':('allpn','bool',False),
       'pid':('pid','str',-1)
      }
    r=re_args_get(msg,d)
    
    mode=r['mode']
    pg=r['pg']
    pz=r['pz']
    
    fdate=date.replace('-','')[2:]
    search_msg=f'{mode}|{fdate}|{pg}|{pz}'
    
    r['fdate']=fdate
    r['search_msg']=search_msg
    
    return r

def search_by_pid(pid=85633671,head_json='pixivic_search_pid.json',**kw):
    
    base_url='https://api.bbmang.me/illusts/{}'.format(pid)
    print(base_url)

    response=easy_request(base_url,header=truepath(__file__,head_json))
    try:     
        data=response['data']
        if __name__ == '__main__':
            print('level:',data['sanityLevel'])
    except:
        print(response)
        return None
    
    urls=data['imageUrls']
    ori_urls=[]
    for d in urls:
        ori_urls.append(d['original'].replace('i.pximg.net','o.acgpic.net'))
    return ori_urls

def search_by_rank(mode='day',date='2022-08-11',pg=1,pz=5,
                   head_json='pixivic_search_rank.json',allpn=False,maxpn=5,**kw):
    
    modes=['day','week','month','male','female']
    
    if mode not in modes:
        mode='day'
    pz+=1
    pz=30 if pz>30 else pz
    
    base_url='https://api.bbmang.me/ranks?page={}&date={}&mode={}&pageSize={}'\
                .format(pg,date,mode,pz)
    print(base_url)
    
    # with open(truepath(__file__,head_json)) as fp:
    #     head=json.load(fp)
    
    # http=urllib3.PoolManager()
    # r=http.request('GET',base_url,headers=head)
    # response=r.data
    response=easy_request(base_url,header=truepath(__file__,head_json))
    # print(response)
    data=response['data']
    
    ori_urls=[]
    for n,i in enumerate(data):
        ill=i['imageUrls']
        ori_urls.append([])
        cnt=1
        for j in ill:
            ori_url=j['original']
            if 'name' not in  ori_url:
                ori_urls[n].append(ori_url.replace('i.pximg.net','o.acgpic.net'))
            cnt+=1
            if not allpn or cnt>=maxpn:
                break
            
    ori_urls=flatten(ori_urls)
    return ori_urls

if __name__ == '__main__':
    
    # msg='pic pid132112 modefemale pz=4 pg 3 allpn maxpn=4'
    # print(search_setting(msg))
    
    # r=search_by_rank()
    # print(r)
    
    r=search_by_pid(pid=104442365)
    print(r)
    


        
        
        
        
        
        