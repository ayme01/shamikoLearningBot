import re
import MeCab
import time
import random
import sys
from mastodon import Mastodon
from collections import deque

def format_text_filter(text_list):
    conv = re.compile(r"<[^>]*?>")
    format_list = []
    for line in text_list:
        line = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", line)
        line = re.sub(r'\u200b', "", line)
        line = re.sub(r':[^:]+:',"",line)
        line = re.sub(r'@.*', "", line)
        line = re.sub(r'#.*', "", line)
        line = re.sub(r':.*', "", line)
        line = re.sub(r"<[^>]*?>", "", line)
        line = re.sub(r"\(.*", "", line)
        line = line.replace('\\', "")
        line = line.replace('*', "")
        line = line.replace('\n', "")
        line = line.replace('\u3000', "")
        line = line.replace('俺', "私")
        line = line.replace('僕', "私")
        line = line.replace('オレ', "私")
        line = line.replace('RT', "")
        line = line.replace('.', "")
        line = line.replace(' ', "")
        format_list.append(line)
        
    return format_list

def shamiko_word_list():
    text_list = []
    with open("./data/syamiko_words.txt", encoding='utf-8') as data:
        for line in data:
            char, text = line.rstrip('\n').split(" ")
            if char == "優子":
                text_list.append(text)
    return text_list

def mecab_analyze_list(word_list):
    text_model = []
    for list_macab in word_list:
        t = MeCab.Tagger("-Owakati")
        parsed_text = t.parse(list_macab).replace("\n", "")
        parsed_text_list = [None] + parsed_text.split() + [None]
        for i in range(len(parsed_text_list) - 2):
            model_word = parsed_text_list[i:i+3]
            text_model.append(model_word)
    return text_model

def mk_sentence(mecab_list):
    none_model = []
    for i in mecab_list:
        if None in i:
            text_list = i
            if text_list[0] == None:
                none_model.append(text_list)
    random_word = random.choice(none_model)
    if random_word[2] == None:
        return random_word[1]
    fast_word = random_word[1], random_word[2]
    sentence = []
    sentence += random_word[1]
    tes = []
    while fast_word:
        for i in mecab_list:
            ju = i[0], i[1]
            if ju == fast_word:
                tes += [i]
        random_word = random.choice(tes)
        sentence += random_word[1]
        fast_word = random_word[1], random_word[2]
        end_word = random_word[2]
        tes = []
        if end_word == None:
            break
    return sentence

def mk_filter_word(serihu):
    text_list = []
    with open("./data/filter.txt", encoding='utf-8') as data:
        for line in data:
            line = line.replace('\n', "")
            serihu= serihu.replace(line, "not") 
    return serihu

def mk_new_sentence(timeline):
    word_list = timeline + shamiko_word_list()
    mecab_word_list = mecab_analyze_list(word_list)
    serihu = "".join(map(str, mk_sentence(mecab_word_list)))
    
    return serihu
    # while True:
    #     sarch = serihu in word_list
    #     filter_judg = serihu in mk_filter_word(serihu)
    #     if serihu == []:
    #         serihu = "".join(map(str, mk_sentence(mecab_word_list)))
    #     elif filter_judg == False:
    #         mastodon.status_post(serihu,visibility='private')
    #         serihu = "".join(map(str, mk_sentence(mecab_word_list)))
    #     elif sarch == False:
    #         serihu = serihu.replace('シャミ子', "私")
    #         return serihu
    #     else:
    #         serihu = "".join(map(str, mk_sentence(mecab_word_list)))
    