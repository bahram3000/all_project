import numpy as np
import pandas as pd


class home_for_rent():
    num_of_home = 0
    mort_interest = 0.03

    def __init__(self, square: int, mort: int, cash: float, loc: str):
        self.square = square
        self.mort = mort
        self.cash = cash
        self.loc = loc
        self.num_of_home += 1

    def total_rent(self):
        return self.cash + self.mort_interest * self.mort

    def avg(self):
        return self.total_rent() / self.square

    @classmethod
    def set_new_home(cls, str_):
        sq, mo, ca, lc = str_.split()
        sq = int(sq)
        mo = int(mo)
        ca = int(ca)
        return cls(sq, mo, ca, lc)


home1 = home_for_rent(170, 300, 4.5, 'danesh')
home2 = home_for_rent(75, 30, 3, 'boostan')
home3 = home_for_rent(85, 50, 4, '12farvardin')
home4 = home_for_rent(92, 130, 0, 'kh emem j sadegh')
home5 = home_for_rent(70, 30, 3.5, 'memar')
home6 = home_for_rent(70, 20, 6, 'emam reza')
home7 = home_for_rent(50, 20, 2, 'navab')
home8 = home_for_rent(80, 60, 3, 'mola fath')
home9 = home_for_rent(100, 100, 1, 'hemat')
home10 = home_for_rent(120, 300, 5, 'amir almom')
home11 = home_for_rent(103, 50, 5, 'bolvar sanat')
home12 = home_for_rent(110, 50, 3.5, 'sh janbazan')
home13 = home_for_rent(110, 50, 5, 'bolvar sanat')
home14 = home_for_rent(120, 70, 0, 'amirkabir')
home15 = home_for_rent(70, 120, 0.5, 'darb ata')
home16 = home_for_rent(75, 50, 2.5, 'kh 22 bahman')
home17 = home_for_rent(55, 70, 0.6, 'blv piroozi')
home18 = home_for_rent(90, 150, 0.5, 'maskan mehr')
home19 = home_for_rent(80, 20, 3.3, 'maskan mehr')
home20 = home_for_rent(90, 100, 2, 'fin koochak')
home21 = home_for_rent(78, 20, 3.3, 'kh mehraban')
home22 = home_for_rent(85, 100, 1.1, 'maskan mehr')
l = [home2, home3, home4, home5, home6, home7, home8, home9, home11, home13, home12,
     home14, home15, home16, home17,
     home18, home19,
     home20, home21, home22]
m = [i.avg() for i in l]
avg = np.array(m)
avg = avg[avg < 50]

print(np.mean(avg))


def rent_ex(arr, sq):
    mein_ = np.mean(arr)
    return sq *mein_


print(rent_ex(avg, 78))
print(home2.total_rent())