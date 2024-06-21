from modules.syamiko_bot import ShamikoBotForMastdon,Stream
from mastodon import Mastodon
import json
import threading
def get_token_sauce():
    with open("./data/config.json", encoding='utf-8') as data:
        config_json = json.load(data)
        for obj in config_json:
            if 'client_id' in obj:
                return obj

def mk_post_sentence():
    token_obj = get_token_sauce()
    bot = ShamikoBotForMastdon(
        api_base_url = token_obj['api_base_url'],
        client_id = token_obj['client_id'],
        client_secret= token_obj['client_secret'],
        access_token = token_obj['access_token'] 
    )
    bot.main()

def stream_reply():
    token_obj = get_token_sauce()
    stromMastdon = Mastodon(
        api_base_url = token_obj['api_base_url'],
        client_id = token_obj['client_id'],
        client_secret= token_obj['client_secret'],
        access_token = token_obj['access_token'] 
    )

    stromMastdon.stream_user(Stream())

if __name__ == "__main__":
    thread_1 = threading.Thread(target=mk_post_sentence)
    thread_2 = threading.Thread(target=stream_reply)

    thread_2.start()
    thread_1.start()

