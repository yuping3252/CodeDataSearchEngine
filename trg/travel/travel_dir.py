import os
from datetime                       import datetime
from threading import Thread

from tree.nodelist2treefile import NodeList2TreeFile
from trg.globaldata                 import Tables_TRO
from trg.sql_decom.a_file_sqldecoms import SqlDecom
from trg.sql_tool.data_store        import data_store_db_
from trg.tool.filesuffix            import FileSuffix
from trg.tool.read_file_all_types   import read_file_all_types


class TravelDir:
    def __init__(self):
        self.filelist = []
        self.sqllist  = []
        self.glo = ""

    def travel_dir_(self, path_, glo):                     # here, path_ is a path, not file
        tro  = Tables_TRO()
        # initially, nodeid = -1. Later nodeid will be based on the maximum nodeid in the database table
        glo.nodeid   = tro.maxid_select('TR_Node', glo.dbserver_[0]) + 1
        glo.fileid   = tro.maxid_select('TR_File', glo.dbserver_[0]) + 1
        glo.sql_id   = tro.maxid_select('TR_SQL',  glo.dbserver_[0]) + 1
        glo.serverid = 0

        ip       = "0.0.0.0"
        port     = 1521
        filesuffix   = FileSuffix()
        t1 = Thread(target=self.build_nodelist, args=(ip, port, filesuffix, path_, glo))
        t1.start()
        t1.join()
        t2 = Thread(target=self.build_sqllist, args=(self.filelist, self.glo))
        t2.start()
        t2.join()

        self.glo.nodeid   = tro.maxid_insert('nodeid', 'TR_Node', self.glo.dbserver_[0])
        self.glo.fileid   = tro.maxid_insert('fileid', 'TR_File', self.glo.dbserver_[0])
        self.glo.sql_id   = tro.maxid_insert('sqlid',  'TR_SQL',  self.glo.dbserver_[0])

    def build_nodelist(self, ip, port, filesuffix, path_, glo):
        # ------------------------ create nodelist  ----------------------------
        nodelist = []
        for parent, dirnames, filenames in os.walk(path_):
            # ------------------------ The first time ----------------------------
            if not nodelist:
                updatetime  = datetime.fromtimestamp(os.path.getmtime(parent)).strftime("%Y-%m-%d %H:%M:%S")
                msg = "a directory"
                file_ = [glo.fileid, glo.serverid, ip, port, 'dir', 'type', parent, parent, parent, msg, updatetime]
                node_ = [glo.nodeid, glo.nodeid, 'root', 'dir', glo.fileid, file_, updatetime]
                self.filelist.append(file_)
                nodelist.append(node_)
                glo.fileid += 1
                glo.nodeid += 1
            # --------------------------- node_pid ------------------------------
            node_pid = 0
            for node_ in nodelist:
                file_ = node_[5]
                if file_[4] == "dir":
                    filepath = file_[6]
                    if parent == filepath:
                        node_pid = node_[0]  # if a dir's filepath is parent dir, node_pid = id of this node
                        break
            # ------------------------ directories under current parent ----------------------------
            for dir in dirnames:
                if dir == '.' or dir == '..':
                    continue
                fullpath = os.path.join(parent, dir)
                updatetime = datetime.fromtimestamp(os.path.getmtime(fullpath)).strftime("%Y-%m-%d %H:%M:%S")
                msg = "a directory"
                file_ = [glo.fileid, glo.serverid, ip, port, 'dir', 'type', fullpath, dir, dir, msg, updatetime]
                node_ = [glo.nodeid, node_pid, "dir", 'dir', glo.fileid, file_, updatetime]
                self.filelist.append(file_)
                nodelist.append(node_)
                glo.fileid += 1
                glo.nodeid += 1
            # ------------------------ files under current parent ----------------------------
            for filenm in filenames:
                if filesuffix.filesuffix_(filenm)=='pyc' or filenm[0] == '.':
                    continue
                fullpath = os.path.join(parent, filenm)
                updatetime = datetime.fromtimestamp(os.path.getmtime(fullpath)).strftime("%Y-%m-%d %H:%M:%S")
                filecontent  = read_file_all_types(fullpath)                        # read this file --> content
                if not filecontent:
                    filecontent = ''
                suffix = filesuffix.filesuffix_(filenm)
                if not suffix == 'sql':
                    filecontent = ''
                msg = "a file"
                file_ = [glo.fileid, glo.serverid, ip, port, "file", suffix, fullpath, filenm, filecontent, msg, updatetime]
                node_ = [glo.nodeid, node_pid, "dir", 'file', glo.fileid, file_, updatetime]
                #                               parent  self    stuff id    stuff content
                self.filelist.append(file_)
                nodelist.append(node_)
                glo.fileid += 1
                glo.nodeid += 1
        nodetreefile = NodeList2TreeFile()
        nodetreefile.nodelist2treefile_(nodelist)
        for node in nodelist:
            node[5] = node[5][7]
        data_store_db_("public.TR_Node", nodelist, glo)
        self.glo = glo


    def build_sqllist(self, filelist, glo):
        updatetime = datetime.now()
        # ------------------------ decompose SQL files ----------------------------
        sqllist   = []
        for file_ in filelist:
            suffix = file_[5]
            if suffix == 'sql':

                glo.fileid   = file_[0]
                sqlcontent   = file_[8]
                sqlobj       = SqlDecom()                # SQL decomposition root


                print("travel_dir.py,   build_sqllist(), file_[7]=", file_[7])

                sql_decom_list = sqlobj.a_file_sqldecoms_(sqlcontent, glo)

                print("")
                print("")

                if sql_decom_list:
                    if type(sql_decom_list) == type([]):
                        sqllist.extend(sql_decom_list)
                    elif type(sql_decom_list) == type("xxx"):
                        file_[9] = str(sql_decom_list)
        data_store_db_("public.TR_File", filelist, glo)
        data_store_db_("public.TR_SQL",  sqllist,  glo)



