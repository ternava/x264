
# This script is not used !!!
from itertools import combinations
from options import all_options

input = all_options
# print(input)

# output = sum([list(map(list, combinations(input, i))) for i in range(len(input) + 1)], [])
# print(output)


from random import seed, randrange

seed(None)

def indexed_combination(seq, n):
    result = []
    for u in seq:
        if n & 1:
            result.append(u)
        n >>= 1
        if not n:
            break
    return result

""" print('Testing indexed_combination')
#seq = 'abc'
for i in range(1 << len(input)):
    print(i, ''.join(indexed_combination(input, i)))
print() """

def random_combination(seq):
    n = randrange(1 << len(seq))
    return indexed_combination(seq, n)

print('Testing random_combination')
# seq = 'abcdefghij'
for i in range(50):
    print(i, random_combination(input))