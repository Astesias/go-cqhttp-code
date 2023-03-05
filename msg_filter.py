import cq
import time
import random
import asyncio
import traceback
from api import send_msg,clean_cache
from extend_api.chatGPT import chat
from extend_api.pixivel import search,img_args,image_msg
from extend_api.pixivic import search_by_pid,search_by_rank,search_setting
from extend_api.aidraw import draw_setting,draw,get_available
from extend_api.baidraw import baidu_aidraw,get_balance
from extend_api.daidraw import daidu_aidraw,get_db_available
from extend_api.utils_api import img_writers,clear_img_cache,img_writer,re_args_get
from extend_api.chatGPT2 import chat2

from utils import Fplog,logprint,Configs
configs=Configs('configs.json')
logger=Fplog('./log/filter/log')
def print(*log,logger=logger,**kw):
    logprint(*log,logger=logger,**kw)

global BACKDOOR_ROLL
BACKDOOR_ROLL=None

def sent_msg(_,at=True):
    
    r=json_rule(_)
    if r:
        sender,msg,pid,is_group,is_self,is_order=r
        if (cq.at(configs.qq) in msg or is_order or ('@'+configs.id in msg) ) and\
            (sender!=configs.id or is_order):
            
            msg=msg.replace(cq.at(configs.qq),'').replace('@'+configs.id,'')
            ex='\n# TEST ORDER #' if _.get("font") == 10 else ''
            if at and is_group:
                bf=cq.at(_["sender"]["user_id"])
            else:
                bf=''
            
            #### 1  self_test
            if is_self:
                if is_self==2:
                    asyncio.run(send_msg(pid,msg.replace('sself:','') ,is_group=is_group))   
                    _['message']=cq.at(configs.qq)+msg.replace('sself:','')
                    time.sleep(0.1)
                    sent_msg(_,at)
                else:
                    asyncio.run(send_msg(pid,msg.replace('self:','') ,is_group=is_group))   
                return
            #### 2  help
            elif msg.count('help'):
                help_api(msg,pid,is_group,bf=bf,ex=ex)  
            #### 3  ping
            elif msg.count('ping'):
                ping(pid,is_group,bf=bf,ex=ex)
            #### 4  random_pic
            elif msg.count('发图'):
                randomPic_api(msg,pid,is_group,num=msg.count('发图'),bf=bf,ex=ex)
                return
            #### 5  aidraw
            elif msg.count('aidraw'):
                aiDraw_api(msg,pid,is_group,bf=bf,ex=ex)
                return
            #### 6  pixivel
            elif msg.count('pie') and not msg.count('pixiv'):
                pixivel_api(msg,pid,is_group,bf=bf,ex=ex)
                return
            #### 7  pixivic
            elif msg.count('pic'):
                pixivic_api(msg,pid,is_group,bf=bf,ex=ex)
                return
            #### 8  roll
            elif msg.count('roll'):
                roll_api(msg,pid,is_group,target_usr=_["sender"]["user_id"],bf=bf,ex=ex)
                return
            ### 9 backdoor
            elif msg.count('backdoor'):
                backdoor(msg,target_usr=_["sender"]["user_id"],bf=bf,ex=ex)
                return
            #### 10  chatgpt2
            elif msg.count('chat'):
                if msg.count('-reset'):
                    msg=msg.replace('-reset','')
                    reset=True
                else:
                    reset=False
                chatgpt2_api(msg,pid,is_group,reset=reset,bf='')
                return
            #### 10  chatgpt
            elif not is_self:
                chatgpt_api(msg,pid,is_group,bf='')
                return
    else:
        pass

def json_rule(_,order_form='@ '):
    
    msg=_['message']
    r=is_server_(_,order_form)
    msg=msg.replace(order_form,'')
    if r:
        pid,is_group,is_self,is_order,sender,event=r
        
        print('',t=True)
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        event='recv' if event=='message' else 'send'
        print('event:{} {} ({})'.format('group' if is_group else 'private',event,pid))
        print('sender: {}\nmsg: {}\npid: {}\ngroup: {}\nself: {}\norder: {}'
          .format(sender,msg,pid,is_group,is_self,is_order))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n')
        return sender,msg,pid,is_group,is_self,is_order
    
    else:
        return None
        
