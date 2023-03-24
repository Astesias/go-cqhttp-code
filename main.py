import time
import random
import asyncio
import threading
import traceback
from api import send_msg
from flask import Flask, request
from flask_restful import Resource, Api
from msg_filter import sent_msg,cleanCache
from utils import Fplog,logprint,cmd,Timer,Configs

configs=Configs('configs.json')

logger=Fplog('./log/main/log')
def print(log,logger=logger,**kw):
    logprint(log,logger=logger,t=True,**kw)
    
import queue
TASK=queue.Queue(maxsize=20)

class Recver(Resource):
    def get(self):
        return TASK.qsize()
    def post(self):
        _ = request.json
        global TASK
        if _.get('post_type')=='message' or _.get('post_type')=='message_sent':
            TASK.put_nowait(_)
            
def sender1():
    while 1:
        t=TASK.get()
        sent_msg(t)
        TASK.task_done()
def sender2():
    while 1:
        t=TASK.get()
        sent_msg(t)
        TASK.task_done()
def sender3():
    while 1:
        t=TASK.get()
        sent_msg(t)
        TASK.task_done()

def say(pid=configs.test_group,is_group=True):
    test_json={\
     'post_type': 'message',
     'message_type': 'group',
     'self_id': configs.qq,
     'font': 0,
     'message': '',
     'group_id': configs.test_group,
     'sender': {'age': 0, 
                'nickname': '测试用例',
                'sex': 'unknown',
                'user_id': configs.qq},
     'user_id': 2854196310,
     'message_id': 1618317904
     }
        
    while 1:
        try:
            ip=input()
            if ip[0]==':':
                ip=ip.strip(':')
                print(eval(ip))
                continue
            message=f'[CQ:at,qq={configs.qq}]'+ip
            test_json['message']=message
            test_json['raw_message']=message
            
            test_json['font']=10 # selfFlag
            
            test_json['message_type']='group' if is_group else 'private'
            if not is_group:
                test_json['sender']['user_id']=pid
            else:
                test_json['group_id']=pid
                
            test_json['message_seq']=random.randint(1000,3000) # diff data
            
            # print(test_json)
            sent_msg(test_json)
        except:
            print('Error occured:')
            print(traceback.format_exc()[-80:])
            print('T2 dead')
            print('Restart T2')

    
def go_cqhttp():
    cmd('cd .. && ./go-cqhttp.exe -faststart')

def timer(uid=configs.test_group,is_group=True):
    ping=Timer(10*60)
    while 1:
        try:
            if ping.T():
                time.sleep(random.randint(0,20))
                t=time.strftime('%m%d|%H:%M:%S',time.localtime())
                asyncio.run(send_msg(uid,t+' Bot is running',is_group=True))
        except:
            # TODO restart
            pass

def main(address):  
    isDead=False
    _=1
    while 1: 
        try:
            if _ or isDead:
                app.run(*address)
                asyncio.run(cleanCache())
                _=0
                isDead=False
        except:
            print('Error occured:')
            print(traceback.format_exc())
            isDead=True
            _=1
            print('main dead')
            print('Restart main')  
            time.sleep(5)
            
        
if __name__ == '__main__':
    
    app = Flask(__name__)
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=unicode"
    api = Api(app)
    api.add_resource(Recver, "/", endpoint="index")
    
    main_=threading.Thread(target=main,args=[configs.address.split(':')])
    say_=threading.Thread(target=say,args=[configs.test_group,True])
    timer_=threading.Thread(target=timer)
    sender1_=threading.Thread(target=sender1)
    sender2_=threading.Thread(target=sender2)
    sender3_=threading.Thread(target=sender3)
    go_cqhttp_=threading.Thread(target=go_cqhttp)
    
    global tasks
    tasks=[main_,say_,timer_,go_cqhttp_,sender1_,sender2_,sender3_]
    import sys
    if len(sys.argv)>1 and int(sys.argv[1]) :
        pass
    else:
        tasks.remove(go_cqhttp_)
    tasks.remove(timer_)
    # tasks.remove(say_)
    
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()


# order_list (kw=|kw |kw)
#   {question}                                        (chatGPT)           # 聊天机器人
#   {发图}*n                                          (randomPic)         # 随机图片
#   pie {kw} pn pg ix nc                              (Pixivel)           # Pixivel图片搜索
#   pic {pid}                                         (Pixivic by pid)    # Pixivic pid搜索(年龄限制)
#   pic {date}xxxxxx mode (f)male/dwm                 (Pixivic by date)   # Pixivic 模式搜索(年龄限制)

#   aidraw  {kw} ukw ek(0-1%2) sz ori 2-3 [image]     (aidraw)            # 盗梦师ai作画
#            ["1:1" , "9:16", "16:9",'xxx', "3:4" ,"4:3"] index 1-6

#   baidraw {kw}  ["1:1","16:9","9:16","3:2","4:3"]   index 1-5           # 百度ai作画                
#   baidraw {kw} ek(1-10)  sz (ori 2-6) [image]       (baidu_aidraw)      

#   daidraw {kw} ek(0-1%1) sz(min-max) md [image]     (daidu_aidraw)      # draft ai作画
#                            md:(0-100 2,3,18,36,37,38,44[nxd])

#   ping                                              (Ping)              # ping服务器所有模块 

#   help                                              (help)              # 获取帮助信息

'''
Example
@bot/@ (in private chat) +
    chatgpt who jb you
    pie kw=关键词 pg=2 i=1
    pic pid=114514
    pic date230101 mode male
    aidraw  kw白发，长发，红瞳 ukw手部描写 ek0.3 sz ori [image]
    baidraw kw白发，长发，红瞳 sz ek0.3 ori [image]
    daidraw kw白发，长发，红瞳
    roll {n}d{m}
    help {module name}
    
    ping
'''


'''
TODO
pic bug

usage config
cookie command
api ops  
configs extend

setup env

draft search other
bing
'''








