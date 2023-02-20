def single_image(file=None,url=None,):
    assert file==None or url==None
    if file:
        return f'[CQ:image,file={file}]'
    else:
        return f'[CQ:image,url={url}]'

def muti_image(list_,is_url=False):
    s=''
    for i in list_:
        if is_url:
            s+=single_image(url=i)
        else:
            s+=single_image(file=i)
    return s

def image(file_or_url,is_url=False):
    if isinstance(file_or_url,str):
        if is_url:
            return single_image(url=file_or_url)
        else:
            return single_image(file=file_or_url)
    elif isinstance(file_or_url,(list,tuple)):
        return muti_image(file_or_url,is_url)
    else:
        raise ValueError

def at(qq):
    return f'[CQ:at,qq={qq}]'