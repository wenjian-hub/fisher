
a = {
    "1": 1,
    "2": 2,
    "3": 3
}


b = {
    "2": 2,
    "3": 3,
    "4": 4
}

print(a.items() & b.items())