#!/usr/bin/python

print "\n"

f = open('test28_sql.sql')
lines = f.read()
sql = ""
new_c = ""
for c in lines:
    new_c = c
    if c == "\n":
        new_c = " "
    sql += new_c
print ".... original lines=...\n", lines
print ""
print ".... merged   lines=...\n", sql
f.close()



