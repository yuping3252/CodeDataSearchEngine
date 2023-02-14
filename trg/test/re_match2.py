#!/usr/bin/python
import re

text = "JGood is a handsome boy, he is cool, clever, and so on..."
m = re.match(r"(\w+) is (\w+)\s", text)
if m:
    print m.group(), '\n', m.group(0), '\n', m.group(1), '\n', m.groups()
else:
    print 'not match'