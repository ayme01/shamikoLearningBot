import re
from collections import deque
import random
import sys
import time
from mastodon import Mastodon,StreamListener
from misskey import Misskey
from modules.create_sentence import format_text_filter, mk_new_sentence
import json


class ShamikoBotForMastdon:
    '''
    マストドン用のシャミ子のセリフを作成するclassです。
    '''
    def __init__(self,api_base_url,client_id,client_secret,access_token):
        self._api_base_url = api_base_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = access_token

        self._mastdon = Mastodon(
            client_id = self._client_id,
            client_secret = self._client_secret,
            api_base_url = self._api_base_url,
            access_token = self._access_token
        )

    def get_timeline(self):
        text_list = []
        timeline = self._mastdon.timeline_home()
        conv = re.compile(r"<[^>]*?>")
        # 10件に出力
        for i in range(0, 20):
            line = conv.sub("", timeline[i]['content'])
            deq_list = line in text_list
            if line != "None" and line != "" and deq_list == False:
                text_list.append(line)

        return text_list
    
    def save_timeline(self,no_get_note):
        formatted_text_list = []
        with open("./data/sample_from_mastdon.txt", encoding='utf-8') as data:

            for line in data:
                text = line.rstrip('\n')
                formatted_text_list.append(text)
        
        if len(formatted_text_list) >= 100:
            del formatted_text_list[0:10]
        
        if no_get_note:
            text_list = self.get_timeline()
            format_text_list = format_text_filter(text_list)
            formatted_text_list = list(set(formatted_text_list + format_text_list))
        else:
            pass

        with open('./data/sample_from_mastdon.txt', 'a') as f:
            f.truncate(0)
            for i in formatted_text_list:
                    print(i, file=f)

        return formatted_text_list
        
    def create_sentence(self,no_get_note = True):
        text_list = self.save_timeline(no_get_note)
        format_text_list = format_text_filter(text_list)
        serihu = mk_new_sentence(format_text_list)
        return serihu

    def mk_sentence_post_noete(self):
        serihu = self.create_sentence()
        self._mastdon.status_post(serihu,visibility='unlisted')
    
    def main(self):
        while True:
            print('test')
            self.mk_sentence_post_noete()
            for i in range(60):
                print(f"{i}秒経過")
                time.sleep(1)

def get_timeline(no_get_note):
    formatted_text_list = []
    with open("./data/sample_from_mastdon.txt", encoding='utf-8') as data:
        for line in data:
            text = line.rstrip('\n')
            formatted_text_list.append(text)

    return formatted_text_list
        

def create_sentence(no_get_note = False):
    text_list = get_timeline(no_get_note)
    format_text_list = format_text_filter(text_list)
    serihu = mk_new_sentence(format_text_list)
    return serihu


def get_token_sauce():
    with open("./data/config.json", encoding='utf-8') as data:
        config_json = json.load(data)
        for obj in config_json:
            if 'client_id' in obj:
                return obj

def main(content,st,id):
    token_obj = get_token_sauce()
    mastodon = Mastodon(
        api_base_url = token_obj['api_base_url'],
        client_id = token_obj['client_id'],
        client_secret= token_obj['client_secret'],
        access_token = token_obj['access_token'] 
    )

    mastodon.status_reply(st,create_sentence(),id,visibility='unlisted') #未収載


class Stream(StreamListener):
    def __init__(self): #継承
        super(Stream, self).__init__()
        # self.logger = logging.getLogger

    def on_notification(self,notif): #通知が来た時に呼び出されます
        if notif['type'] == 'mention': #通知の内容がリプライかチェック
            content = notif['status']['content'] #リプライの本体です
            id = notif['status']['account']['username']
            st = notif['status']
            main(content,st,id)
            
            # print('constnent=>',content,'asdasdfasdfid=>', id, 'asdfasdfasdfst=>',st)
            

        

class ShamikoBotForMisskey:

    def __init__(self,api_base_url,access_token):
        self._api_base_url = api_base_url
        self._access_token = access_token

        self._mk = Misskey(api_base_url, i = access_token)

    def get_timeline(self):
        text_list = []
        timeline = self._mk.notes_timeline()
        print(timeline)
        #visibilityがパブリックのものを抽出
        return timeline
        #conv = re.compile(r"<[^>]*?>")
        # 10件に出力
        #for i in range(0, 20):
        #    line = conv.sub("", timeline[i]['content'])
        #    deq_list = line in text_list
        #    if line != "None" and line != "" and deq_list == False:
        #        text_list.append(line)
