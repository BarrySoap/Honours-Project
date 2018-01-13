# 3_5 #
from pprint import pprint as p_print
from copy import copy, deepcopy

nums_2d = [
    [1, 2, 3, 4, 5, 6, 7],
    [8, 9, 10, 11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20, 21, 22]
]

nums_2d[2][1] = -5
p_print(nums_2d)

letters = ["A", "B", "C", "D", "E", "F"]
letters_2d = [copy(letters), copy(letters), copy(letters)]
letters_2d[0][0] = "F"
p_print(letters_2d)

# 3_6 #

a = list(range(0, 10))
print(a[0:len(a)])
print(a[::2])

print(a[0:6:2])
print(a[0:6:3])

print(a[::-1])