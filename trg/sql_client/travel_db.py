import os
import datetime
from   trg.globaldata import Tables_TRO
import logging


class TravelDatabase:
    def __init__(self): 
        self.glo = ""


    def travel_db(self, conn_db, glo): 

        print("sql_client,  travel_db.py,   travel_db(), conn_db.dbnm = ", conn_db.dbnm)


        updatetime  = datetime.datetime.now()
        tro = Tables_TRO()
        glo.dbid    = tro.maxid_select('TR_DB',         glo.dbserver_[0]) + 1
        glo.tableid = tro.maxid_select('TR_Table',      glo.dbserver_[0]) + 1
        glo.procid  = tro.maxid_select('TR_StoredProc', glo.dbserver_[0]) + 1

        self.travel_db_tables(updatetime, conn_db, glo)
        self.travel_db_procs (updatetime, conn_db, glo)


    def travel_db_tables(self, updatetime, conn_db, glo):
        query_partial = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='"
        tbl_lst_ = self.db_query(updatetime, conn_db, query_partial, "table", glo)
        glo.db_tbl_lst_.append(tbl_lst_)




    def travel_db_procs(self, updatetime, conn_db, glo):
        query_partial = "SELECT ROUTINE_NAME FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_CATALOG='"
        proc_lst_ = self.db_query(updatetime, conn_db, query_partial, "proc", glo)
        glo.db_proc_lst_.append(proc_lst_)




    def db_query(self, updatetime, conn_db, query_partial, obj_type, glo):

        if   conn_db.dbtype == "SQL Server":  
            query_partial += conn_db.dbnm + "'"
        elif conn_db.dbtype == "PostgreSQL" and obj_type == "table": 
            query_partial += conn_db.dbnm + "' AND TABLE_SCHEMA = 'public'" 
        elif conn_db.dbtype == "PostgreSQL" and obj_type == "proc": 
            query_partial += conn_db.dbnm + "' AND ROUTINE_SCHEMA = 'public'" 
        # -------------------------- completed SQL for Query ---------------------------------

        print("travel_db.py,   db_query(),   query_partial=", query_partial)
        cur = conn_db.conn.cursor() 
        try: 
            cur.execute(query_partial)
            data = cur.fetchall() 
            print("travel_db.py,   ", conn_db.dbtype, ",   ", conn_db.dbserv, ",   ", conn_db.dbnm, ",   connection success")
        except: 
            data = []
            print("travel_db.py,   ", conn_db.dbtype, ",   ", conn_db.dbserv, ",   ", conn_db.dbnm, ",   connection failed")
        print("")

        # -------------------------- executed Query ---------------------------------

        obj_lst_ = []
        for row in data: 
            if obj_type == "table": 
                obj_ = [ glo.tableid, row[0], glo.dbid, updatetime]      # [ table ID,  table NAME,  db ID,  time ]
                obj_lst_.append(obj_)
                glo.tableid += 1
            else:
                obj_ = [ glo.procid,  row[0], glo.dbid, updatetime]      # [ proc ID,    proc NAME,  db ID,  time ]
                obj_lst_.append(obj_)
                glo.procid  += 1
        cur.close()

        return obj_lst_


