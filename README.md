go-cqhttp-code
====
基于go-cqhttp的qq机器人功能代码实现<br>
仅供参考<br>

order_list: (选项后加空格等号或不加都可识别)
---
>  {question}													  (chatGPT)           # 聊天机器人<br>
   {发图}*n                                          (randomPic)         # 随机图片<br>
   pie {kw} pn pg ix nc                              (Pixivel)           # Pixivel图片搜索<br>
   pic {pid}                                         (Pixivic by pid)    # Pixivic pid搜索(年龄限制)<br>
   pic {date}xxxxxx mode (f)male/dwm                 (Pixivic by date)   # Pixivic 模式搜索(年龄限制)<br><br>
   aidraw  {kw} ukw ek(0-1%2) sz ori 2-3 [image]     (aidraw)            # 盗梦师ai作画<br>
            ["1:1" , "9:16", "16:9",'xxx', "3:4" ,"4:3"] index 1-6<br><br>
   baidraw {kw}  ["1:1","16:9","9:16","3:2","4:3"]   index 1-5           # 百度ai作画            
   baidraw {kw} ek(1-10)  sz (ori 2-6) [image]       (baidu_aidraw)<br><br>
   daidraw {kw} ek(0-1%1) sz(min-max) md [image]     (daidu_aidraw)      # draft ai作画<br>
                            md:(0-100 2,3,18,36,37,38,44[nxd])<br><br>
   roll {n}d{m}                                      (roll)              # roll点<br> 
   ping                                              (Ping)              # ping服务器所有模块<br> 
   help                                              (help)              # 获取帮助信息<br>


Examples:
--
>@bot/@ (in private chat) +<br>
>>
    chatgpt who jb you
    pie kw=关键词 pg=2 ix=1
    pic pid=114514
    pic date230101 mode male
    aidraw  kw白发，长发，红瞳 ukw手部描写 ek0.3 sz ori [image]
    baidraw kw白发，长发，红瞳 sz ek0.3 ori [image]
    daidraw kw白发，长发，红瞳
    roll 2d100
    help chatgpt
    ping

