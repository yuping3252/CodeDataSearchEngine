#!/usr/bin/python
import re

text = "JGood is a handsome boy, he is cool, clever, and so on..."
regex = re.compile(r'\w*oo\w*')
print regex.findall(text)
print regex.sub(lambda m: '[' + m.group(0) + ']', text)
m = regex.findall(text)

print "re_compile1, regular   ", m