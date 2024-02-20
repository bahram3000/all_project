import requests
import numpy as np
import pandas as pd
import sqlite3
import time
from tqdm import tqdm
import os
from random import randint
import string
#
def internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False
#
def adad_farsi_to_english(inp: str):
    dc = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'}
    out = ''
    for i in inp:
        if i in dc.keys():
            out += dc[i]
        else:
            out += ''
    if out.isdecimal():
        return int(out)
    else:
        return None
#
def get_tokens(inp_url, inp_json):
    out_tokens = []
    resp = requests.post(url=inp_url, json=inp_json)
    if resp.status_code == 200:
        data_v = resp.json()
        for j in data_v["web_widgets"]["post_list"]:
            try:
                out_tokens.append(j['data']['token'])
            except:
                continue
    else:
        return 0
    return out_tokens, data_v['last_post_date'], data_v['first_post_date']
#
def first_get_tokens(inp_url):
    f_post_date = 0
    #l_post_date = 0
    js_v = {"page": 0,
            "json_schema": {"category": {"value": "plot-old"}, "query": "زمین",
                            "sort": {"value": "sort_date"}},
            "last-post-date": int(str(time.time()).replace('.', ''))}

    try:
        l_p_date = requests.post(url=inp_url, json=js_v).json()['last_post_date']
    except:
        l_p_date = int(str(time.time()).replace('.', ''))
    out_tokens = []
    k = 0
    while True:
        json_v = {"page": k,
                  "json_schema": {"category": {"value": "plot-old"}, "query": "زمین",
                                  "sort": {"value": "sort_date"}},
                  "last-post-date": l_p_date}

        result = get_tokens(inp_url, json_v)
        if result == 0:
            break
        else:
            if k == 0:
                f_post_date = result[2]
            out_tokens += result[0]
            l_p_date = result[1]
            k += 1
    return out_tokens, l_p_date, f_post_date
#
def second_get_tokens(inp_url, end_date):
    f_post_date = 0
    out_tokens = []
    json_v = {"page": 0,
              "json_schema": {"category": {"value": "plot-old"}, "query": "زمین",
                              "sort": {"value": "sort_date"}},
              "last-post-date": int(str(time.time()).replace('.', ''))}
    try:
        l_p_date = requests.post(url=inp_url, json=json_v).json()['last_post_date']
    except:
        l_p_date = int(str(time.time()).replace('.', ''))
    k = 0
    while True:
        if l_p_date > end_date:
            js_v = {"page": k,
                    "json_schema": {"category": {"value": "plot-old"}, "query": "زمین",
                                    "sort": {"value": "sort_date"}},
                    "last-post-date": l_p_date}
            result = get_tokens(inp_url, js_v)
            if result != 0:
                if k == 0:
                    f_post_date = result[2]
                out_tokens += result[0]
                l_p_date = result[1]
            else:
                break
        else:
            break
    return out_tokens, l_p_date, f_post_date
#
def get_base_url(inp="https://api.divar.ir/v8/web-search/30/plot-old"):
    inp2 = input('Enter your url :')
    if inp2 == '':
        return inp
    else:
        return inp2
#
def get_base_url2(inp=None):
    if inp:
        return inp
    else:
        return "https://api.divar.ir/v8/web-search/30/plot-old"
#
def get_last_post_data(inp=None):
    if inp:
        return inp
    else:
        return int(str(time.time()).replace('.', ''))
#
def true_get_data2(inp_url, try_num, timeout):
    #o = string.ascii_letters + string.punctuation
    #c = 0
    make_url = inp_url
    for i in range(try_num):
        time.sleep(timeout)
        #print('-', end='')
        resp = requests.get(make_url)
        #make_url = make_url.replace('-', o[randint(0, len(o) - 1)])
        if resp.status_code == 200:
            page_ = resp.text
            if 'متر' in page_ and 'زمین' in page_ and 'متراژ' in page_ and 'قیمت کل' in page_ and 'قیمت هر متر' in page_:
                return resp
            else:
                continue
        else:
            continue
    return False
#
def extract_json_data(inp_url,try_num,timeout):
    true_req = true_get_data2(inp_url, try_num, timeout)
    if true_req is not False:
        out_data=[]
        page_json= true_req.json()
        for i in page_json['sections']:
            if i['section_name'] == 'TITLE':
                out_data.append(i['widgets'][0]['data']['title'])
            if i['section_name']=='LIST_DATA':
                out_data.append(adad_farsi_to_english(i['widgets'][0]['data']['value']))
                out_data.append(adad_farsi_to_english(i['widgets'][1]['data']['value']))
            if i['section_name'] == 'DESCRIPTION':
                out_data.append(i['widgets'][1]['data']['text'])
        if len(out_data)==4:
            return out_data
        else:
            return False
    else:
        return False
#
def get_data_by_tokens(inp_tokens,try_num,timeout):
    df_out=pd.DataFrame({'address':[],'description':[],'area':[],'price':[]})
    for i in tqdm(inp_tokens):
        dest_url=f"https://api.divar.ir/v8/posts-v2/web/{i}"
        dt=extract_json_data(dest_url,try_num,timeout)
        if dt is not False:
            df_out.loc[len(df_out.index)+1]=dt
    return df_out
#
def create_log():
    if 'log.txt' in os.listdir():
        with open('log.txt', 'r') as f:
            if f.read() == '':
                f.close()
                with open('log.txt', 'w+') as f:
                    f.write(f'{0},{time.time()}\n')
    else:
        with open('log.txt', 'w') as f:
            f.write(f'{0},{time.time()}\n')
#
create_log()
#
if internet_connection():
    try_num = 2
    timeout = 1
    with open('log.txt', 'r') as f:
        msg = f.readlines()[-1].split(',')
    if msg[0] == '0':
        tokens = first_get_tokens(get_base_url2())
        with open('log.txt', 'a') as f:
            f.write(f'{1},{time.time()},{tokens[1]},{tokens[2]}\n')
        df = get_data_by_tokens(tokens[0], try_num, timeout)
        df.to_excel('out_data.xlsx')
        con=sqlite3.connect('real_state.db')
        df.to_sql('out_data',con)
    else:
        finish_date=int(msg[-1].replace('\n',''))
        df=pd.read_excel('out_data.xlsx')
        tokens = second_get_tokens(get_base_url2(),finish_date)
        with open('log.txt', 'a') as f:
            f.write(f'{int(msg[0]) + 1},{time.time()},{tokens[1]},{tokens[2]}\n')
        df2 = get_data_by_tokens(tokens[0], try_num, timeout)
        df=pd.concat([df,df2],axis=0)
        df.to_excel('out_data.xlsx')
        con=sqlite3.connect('real_state.db')
        cur=con.cursor()
        cur.execute("DROP table out_data")
        df.to_sql('out_data',con)
