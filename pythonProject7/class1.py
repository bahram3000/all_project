class String_Edit():
    def __init__(self, all_str):
        self.all_str_ = all_str

    def find_in(self, new_str):
        b = 1
        j = 0
        for i in range(len(self.all_str_)):

            if j == len(new_str) and b == 1:
                return bool(b)
            if self.all_str_[i] == new_str[j]:
                j += 1
                b *= 1
            else:
                if j != 0 and j != len(new_str):
                    b *= 0
        return bool(b)

    def find(self, new_str):
        if self.find_in(new_str):
            start = 0
            j = 0

            for i in range(len(self.all_str_)):
                if j == len(new_str):
                    return start, start + j - 1
                if self.all_str_[i] == new_str[j]:
                    if j == 0:
                        start = i
                    j += 1
            end = start + j
            return start, start + j - 1


        else:
            return False

# obj = String_Edit('i am bahram')
# print(obj.find_in('bahi'))
# print(obj.find_in('bah'))
# print(obj.find_in('bahram'))
# print(obj.find_in('ali'))
# print(obj.find_in('am'))
# print(obj.find('bahi'))
# print(obj.find('bah'))
# print(obj.find('bahram'))
# print(obj.find('ali'))
# print(obj.find('am'))
