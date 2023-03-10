import json
import time


try:
    from .utils_api import easy_request,truepath,Auto_model
    from utils import Fplog,logprint
    path=truepath(__file__,'../log/extend_api/chat2/log')
    logger=Fplog(path)
    def print(*log,logger=logger,**kw):
        logprint(*log,logger=logger,t=True,**kw)
except:
    from utils_api import easy_request,truepath,Auto_model

def write_content(file,content,role='user'):
    file=truepath(__file__,file)
    try:
        data=json.load(open(file))
    except:
        data=None
    if not data:
        data={'messages': [],
              "time":int(time.time()),
              "sign":"eeb5d58ed7d5979ea965fb44a1c28ff8a0f6f9c0cffc9392e4a176109766e6db"}
    data['messages'].append({'role': role, 'content': content})
    if len(data['messages'])>=200:
        data['messages']=data['messages'][100:]
    with open(file,'w') as fp:
        json.dump(data,fp,ensure_ascii=False,indent=2)


def chat2(question,reset=False):
    
    url='https://chatgpt.ddiu.me/api/generate'
    question=question.strip(' ').strip('\n')
    
    
    history=Auto_model(truepath(__file__,'../cache/chat'),
                       'cache_',
                       model_extend_name='.txt'
                       )
    data=None
    if history.auto_load(get_latest=True)==None: # first
        save_path=history.auto_save(0)
    elif not reset: # load
        load_path=history.auto_load()
        # print(open(load_path).read())
        data=json.load(open(load_path))
        data['messages'].append({'role': 'user', 'content': question})
        save_path=history.create_new(history.auto_load(get_latest=True))
    else:
        save_path=history.create_new(history.auto_load(get_latest=True)+1)
        
    write_content(save_path,question,role='user')
    
    if not data:
        data={'messages': [{'role': "user", 'content': question}],
              "time":int(time.time()),
              "sign":"eeb5d58ed7d5979ea965fb44a1c28ff8a0f6f9c0cffc9392e4a176109766e6db"}
    # for i in data['messages']:
    #     print(i['content'])
    # print(data)
        
    r=easy_request(url,data=data,method='POST',header=truepath(__file__,'chatGPT2.json'))
    
    if isinstance(r,str):
        r=r.strip(' ').strip('\n')
        write_content(save_path,r,role='assistant')
        return r

if __name__ == '__main__':
    r=(chat2('我刚刚问了什么',reset=False))
    rl=list(r)
    print(r)

# url_b='https://stats.ddiu.io/api/collect'
# payload={"type":"event","payload":{"website":"918699fd-0704-408b-bda3-3f28c1bd9d1b","hostname":"chatgpt.ddiu.me","screen":"1920x1080","language":"zh-CN","url":"/","event_name":"chat_generate"}}
# br=easy_request(url_b,data=payload,method='POST',header='chatGPT2_cookies.json')

