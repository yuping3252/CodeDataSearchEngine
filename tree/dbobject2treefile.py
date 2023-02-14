import sys
import os


class DBObject2TreeFile:
    def __init__(self):
        sys.setrecursionlimit(6000)
        self.nodelist  = []
        self.dots      = "                                                                                                                 "


    def table2treefile(self, glo): 
        self.glo = glo
        treeTableFile = os.getcwd() + '\\tmp_files\\tree_dbtable.txt'
        f = open(treeTableFile, 'w', encoding='utf-8')
        f.truncate()
        f.close()

        d = 0
        for tbl_lst in glo.db_tbl_lst_:     # a list of tables for each database connection
            dbnm = glo.dbconn_[d].dbnm
            dbnm    = glo.dbconn_[d].dbnm
            #tbl_lst = db[1]
            table_lst  = []
            for tbl_ in tbl_lst: 
                table_lst.append([tbl_[0], tbl_[1], tbl_[4]])     # each element = [ tableID, tableNAME, [......]  ]
            self.treefileprint_(dbnm, table_lst, treeTableFile, "table")
            d += 1


    def proc2treefile(self, glo): 
        self.glo = glo
        treeProcFile = os.getcwd() + '\\tmp_files\\tree_dbproc.txt'
        f = open(treeProcFile, 'w', encoding='utf-8')
        f.truncate()
        f.close()

        d = 0
        for prc_lst in glo.db_proc_lst_:     # a list of tables for each database connection
            dbnm = glo.dbconn_[d].dbnm
            dbnm    = glo.dbconn_[d].dbnm
            proc_lst  = []
            for prc_ in prc_lst: 
                proc_lst.append([prc_[0], prc_[1]])     # each element = [ procID, procNAME, procContent  ]
            self.treefileprint_(dbnm, proc_lst, treeProcFile, "proc")
            d += 1


    def treefileprint_(self, dbnm, obj_lst, treeFile, treeType):
        f = open(treeFile, 'a', encoding='utf-8')
        col_cnt = 100
        f.write(self.dots[:19] + "1D:\\" + dbnm + "\n")
        for obj in obj_lst:
            obj_string = self.dots[:20 - len(str(obj[0]))] + str(obj[0]) + "    \\" + obj[1] + "\n"
            f.write(obj_string)
            if treeType == "table": 
                for column in obj[2]:
                    column_string = self.dots[:20 - len(str(col_cnt))] + str(col_cnt) + "      \\" + column[0]  + "\n"
                    f.write(column_string)
                    col_cnt += 1
        f.close()
