import logging


class StoredProc:
    def __init__(self): 
        self.glo = ""


    def a_query(self, proc_, conn_db, glo): 

        procnm = proc_[1]
        cur = conn_db.conn.cursor()

        if  conn_db.dbtype == "SQL Server": 
            query = "SELECT ROUTINE_DEFINITION FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME = \'" + procnm + "\'"

        # PostgreSQL part is wrong
        elif conn_db.dbtype == "PostgreSQL":
            query = "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = '" + tblnm + "'"

        cur.execute(query) 
        data = cur.fetchall() 
        
        routine = []
        for def_ in data:
            routine.append(def_)

        proc_.append(routine)       # proc_ = [ procID, procNAME, dbID, time, routine_definition ]
        cur.close()

        return proc_


