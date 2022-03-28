
def func(num):
    if isinstance(num, int) and num >= 0:
        data1 = str(num)[::-1]
        data2 = int(data1)
        return int(data2)
    else:
        raise Exception("非法输入")


print(func(1000))

