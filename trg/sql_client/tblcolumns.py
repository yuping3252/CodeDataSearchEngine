import logging


class TableColumns:
    def __init__(self): 
        self.glo = ""


    def a_query(self, table_, conn_db, glo): 

        tblnm = table_[1]
        cur = conn_db.conn.cursor()

        print("trg.sql_client.tblcolumns.py,    type of database =", conn_db.dbtype)

        if  conn_db.dbtype == "SQL Server": 
            query = "SELECT NAME FROM SYS.COLUMNS WHERE object_id = object_id(\'" + tblnm +"\')"

        elif conn_db.dbtype == "PostgreSQL":
            query = "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = '" + tblnm + "'"

        try: 
            cur.execute(query) 
        except:
            print("tblcolumns.py, tblnm=", tblnm)
            exit()


        data = cur.fetchall() 
        
        columns = []
        for col in data: 
            columns.append(col)
        table_.append(columns)       # table_ = [ tableID, tableNAME, dbID, time, [...columns...] ]
        cur.close()

        return table_


