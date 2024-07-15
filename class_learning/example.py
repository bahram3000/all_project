import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl as ex

path = 'C:\\Users\\ADMIN\\AppData\\Roaming\\MetaQuotes\\Terminal\\D0E8209F77C8CF37AD8BF550E51FF075\\MQL5\\Files'
file = path + '\\BTCUSD-D1.prn'
btc_data = pd.read_csv(file)
print(btc_data.tail(5))
close = btc_data['<CLOSE>']
print(close)
s = plt.plot(close)
plt.show()
path2 = "C:\\Users\\ADMIN\\Desktop\\my project\\currecies.xlsx"
plt.savefig('BTCUSD')

curr_data = pd.read_excel(path2)
print(curr_data)
c = curr_data.loc[0][1:]
print(c)
plt.plot(c)
plt.show()
plt.savefig('CHFINF')
usdchf = curr_data.loc[10][35:]
plt.plot(usdchf)
plt.show()
