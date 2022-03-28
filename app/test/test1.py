"""
倒序输出
1000 ---> 1
1010 ---> 101
1234 ---> 4321

进阶： 输入负数
"""


def ReverseNum(num):
    if num == 0:
        return 0

    index = 0
    temp = list(str(num))
    reverse_num = temp[::-1]
    if num > 0:
        while index < len(reverse_num):
            if reverse_num[index] == "0":
                reverse_num.pop(index)
            else:
                break
        return int("".join(reverse_num))

    if num < 0:
        while index < len(reverse_num) - 1:
            if reverse_num[index] == "0":
                reverse_num.pop(index)
            else:
                break
        temp = reverse_num[:-1]
        return 0 - int("".join(temp))


print(ReverseNum(1234))