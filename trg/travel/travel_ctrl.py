import os
import gc
import multiprocessing as mp
from multiprocessing import Process, Pipe

from trg.travel.travel_dir    import TravelDir
from trg.sql_tool.trtblcreate import trtblcreate_


def travel_ctrl_(path_, glo):

    trtblcreate_(glo.dbserver_[0])                      # create all db Tables that our system will use
    if path_.endswith('/'):                             # for given path_, return it or,
        path_ = path_[:len(path_)-1]                    # if file, return its parent dir without "/"

    if os.path.isfile(path_):
        try:
            path_ = path_[:path_.rindex('/')]
        except ValueError:
            path_ = path_[:path_.rindex('\\')]
            return False

    if os.path.exists(path_):
        obj = TravelDir()
        obj.travel_dir_(path_, glo)

#        obj = TravelDir()
#        parent_conn, child_conn = Pipe()
#        p = mp.Process(target=obj.travel_dir_, args=(child_conn, path_, glo))
#        p.start()
#        p.join()
        return True
    else:
        return False
