import httpx
from utils import Configs
configs=Configs('configs.json')

global Base_url
Base_url=configs.base_url

async def send_msg(uid,message,base_url=Base_url,is_group=True,bf='',ex=''):
    message=message.strip('\n')
    message=bf+message+ex
    async with httpx.AsyncClient(base_url=base_url,timeout=None) as client:
        if not is_group:
            params = {
                "user_id": uid,
                "message": message,
            }
            await client.get("/send_private_msg", params=params)
        else:
            params = {
                "group_id": uid,
                "message": message,
            }
            await client.get("/send_group_msg", params=params)  
        
async def clean_cache(base_url=Base_url):
    async with httpx.AsyncClient(base_url=base_url,timeout=None) as client:
            await client.get("/clean_cache")
