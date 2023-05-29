try:
    from .utils_api import easy_request,truepath
    # from utils import Fplog,logprint
    # path=truepath(__file__,'../log/extend_api/chat/log')
    # logger=Fplog(path)
    # def print(*log,logger=logger,**kw):
    #     logprint(*log,logger=logger,t=True,**kw)
except:
    from utils_api import easy_request,truepath

def chat(question):
    
    
    url='https://api.aichatos.cloud/api/generateStream'
    payload={'prompt': "你是谁",
            'userId': "#/chat/1681375700406",
            'network': True, 'system': "",
            'withoutContext': False}
    payload['prompt']=question
    data=easy_request(url,method='POST',data=payload,header=truepath(__file__,'headers/chatGPT.json'))
    #print('A: ',data)
    return data


if __name__ == '__main__':
    print(chat('你是谁'))