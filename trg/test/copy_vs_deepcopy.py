__author__ = 'Administrator'
import copy
a = [1, 2, 3, 4, ['a', 'b']]  # original object

b = a                 # assign container handle, b just another name of a
c = copy.copy(a)      # shallow copy, just copy the container, not base element
d = copy.deepcopy(a)  # deep copy, copy everything

a.append(5)           # change outside original a, i.e., outside c, so c unchanged
a[4].append('c')     #  change inside original a, i.e., inside c, so c changed

print 'a = ', a
print 'b = ', b
print 'c = ', c
print 'd = ', d