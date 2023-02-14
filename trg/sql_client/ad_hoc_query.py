import logging


class ADHOC_QUERY:
    def __init__(self): 
        self.glo = ""


    def a_query(self, query, conn_db): 
        data = ""
        col_lst = []
        if type(conn_db) != type(""):
            cur = conn_db.conn.cursor()

            try: 
                query1 = query.strip()
                if query1[len(query1)-1] == '\\':
                    query2 = query1[:len(query1)-1]
                else:
                    query2 = query1
                cur.execute(query2) 
            except:
                print("ad_hoc_query.py, query=", query, " failed")

            data = cur.fetchall() 
            cur.close()

        return data