def is_server_(_,order_form='@ '):
    
    msg=_['message']
    
    if 'self:' in msg:
        if 'sself:' in msg:
            is_self=2
            msg=msg.replace('sself:','')
        else:
            is_self=1
            msg=msg.replace('self:','')
    else:
        is_self=0
        
    is_order= order_form in _['message'] and (_['sender']['user_id']==configs.qq or _.get('message_type')=='private')
        
    is_group=False
    sender=_['sender']['nickname']

    event=_.get('post_type')
    if event=='message_sent':# 发送
        if _.get('message_type')=='private':
            pid=_['target_id']
            # print('event:private send_msg ({})'.format(pid))
            
        elif _.get('message_type')=='group':
            pid=_['group_id']
            is_group=True
            
    elif event=='message':# 接收
        if _.get('message_type')=='private':# 私聊
            pid=_['sender']['user_id']
            # print('event:private recv ({})'.format(pid))
            
        elif _.get('message_type')=='group':
            pid=_['group_id']
            # print('event:group recv ({})'.format(pid))
            is_group=True
    if (is_group and pid not in configs.server_group.values()) or\
        (not is_group and pid not in configs.server_private.values()):
            return None
    else:
        return pid,is_group,is_self,is_order,sender,event



def chatgpt_api(msg,pid,is_group,bf='',ex=''):
    q=chat(msg)
    r='\nQuestion: {}\nChatGPT: {}'.format(msg,q)
    # print(r)
    asyncio.run(send_msg(pid,r,is_group=is_group,bf=bf))   

def chatgpt2_api(msg,pid,is_group,reset=False,bf='',ex=''):
    q=chat(msg,reset=reset)
    r='\nQuestion: {}\nChatGPT: {}'.format(msg,q)
    # print(r)
    asyncio.run(send_msg(pid,r,is_group=is_group,bf=bf))    
    
def pixivel_api(msg,pid,is_group,bf='',ex=''):
    kws=img_args(msg)
    strarg='{0[0]}|{0[3]}|{0[1]}|{0[2]}'.format(list(kws.values()))
    bf=bf+strarg+'\n'
    r=search(**kws)
    try:
        asyncio.run(send_msg(pid,
                                '{}\n{}\n'
                                .format(cq.image(r['file_name']),image_msg(r)),
                                is_group=is_group,ex=ex,bf=bf))
    except:
         print('群消息发送失败: 账号可能被风控')
         try:
            print('retry url send_msg ')
            asyncio.run(send_msg(pid,
                                    '{}\n{}\n'
                                    .format(cq.image(r['url'],is_url=True),image_msg(r)),
                                    is_group=is_group,ex=ex,bf=bf))
         except:
             print('retry failed')
             asyncio.run(send_msg(pid,f'限制级太高图片寄了\n{r[-1]}\n',is_group=is_group,ex=ex,bf=bf))
    finally:
        pass
        # cleanCache()
         
def pixivic_api(msg,pid,is_group,bf='',ex=''):
    sets=search_setting(msg)
    picid=sets['pid']
    if picid==-1:
        urls=search_by_rank(**sets)
        search_msg=sets['search_msg']
        bf+=f'\n{search_msg}\n'
    else:
        urls=search_by_pid(picid)
        if urls:
            bf+=f'\npid {picid}\n'
    files=img_writers(url=urls,headers='pixivic_search_pid.json')
    cqmsg=cq.image(files) + ('' if urls else '\nsearch failed\nreturn random')
    asyncio.run(send_msg(pid,cqmsg,is_group=is_group,ex=ex,bf=bf))
    # cleanCache() 

def randomPic_api(msg,pid,is_group,num=1,bf='',ex=''):
    if num>10:
        num=10
    asyncio.run(send_msg(pid,
                            '随机图片'+\
                            '{}'.format(
                                cq.image(img_writer(num=num))),
                                is_group=is_group,ex=ex,bf=bf)
                                        )
         
def aiDraw_api(msg,pid,is_group,bf='',ex=''):
    if msg.count('baidraw'):
        msg=msg.replace('baidraw ','').replace('baidraw','')
        imageFile=baidu_aidraw(msg)
        if imageFile[0]==0:
            asyncio.run(send_msg(pid,
                                 cq.image(imageFile[1]),is_group=is_group,bf=bf,ex=ex))
        else:
            asyncio.run(send_msg(pid,
                                 imageFile,is_group=is_group,bf=bf,ex=ex))
    elif msg.count('daidraw'):
        msg=msg.replace('daidraw ','').replace('daidraw','')
        imageFile=daidu_aidraw(msg)
        if imageFile[0]==0:
            asyncio.run(send_msg(pid,
                                 cq.image(imageFile[1]),is_group=is_group,bf=bf,ex=ex))
        else:
            asyncio.run(send_msg(pid,
                                 imageFile,is_group=is_group,bf=bf,ex=ex))
    else:
        msg=msg.replace('aidraw ','').replace('aidraw','')
        kw=draw_setting(msg)
        imageUrl=draw(**kw)
        if imageUrl[0]==0:
            asyncio.run(send_msg(pid,
                                 cq.image(imageUrl[1]),is_group=is_group,bf=bf,ex=ex))
        else:
            asyncio.run(send_msg(pid,
                                 imageUrl,is_group=is_group,bf=bf,ex=ex))
     
