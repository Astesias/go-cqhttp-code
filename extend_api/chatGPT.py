import json
import urllib3 
from urllib import parse

def chat(question,retry=3):
    
    url = 'http://chat.h2ai.cn/api/trilateral/openAi/completions?prompt={}\
    &openaiId=101527734469956768286371869843052352044700336730028'
    url=url.format(parse.quote(question))
    
    T=flag=1
    while T<20 and flag:
        http=urllib3.PoolManager()  
        html= http.request("GET", url)
        try:
            js=json.loads(html.data)
            flag=0
        except:
            pass
        
    if T>=20:
        return '连接失败'
    else:
        try:
            data=js['data']['choices'][0]['text'].replace('<br/>','\n').strip('\n')
        except:
            # print(js)
            data='request failed'
            if js['code']==200 and retry:
                data=chat(question,retry-1)
        return data

if __name__ == '__main__':
    print(chat('你是谁'))