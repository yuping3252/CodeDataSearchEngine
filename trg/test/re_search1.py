#!/usr/bin/python
import re

line = "Cats are smarter than dogs       Cats are smarter than dogs";

searchObj = re.search( r'(.*) are (.*?) .*', line, re.M|re.I)

if searchObj:
   print "searchObj.group()  : ", searchObj.group()
   print "searchObj.group(1) : ", searchObj.group(1)
   print "searchObj.group(2) : ", searchObj.group(2)
   print "searchObj.groups() : ", searchObj.groups()
else:
   print "Nothing found!!"

#   Python offers two different primitive operations based on regular expressions:
#   match checks for a match only at the beginning of the string, while
#   search checks for a match anywhere in the string (this is what Perl does by default).