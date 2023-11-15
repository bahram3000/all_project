import numpy as np
import pandas as pd
import finpy_tse as tse

# bourse = bool(input('for get bourse enter 1 otherwise 0 :'))
# farabourse = bool(input('for get farabourse enter 1 otherwise 0 :'))
# payeh = bool(input('for get payeh enter 1 otherwise 0 :'))

path = input('Enter your path for save files like as C:\\Users\\ADMIN\\Desktop\\dir :')
symbols = tse.Build_Market_StockList(bourse=True, farabourse=True, payeh=True)
symbols.Name = symbols.index
symbols.drop(
    ['Panel', 'Sector', "Sub-Sector", 'Comment', 'Company Code(12)', 'Ticker(4)', 'Ticker(5)', 'Ticker(12)',
     'Sector Code', 'Sub-Sector Code', 'Panel Code'], axis=1, inplace=True)
symbols.reset_index(inplace=True)
symbols.drop('Ticker', axis=1, inplace=True)
symbols.index = symbols.Name
symbols.drop('Name', axis=1, inplace=True)
symbols.to_csv(path + '\\symbols.csv')


# print(symbols)
# print(symbols.index[1])
# print(symbols['Name'][1])

def export_data_by_name(name: str):
    file_name = symbols['Name(EN)'][name].replace('*', '').replace(' ', '_')
    file_name += '.prn'
    exp_f = open(path + '\\' + file_name, 'a')
    exp_f.write('<DTYYYYMMDD>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>')
    exp_f.write('\n')
    exp_df = tse.Get_Price_History(name, ignore_date=True, double_date=True)
    for i in exp_df.index:
        str_lne = str(exp_df.Date[i])[:10].replace('-',
                                                   '') + f',{exp_df.Open[i]},{exp_df.High[i]},{exp_df.Low[i]},{exp_df.Close[i]},{exp_df.Volume[i]}'
        exp_f.write(str_lne)
        exp_f.write('\n')
    exp_f.close()


method = int(input('if you have a list of symbols enter 1 else enter 0 :'))
while True:
    if method == 0 or method == 1:
        break
    method = int(input('if you have a list of symbols enter 1 else enter 0 :'))
# assert method == 1 or method == 0
if method == 1:
    inp = input('Enter your symbols with sapace,like as AAPL TSLA AMZN :')
    list_symbol = inp.split()
    for nme in list_symbol:
        if nme in symbols.index:
            export_data_by_name(nme)


elif method == 0:
    bourse = bool(int(input('for get bourse enter 1 otherwise 0 :')))
    farabourse = bool(int(input('for get farabourse enter 1 otherwise 0 :')))
    payeh = bool(int(input('for get payeh enter 1 otherwise 0 :')))
    dic = {'بورس': bourse, 'فرابورس': farabourse, 'پایه زرد': payeh, 'پایه نارنجی': payeh, 'پایه قرمز': payeh}
    for nme in symbols.index:
        if dic[symbols['Market'][nme]]:
            export_data_by_name(nme)
else:
    print("ERROR")
input('Press Any key to Exit :')
