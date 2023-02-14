import os
import logging
__author__ = 'YupingYang'


def searchctrl_(cnt,globaldata):
    if os.path.isfile(cnt):
        result = s_dflow_file(cnt)
        print (result)
    else:
        logging.debug("this is not will be exec")
        pass # will be add function.
