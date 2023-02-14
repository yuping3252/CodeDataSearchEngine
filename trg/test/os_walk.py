#! usr/bin/python
import os


for root, dirs, files in os.walk(".", topdown=False):

    print ("root  ", root)
    print ""

    for name in dirs:
        print("dir   ", os.path.join(root, name))

    print ""

    for name in files:
        print("file  ", os.path.join(root, name))


    print ""
    print ""
    print ""