from modules.syamiko_bot import ShamikoBotForMisskey
from mastodon import Mastodon
import json

def get_token_sauce():
    with open("./data/config.json", encoding='utf-8') as data:
        config_json = json.load(data)
        for obj in config_json:
            if 'client_id' not in obj:
                return obj

def mk_post_sentence():
    token_obj = get_token_sauce()
    bot = ShamikoBotForMisskey(
        api_base_url = token_obj['api_base_url'],
        access_token = token_obj['access_token'] 
    )
    
    serihu = bot.get_timeline()
    print(serihu)

mk_post_sentence()