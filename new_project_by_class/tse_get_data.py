import os

import numpy as np
import pandas as pd
import finpy_tse as tse
import time
from persiantools.jdatetime import JalaliDate
from tqdm import tqdm
import requests


#
def get_path():
    try:
        path = input("Enter your Destination file location :")
        os.listdir(path)
    except Exception as e:
        path = os.getcwd()
        with open('errors.txt', 'a') as f:
            f.write(f'{e.__cause__}\n')
    return path


#
def internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False


#
def get_method():
    inp = input("Enter your get method (all=1,select=2,enter=3) :")
    if inp in ['1', '2', '3']:
        return inp
    else:
        get_method()


#
def create_log():
    if 'tse_log.txt' in os.listdir():
        with open('tse_log.txt', 'r') as f:
            if f.read() == '':
                f.close()
                with open('tse_log.txt', 'w+') as f:
                    f.write(f'{0},{time.localtime(time.time())[:3]},{JalaliDate.today()}\n')
                    # f.write('\n')
    else:
        with open('tse_log.txt', 'w') as f:
            f.write(f'{0},{time.localtime(time.time())[:3]},{JalaliDate.today()}\n')
            # f.write('\n')


#
def select_symbols(inp_symbols):
    select_symbol = []
    for i in inp_symbols.index:
        select = input(f'if you want this ticker(symbol) -> {i} <- enter 1 for end enter other key :')
        if select == '1':
            select_symbol.append(i)
        elif select == '0':
            continue
        else:
            break
    return inp_symbols.loc[select_symbol, :]


#
def enter_symbols(inp_symbols):
    enter_symbol = []
    while True:
        inp = input("Enter your Ticker(symbol) :")
        if inp in inp_symbols.index:
            enter_symbol.append(inp)
        else:
            break
    return inp_symbols.loc[enter_symbol, :]


#
def export_data(one_symbols, inp_start_date=None):
    if inp_start_date:
        get_df = tse.get_price_history(stock=one_symbols, start_date=inp_start_date, double_date=True)
        get_df = get_df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        get_df.Date = np.array([str(i)[:10].replace('-', '') for i in get_df.Date])
        get_df.reset_index(inplace=True)
        get_df.drop('J-Date', axis=1, inplace=True)
        get_df.rename(
            columns={'Date': '<DTYYYYMMDD>', 'Open': '<Open>', 'High': '<HIGH>', 'Low': '<LOW>', 'Close': '<CLOSE>',

                     'Volume': '<VOL>'}, inplace=True)
    else:
        get_df = tse.get_price_history(stock=one_symbols, ignore_date=True, double_date=True)
        get_df = get_df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        get_df.Date = np.array([str(i)[:10].replace('-', '') for i in get_df.Date])
        get_df.reset_index(inplace=True)
        get_df.drop('J-Date', axis=1, inplace=True)
        get_df.rename(
            columns={'Date': '<DTYYYYMMDD>', 'Open': '<Open>', 'High': '<HIGH>', 'Low': '<LOW>', 'Close': '<CLOSE>',

                     'Volume': '<VOL>'}, inplace=True)

    return get_df


#
def first_export_data(inp_symbols):
    base_path = get_path()
    for i in tqdm(inp_symbols.index):
        try:
            get_df = export_data(i)
            path = base_path + '\\' + inp_symbols['Name(EN)'][i].replace(' ', '_').replace('*', '_') + '.prn'
            # print(path)
            # print(get_df)
            time.sleep(1)
            get_df.to_csv(path)
        except Exception as e:
            with open('tse_errors.txt', 'a') as f:
                f.write(f'{time.localtime(time.time())[:3]}--{e.__cause__}--{e.__str__()}\n')


#
def second_export_data(inp_symbols, inp_start_date):
    base_path = get_path()
    for i in tqdm(inp_symbols.index):
        try:
            get_df = export_data(i, inp_start_date)
            path = base_path + '\\' + inp_symbols['Name(EN)'][i].replace(' ', '_') + '.prn'
            df = pd.read_csv(path)
            df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            get_df = pd.concat([df, get_df], axis=0)
            get_df.to_csv(path)
        except Exception as e:
            with open('tse_errors.txt', 'a') as f:
                f.write(f'{time.localtime(time.time())[:3]}--{e.__cause__}--{e.__str__()}\n')


#
create_log()
if internet_connection():
    with open('tse_log.txt', 'r') as f:
        msg = f.readlines()[-1].split(',')
    if msg[0] == '0':
        if 'symbols.xlsx' in os.listdir():
            # print('1',os.listdir())
            symbols = pd.read_excel('symbols.xlsx')
            symbols.index = symbols.Ticker
        else:
            symbols = tse.Build_Market_StockList(
                bourse=True,
                farabourse=True,
                payeh=True,
                detailed_list=True,
                show_progress=True)
            symbols.to_excel('symbols.xlsx')

        method = get_method()
        if method == '1':
            first_export_data(symbols)

        elif method == '2':
            selected = select_symbols(symbols)
            selected.to_excel('select_symbols.xlsx')
            # selected = selected['Name(EN)']
            first_export_data(selected)

        elif method == '3':
            entered = enter_symbols(symbols)
            entered.to_excel("enter_symbols.xlsx")
            # entered = entered["Name(EN)"]
            first_export_data(entered)
        with open('tse_log.txt', 'a') as f:
            f.write(f'{1},{time.localtime(time.time())[:3]},{JalaliDate.today()}\n')
    else:
        start_date_get = msg[-1].replace('\n', '')
        symbols = pd.read_excel('symbols.xlsx')
        inp = input('if you want continue same as past enter 1 else 0 :')
        if inp == '1':
            if 'select_symbols.xlsx' or 'enter_symbols.xlsx' not in os.listdir():
                uti_symbols = symbols["Name(EN)"]
                second_export_data(uti_symbols, start_date_get)
            elif 'select_symbols.xlsx' in os.listdir():
                uti_symbols = pd.read_excel('select_symbols.xlsx')
                second_export_data(uti_symbols, start_date_get)
            elif 'enter_symbols.xlsx' in os.listdir():
                uti_symbols = pd.read_excel('enter_symbols.xlsx')
                second_export_data(uti_symbols, start_date_get)
            with open('tse_log.txt', 'a') as f:
                f.write(f'{int(msg[0]) + 1},{time.localtime(time.time())[:3]},{JalaliDate.today()}\n')
        elif inp == '0':
            try:
                os.rmdir('select_symbols.xlsx')
                os.rmdir('enter_symbols.xlsx')
            except Exception as e:
                with open('tse_errors.txt', 'a') as f:
                    f.write(f'{time.localtime(time.time())[:3]}--{e.__cause__}--{e.__str__()}\n')
            method = get_method()
            if method == '1':
                second_export_data(symbols, start_date_get)
            elif method == '2':
                selected = select_symbols(symbols)
                selected.to_excel('select_symbols.xlsx')
                # selected = selected['Name(EN)']
                second_export_data(selected, start_date_get)
            elif method == '3':
                entered = enter_symbols(symbols)
                entered.to_excel("enter_symbols.xlsx")
                # entered = entered["Name(EN)"]
                second_export_data(entered, start_date_get)
            with open('tse_log.txt', 'a') as f:
                f.write(f'{int(msg[0]) + 1},{time.localtime(time.time())[:3]},{JalaliDate.today()}\n')