def roll_api(msg,pid,is_group,target_usr=None,bf='',ex=''):
    msg=msg.strip('roll ')
    n,k=map(int,msg.split('d'))
    r=[random.randint(1,k) for _ in range(n)]
    if n !=1:
        ds='+'.join(map(str,r))
    else:
        ds=''
        
    global BACKDOOR_ROLL
    if n==1 and k==100 and BACKDOOR_ROLL:
        if BACKDOOR_ROLL[0]==int(target_usr) and 0<BACKDOOR_ROLL[1]<=k:
            ds=r=BACKDOOR_ROLL[1]
            BACKDOOR_ROLL=None
            asyncio.run(send_msg(pid,
                     f'{msg}\n={r}'
                     ,is_group=is_group,bf=bf,ex=ex))
            return
    asyncio.run(send_msg(pid,
                         f'{msg}\n{ds}={sum(r)}'
                         ,is_group=is_group,bf=bf,ex=ex))
    
def backdoor(msg,target_usr,bf='',ex=''):
    d={
       'tu':('tu','int',2264168148),
       'num':('num','int',2)
       }
    r=re_args_get(msg,d)
    tu=r['tu']
    if tu:
        target_usr=tu
    num=r['num']
    global BACKDOOR_ROLL
    BACKDOOR_ROLL=(target_usr,num)
    asyncio.run(send_msg(configs.test_group,
                     f'{target_usr} will get {num}'
                     ,is_group=True,bf='',ex=''))
    
        
def ping(pid,is_group,bf='',ex='',test=False):
    if not test:
        asyncio.run(send_msg(pid,'Bot is servering',is_group=is_group,bf=bf))
    
    a=get_available()
    b=get_balance()
    d=get_db_available()
    aidraw_process=f'printidea.com 剩余点数: {a} 预计可使用: {a//3}次\n'+\
                   f'yige.baidu.com 剩余点数: {b} 预计可使用: {b//2}次\n'+\
                   f'draft.art.com  剩余点数: {d} 预计可使用: {d}次\n'
    try:
        img_writers(url=search_by_pid(68296699),headers='pixivic_search_pid.json')
        pixivic_process='pixivic connect success'
    except:
        print(traceback.print_exc())
        pixivic_process='pixivic connect failed'
    try:
        search('ai',nocache=True)
        pixivel_process='pixivel connect success'
    except:
        print(traceback.print_exc())
        pixivel_process='pixivel connect failed'
    try:
        assert 'fail' not in chat('what is your name')
        chat_process='chatGPT connect success'
    except:
        chat_process='chatGPT connect failed'
    module_process=aidraw_process+'\n'.join([pixivic_process,pixivel_process,chat_process])
    if not test:
        asyncio.run(send_msg(pid,module_process,is_group=is_group,bf=bf+'\n'))
    else:
        print(module_process)
    
def help_api(msg,pid,is_group,bf='',ex=''):
    bf=bf.strip('\n')+'Help message\n'
    
    if msg.count('chat'):
        r='  help for chatGPT\n'+\
          '  order: {question}\n'+\
          '  description: chatGPT'
          
    elif msg.count('pie') or msg.count('pixivel'):
        r='  help for pixivel\n'+\
          '  order: (pie) {kw} pn pg ix nc\n'+\
          '  description: pixivel api'
          
    elif msg.count('pic') or msg.count('pixivic'):
        r=  'help for pixivic\n'+\
          '  order: pic {pid}\n'+\
          '         pic {date}xxxxxx mode (f)male/day/week/month\n'+\
          '  description: pixivic api'
          
    elif msg.count('baidraw'):
        r='  help for baidraw\n'+\
          '  order: {kw} ek(1-10%0) sz ori(cost+4) [image]\n'+\
          '  description: 百度ai作画'
                
    elif msg.count('daidraw'):
        r='  help for daidraw\n'+\
          '  order: {kw} ek(0-1%1) sz(1-n%0) md(0-100%0) [image]\n'+\
          '  description: draft ai作画'
          
    elif msg.count('aidraw'):
        r='  help for aidraw\n'+\
          '  order: {kw} ukw ek(0-1%2) sz ori(cost+1) [image]\n'+\
          '  description: 盗梦师ai作画'
          
    elif msg.count('ping'):
        r='  help for ping\n'+\
          '  order: {ping}\n'+\
          '  description: 检测所有模块'
          
    elif msg.count('发图'):
        r='  help for 发图\n'+\
          '  order: {发图}*n\n'+\
          '  description: 随机图片'
          
    else:
        r='orders list:\n'+\
          '  chat\n  pie(pixivel)\n  pic(pixivic)\n  aidraw\n  baidraw\n  daidraw\n  ping\n  发图\n'+\
          '\ntype help {order_name} for more information'
    asyncio.run(send_msg(pid,r,is_group=is_group,bf=bf))
    
    
def cleanCache():
    clean_cache()
    clear_img_cache(num=40)
    
    
if __name__ == '__main__':
    ping(configs.test_group,True,test=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    