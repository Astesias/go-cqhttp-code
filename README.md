# go-cqhttp-code

order_list (kw=|kw |kw)
   {question}                                        (chatGPT)           # 聊天机器人
   {发图}*n                                          (randomPic)         # 随机图片
   pie {kw} pn pg ix nc                              (Pixivel)           # Pixivel图片搜索
   pic {pid}                                         (Pixivic by pid)    # Pixivic pid搜索(年龄限制)
   pic {date}xxxxxx mode (f)male/dwm                 (Pixivic by date)   # Pixivic 模式搜索(年龄限制)

   aidraw  {kw} ukw ek(0-1%2) sz ori 2-3 [image]     (aidraw)            # 盗梦师ai作画
            ["1:1" , "9:16", "16:9",'xxx', "3:4" ,"4:3"] index 1-6

   baidraw {kw}  ["1:1","16:9","9:16","3:2","4:3"]   index 1-5           # 百度ai作画                
   baidraw {kw} ek(1-10)  sz (ori 2-6) [image]       (baidu_aidraw)      

   daidraw {kw} ek(0-1%1) sz(min-max) md [image]     (daidu_aidraw)      # draft ai作画
                            md:(0-100 2,3,18,36,37,38,44[nxd])

   ping                                              (Ping)              # ping服务器所有模块 

   help                                              (help)              # 获取帮助信息

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
