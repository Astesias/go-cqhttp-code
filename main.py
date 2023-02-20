import sys
import time
import random
import asyncio
import threading
import traceback
from api import send_msg
from flask import Flask, request
from flask_restful import Resource, Api
from msg_filter import sent_msg,cleanCache
from utils import Fplog,logprint,configs,cmd,Timer

logger=Fplog('./log/main/log')
def print(log,logger=logger,**kw):
    logprint(log,logger=logger,t=True,**kw)
    
import queue
TASK=queue.Queue(maxsize=20)

class Recver(Resource):
    def get(self):
        return TASK
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

def say(pid=657696854,is_group=True):
    test_json={\
     'post_type': 'message',
     'message_type': 'group',
     'self_id': configs.qq,
     'font': 0,
     'message': '',
     'group_id': 657696854,
     'sender': {'age': 0, 
                'nickname': '测试用例',
                'sex': 'unknown',
                'user_id': '2264168148'},
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
    cmd('cd .. && .\go-cqhttp.exe -faststart')

def timer(uid=configs.server_group["文件传输助手"],is_group=True):
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
    say_=threading.Thread(target=say,args=[configs.server_group["文件传输助手"],True])
    timer_=threading.Thread(target=timer)
    sender1_=threading.Thread(target=sender1)
    sender2_=threading.Thread(target=sender2)
    sender3_=threading.Thread(target=sender3)
    go_cqhttp_=threading.Thread(target=go_cqhttp)
    
    global tasks
    tasks=[main_,say_,timer_,go_cqhttp_,sender1_,sender2_,sender3_]
    if not len(sys.argv)>=2:
        tasks.remove(go_cqhttp_)
        pass
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

'''
@ysl +
    我是谁我从哪里来我要去哪里
    pie kw=原神 pg=2 i=1
    pic pid=114514
    pic date230101 mode male
    aidraw  kw白发，长发，红瞳 ukw手部描写 ek0.3 sz ori [image]
    baidraw kw白发，长发，红瞳 sz ek0.3 ori [image]
    daidraw kw白发，长发，红瞳
    
    ping
'''


# TODO
    # draft search other
    # help
    
    # seach author  x
    # pix pn show all  x
    # random sent daily  x
    # top sent daily   x
    # restart   x
    
# 974996372   b
# 657696854   s
# 1206094636  ych

# [CQ:at,qq=2264168148]aidraw斑驳的阳光,美丽的少女,秋千,蓝宝石般的眼珠,纱裙,露肩,浅白色露肩长裙,幽静,萝莉,罗马柱,白花,兰花,长筒靴,复古色,丁达尔效应,神圣的教堂,红色瞳孔,金黄色长发,小巧的脸蛋,丰满的身材














