import traceback
import pymssql
import psycopg2

from PyQt4.QtCore import *
from PyQt4.QtGui  import *



class TableRelate:
    def __init__(self, db, sz):
        self.db = db
        self.sz = sz

    def related_value_tmp_info(self):                    # from tr_value_tmp_info table, not used for now
        stmt = "select * from dbo.tr_value_tmp_info"
        value_info, rows_ = self.db.execsql(stmt)
        return value_info


    def get_related_tables(self, params):
        stmt  = "dbo.tr_related_value_search7"
        self.db.execproc(stmt, params)

        stmt = "select * from dbo.tr_value_tmp_info"
        tmp_info, rows = self.db.execsql(stmt)

        tbl_lst = []
        for tmp_row in tmp_info:
            tbl_lst.append(tmp_row[1])
            # tbl_lst.append(tmp_row[0] + '.dbo.' + tmp_row[1])
        return tbl_lst


    def get_relat_tbl_all_vals(self, params):
        stmt  = "dbo.tr_related_value_search7"
        self.db.execproc(stmt, params)
        tbl_lst = self.get_related_tables(params)
        stmt = "select * from dbo.tr_value_tmp_info"
        info_rows, rownum = self.db.execsql(stmt)

        row_lst = []
        col_lst = []
        for rows in info_rows:
            if rows[8] == -1: 
                if len(info_rows) == 1: 
                    #one_tbl_rows, one_tbl_cols = self.get_one_tbl_rows(db, params)
                    break
                continue
            stmt_sel_tmp = "select " + rows[3] + " from " + rows[0] + ".dbo." + rows[1]

            data, rownum1 = self.db.execsql(stmt_sel_tmp) 

            tbl_rows = []
            rows_ = self.sz.dsply_rows_index(data)

            for row in rows_:
                tbl_rows.append(row)
            row_lst.append(tbl_rows)

            col_lst = rows[3].split(',')
            col_lst.append(col_lst)

        if len(info_rows) == 1:
            col_lst = [one_tbl_cols]
            row_lst = [one_tbl_rows]
        row_max, col_max, row_max_lst, col_cnt_lst = self.sz.compute_screen_rowcols(row_lst, col_lst)
        return row_max, col_max, tbl_lst, row_lst, col_lst 


    def get_relat_tbl_relat_vals(self, params):

        stmt  = "dbo.tr_related_value_search8"
        success = self.db.execproc(stmt, params)

        if not success:
            return 0, 0, [], [[]], []
        tbl_lst = self.get_related_tables(params)

        new_tbl_lst            = []
        new_info_rows          = []
        new_info_rows_tmp_tbls = []

        stmt = "select * from dbo.tr_value_tmp_info"
        info_rows, rownum = self.db.execsql(stmt)

        t = 0
        for row_ in info_rows:
            if  new_info_rows_tmp_tbls.count(row_[2]) == 0:
                new_tbl_lst.append(row_[1])
                new_info_rows.append(row_)
                new_info_rows_tmp_tbls.append(row_[2])
            t += 1

        row_lst = []
        col_lst = []
        one_tbl_cols = []
        one_tbl_rows = []
        
        t = 0
        new1_tbl_lst = []
        for rows in new_info_rows: 
            if rows[8] == -1: 
                if len(new_info_rows) == 1: 
                    # one_tbl_rows, one_tbl_cols = self.get_one_tbl_rows(db, params)
                    break
                t += 1
                continue
            new1_tbl_lst.append(new_tbl_lst[t])
            t += 1

            stmt_sel_tmp = "select distinct " + rows[3] + "," + rows[4] + "_pk1," + rows[6] + "_pk2,chain from "  \
                           + rows[0] + ".dbo." + rows[2]
            #stmt_sel_tmp = "select distinct " + rows[3] + " from " + rows[0] + ".dbo." + rows[2]


            print("tablerelate.py,   get_relat_tbl_relat_vals(),   stmt_sel_tmp=", stmt_sel_tmp)

            data, rownum1 = self.db.execsql(stmt_sel_tmp) 

            tbl_rows = []
            rows_ = self.sz.dsply_rows_index(data)
            for row in rows_:
                # print("tablerelate.py,   get_relat_tbl_relat_vals(),  row=", row)
                tbl_rows.append(row)
            row_lst.append(tbl_rows)

            collist_ = rows[3].split(',')
            col_lst.append(collist_)

            print("")

        print("")

        if len(info_rows) == 1:
            col_lst = [one_tbl_cols]
            row_lst = [one_tbl_rows]

        row_max, col_max, row_max_lst, col_cnt_lst = self.sz.compute_screen_rowcols(row_lst, col_lst)
        return row_max, col_max, new1_tbl_lst, row_lst, col_lst 


    def get_relat_val_tmp_tbls_rows_pk2_(self, params):
        stmt  = "dbo.tr_related_value_search7"
        self.db.execproc(stmt, params)
        tbl_lst = self.get_related_tables(params)

        stmt = "select * from dbo.tr_value_tmp_info"
        info_relat_tbl, tbl_cnt = self.db.execsql(stmt)

        row_lst = []
        col_lst = []
        
        for info_val_tmp_tbl in info_relat_tbl:
            if info_val_tmp_tbl[8] == -1: 
                continue
            pk2_ = info_val_tmp_tbl[6]
            collist = info_val_tmp_tbl[3]
            val_tmp_tbl = info_val_tmp_tbl[2]
            stmt_sel_val_tmp = "select " + pk2_ + "_pk2, " + collist + " from dbo." + val_tmp_tbl
            data, rownum1 = self.db.execsql(stmt_sel_val_tmp) 

            tbl_rows = self.sz.dsply_rows_index(data)
            row_lst.append(tbl_rows)

            collist_ = [pk2_+"_pk2"] + collist.split(',')
            col_lst.append(collist_)
        row_max, col_max, row_max_lst, col_cnt_lst = self.sz.compute_screen_rowcols(row_lst, col_lst)
        return row_max, col_max, tbl_lst, row_lst, col_lst 


    def get_relat_val_tmp_tbls_rows(self, params):
        stmt  = "dbo.tr_related_value_search7"
        self.db.execproc(stmt, params)
        tbl_lst = self.get_related_tables(params)

        stmt = "select * from dbo.tr_value_tmp_info"
        info_relat_tbl, tbl_cnt = self.db.execsql(stmt)
        row_lst = []
        col_lst = []
        
        for info_val_tmp_tbl in info_relat_tbl:
            pk2_        = info_val_tmp_tbl[6]
            collist     = info_val_tmp_tbl[3]
            val_tmp_tbl = info_val_tmp_tbl[2]

            if info_val_tmp_tbl[8] == -1: 
                stmt_sel_val_tmp = "select " + pk2_ + ", "     + collist + " from dbo." + val_tmp_tbl
            else:
                stmt_sel_val_tmp = "select " + pk2_ + "_pk2, " + collist + " from dbo." + val_tmp_tbl

            data, rownum1 = self.db.execsql(stmt_sel_val_tmp) 
            tbl_rows      = self.sz.dsply_rows_index(data)
            row_lst.append(tbl_rows)
            collist_      = collist.split(',')
            col_lst.append(collist_)

        row_max, col_max, row_max_lst, col_cnt_lst = self.sz.compute_screen_rowcols(row_lst, col_lst)
        return row_max, col_max, tbl_lst, row_lst, col_lst








