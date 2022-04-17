'''
 The script demonstrate usage of Python generators,
 to calculate a factorial
 (in the function fact_gen with the keyword yield)
'''
# Code block
def prod(a,b):
    output = a*b
    return output

def fact_gen():
    i = 1
    n = i
    
    while True:
        output = prod(n, i)
        i = i + 1
        n = output
        yield output


# Test block
my_gen = fact_gen()
num = 5 # number for which factorial should be calculated
for i in range(num):
    print(next(my_gen))

# Correct result when num = 5:
# 1
# 2
# 6
# 24
# 120


