import os
import time
import demjson

class Fplog():
    def __init__(self,filename):
        self.filename=filename+'_'+getime()+'.txt'
        newpath(self.filename)
        self.fp=open(self.filename,'w')
    def add(self,message,t=True):
        self.fp=open(self.filename,'a+')
        self.fp.write('{}{}\n'.format(getime()+' : ' if t else '',message))
        self.fp.close()
    def close(self):
        self.fp.close()
    def __del__(self):
        self.close()
        
class Configs:
    def __init__(self,file='configs.json'):
        fp=open(file)
        js=fp.read()
        fp.close()
        cfg=demjson.decode(js)
        for k,v in cfg.items():
            self.__setattr__(k, v)
            
def newpath(path):
    d=os.path.split(path)[0]
    if os.path.exists(d):
        pass
    else:
        os.mkdir(d)         

class Timer():
    def __init__(self,sep=1):
        self.start=0
        self.sep=sep
    def T(self):
        if time.time()-self.start>self.sep:
            self.start=time.time()  
            return True
        else:
            return False

        
def getime():
    t=time.localtime()
    return time.strftime('%Y_%m_%d__%H_%M_%S',t)

def logprint(*log,logger=None,t=False,**kw):
    if logger:
        try:
            logger.add(' '.join(log),t=t)
        except:
            pass
    print(*log,**kw)
    
def cmd(command):
    import subprocess
    cmd=subprocess.getstatusoutput(command)
    print(('Success' if not cmd[0] else 'Fail') + ' Command:\n   '+command)
    print(cmd[1].replace('Active code page: 65001',''))

    
if __name__ == '__main__':
    
    print(Configs().qq)
    