def remove_substr(primal: str, intended: str):
    ln_pr = len(primal)
    ln_ind = len(intended)
    for i in range(ln_pr - ln_ind + 1):
        if primal[i:i + ln_ind] == intended:
            return primal[0:i] + primal[i + ln_ind:]
    else:
        return primal


name = 'bahram papaki kashani'
print(remove_substr(name, 'ani'))




