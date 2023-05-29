import re

def make_json(name):
    
    with open('temp.json') as fp:
        data=fp.read()
    # data='\n'.join(data)
    print(data)
    
    keys=re.findall('.+?(?=:): ',data)
    values=re.findall('(?<= ).+',data)
    
    with open(name+'.json','w') as fp:
        fp.write('{\n')
        for i,j in zip(keys,values):
            i=i.strip(': ')
            fp.write(f'\"{i}\": \"{j}\",\n')
        
        fp.write(r'"py": "ysl"')
        fp.write('\n}')

header='''\
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,et;q=0.8,ja;q=0.7,fr;q=0.6,en;q=0.5,es;q=0.4,ko;q=0.3,kn;q=0.2,nl;q=0.1,az;q=0.1,mr;q=0.1,la;q=0.1,ms;q=0.1,eo;q=0.1
content-length: 185
content-type: application/json
origin: https://chatgpt.ddiu.me
referer: https://chatgpt.ddiu.me/
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: cross-site
user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36
x-umami-cache: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3ZWJzaXRlIjp7IndlYnNpdGVJZCI6Nywid2Vic2l0ZVV1aWQiOiI5MTg2OTlmZC0wNzA0LTQwOGItYmRhMy0zZjI4YzFiZDlkMWIifSwic2Vzc2lvbiI6eyJpZCI6MTk2NzMyLCJzZXNzaW9uVXVpZCI6IjExMTg0MDMyLWVjMDMtNWY0Ni1iNjVjLWI1YmJmMjZiZTZmYiIsImhvc3RuYW1lIjoiY2hhdGdwdC5kZGl1Lm1lIiwiYnJvd3NlciI6ImNocm9tZSIsIm9zIjoiV2luZG93cyAxMCIsInNjcmVlbiI6IjE5MjB4MTA4MCIsImxhbmd1YWdlIjoiemgtQ04iLCJjb3VudHJ5IjoiQ04iLCJkZXZpY2UiOiJkZXNrdG9wIn0sImlhdCI6MTY3ODAxNDU2NX0.86wFggBC4bSPrnUjeQYO6fwd4Ijgid6130w3vREAoyo
'''



with open('./temp.json','w') as fp:
    fp.write(header)
make_json('temp_')