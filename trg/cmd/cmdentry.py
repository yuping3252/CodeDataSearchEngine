import logging

def cmdentry_():
    operate = 't'

    if operate == 't':
        try:
            # path_ = raw_input("Type in the path we will travel: ")
            path_ = "D:/tr7/tr103"
        except:
            # path_ = input("Type in the path we will travel: ")
            path_ = "D:/tr7/tr103"
        path_ = path_.strip()
        return operate, path_
    elif operate == 's':
        try:
            cond_ = raw_input("Type in search condition: ")
        except:
            cond_ = input("Type in search condition: ")
        cond_ = cond_.strip()
        logging.debug("search condition=%s", cond_)
        return operate, cond_
    elif operate == 'a':
        return operate, True
    elif operate == 'r':
        return operate, True
    else:
        print("Sorry,Input again!")
        return None
