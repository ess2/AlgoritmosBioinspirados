import math as trunc

a = [1,2,3,4,5,6]

c = 1
d = 6

print a[0:c] + (a[c:d])[::-1] + a[d:len(a)]