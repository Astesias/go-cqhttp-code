<div align="center">
  <h1>QQ-Bot server codes base on <a href="https://github.com/Mrs4s/go-cqhttp">go-cqhttp</a> </h1>
  <img src="https://img.shields.io/badge/Release-Ver1.0.0-blue.svg">
</div>
本项目仅供学习交流<br>

## 支持命令

orders     | required argment | optional argments | descriptions
:-----:    |:-----:           |:-----:            |:-----:
\          |Any Question but not in orders       |\                  |[chatGPT](https://chat.openai.com/) api
发图        |\                |发图{*n}                |随机二次元[图片](https://api.yimian.xyz/img)多张
pie|kw|pg ix pn nc|[Pixivel](https://pixivel.moe/)搜图接口
pic|\ |pg pz date mode maxpn allpn |  [Pixivic](https://pixivic.com/)排行接口
pic|pid|\ |  [Pixivic](https://pixivic.com/)搜图接口,查询失败会返回随机图片
aidraw|kw |ukw ek ori sz [image] | [盗梦师AI绘画](https://printidea.art/)接口
baidraw|kw |ek sz ori [image] | [百度AI绘画](https://yige.baidu.com/)接口,使用[预制promote](https://github.com/Astesias/go-cqhttp-code/blob/master/extend_api/aidraw.py#L72)加入kw
daidraw|kw |ek sz md [image] | [DraftAI绘画](https://draft.art/)接口
roll| {n}d{m} | \ | 随机取n个[1,m]区间的值
ping | \ | \ | 服务器模块测试
help | \ | {order_name} | 获取命令帮助信息 

## 参数详情
argments     | type | default | descriptions
:-----:    |:-----:           |:-----:            |:-----:
pid|int|\ |p站图片id
kw|str|\ |关键词(keyword\|promote)
ukw|str|\ |反向关键词(unkeyword\|depromote)
pg| int [1,] | 1 |搜索结果页(page)序
ix| int [1,] | 1 |页中作品序号(index)
pn| int [1,] | 1 |作品中图片序号(pic num)
date| date(YYMMDD) | now-2day |某日排行榜
mode| enmu(`day`,`week`,`month`,`male`,`female`)|`male` |排行依据
pz | int [1,10] | 5 | 展示top n
allpn | bool | False | 展示所有pn,默认只展示作品第一张
maxpn | int [1,10] | 5 | 一个最大展示数量(绑定allpn)
ek| int [0,10] | 3 | 生成图片与给定图片相似度
sz| int [1,]| index of 16:9 | 生成图片大小(各接口互异)<br>aidraw:[1:1, 9:16,16:9,6:13,3:4 ,4:3]<br>baidraw:[1:1,16:9,9:16,3:2,4:3]<br>draft不同模型支持size不同
md | int [0,100+] | 18| ai模型类别,不断更新中 
ori| bool | False |是否生成原图品质(耗费点数增加)
[image]| image | \ | 命令消息中的用于ai绘画参考的图片(只需图片无需参数名)

## 命令示例
>@bot/@ (in private) +<br>
>>
    what is your name
    pie kw=关键词 pg=2 ix=1
    pic pid=114514
    pic date230101 mode male
    aidraw  kw白发，长发，红瞳 ukw手部描写 ek3 sz ori [image]
    baidraw kw白发，长发，红瞳 sz ek3 ori [image]
    daidraw kw白发，长发，红瞳
    roll 2d100
    help chatgpt
    ping
    
* 使用命令时需@机器人qq(私聊时@空格)
* 参数名后可直接跟参数或使用空格或=后再加参数
* 参数结束后需加空格表示结束
* ai绘画合适的promote可参考ai绘画官网

## 接口详情
所有接口使用请求头中cookies以保持登录状态,过期后(不常)需登录原网址获取并更换
### chatGPT
* 使用国内代理接口
* 不稳定,可根据需求更换
### Pixivel & Pixivic
* 不支持r18
* 限制级过高可能无法发送
### ai绘画
* 每日可登录官网领取免费次数
* 盗梦师ai关键词较长，使用预置promote与depromote，出图质量较好，赠送点数较多
* 百度ai关键词较短，promote尽量为多个名词，出图质量一般，赠送点数很多
* draft模型数多，出图质量好，每天赠送20次当日次数，过期不累加
### 拓展
* 拓展接口可增加到[这里](https://github.com/Astesias/go-cqhttp-code/edit/master/msg_filter.py#L80)


