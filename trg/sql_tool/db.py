
__author__ = 'YupingYang'
import traceback
import logging
import psycopg2
# import pymssql
# import cx_Oracle

class Database:
    def __init__(self, host, port, user, password, dbname, dbtype):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = password      # unenscrypted password
        self.dbname = dbname
        self.dbtype = dbtype
        self.conn   = ""


    def db_connect(self):
        try: 
            if self.dbtype == 'mssql': 
                self.conn = pymssql.connect(host=self.host,user=self.user,password=self.passwd,database=self.dbname,charset='UTF-8')

            elif self.dbtype == 'oracle': 
                self.conn = cx_Oracle.connect(user=self.user,password=self.passwd,dsn=self.host+'/'+self.dbname)

            if self.dbtype == 'postgresql': 
                self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.passwd, database=self.dbname)

            cur = self.conn.cursor()

        except:
            print (traceback.format_exc())
            logging.debug("sql_tool server database connect error.")
            print("sql_tool server database connect error.")
            return
        return cur


    def sqlexec(self, cmds):

        cur = self.db_connect()

        try:
            if cmds.strip().startswith("select"):

                cur.execute(cmds)
                data = cur.fetchall()

                cur.close()
                return data
            else:

                cur.execute(cmds)
                self.conn.commit()

        except Exception(e):
            print (traceback.format_exc())
            logging.debug("sql_tool command exec error,%s",str(e))
            self.conn.rollback()

        finally:
            cur.close()


    def tblcreate_(self,tablename, colnames, coltypes):


        if len(colnames) != len(coltypes):
            return
        collist = []
        collist.append(colnames[0])
        collist.append(", " + coltypes[0])
        i = 1
        for col in colnames[1:]:
            collist.append(", " + col)
            collist.append(" "  + coltypes[i])
            i += 1
        sql = "create table if not exists " + tablename + "(" + ''.join(collist) + ")"
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception(e):
            print (traceback.format_exc())
            logging.debug("create table error, %s",str(e))
            self.conn.rollback()
        finally:
            cur.close()


    def tblinsert(self,tblname,data):   # data= ( , , )
        cur = self.db_connect()
        try:
            cmds = "insert into %s values %s" % (tblname,data)
            cur.execute(cmds)
            self.conn.commit()
        except Exception(e):
            print (traceback.format_exc())
            logging.debug("insert data into table error,%s",str(e))
            self.conn.rollback()
        finally:
            cur.close()


    def tblselect(self,colnames,tblname,cnt=None):  # colname = ( , , )
        cur = self.db_connect()
        try:
            length = len(colnames)
            argnum = '%s,'*length
            if cnt:
                cmds = "select %s from %s where %s"%(argnum[:-1],tblname,cnt)% colnames
            else:
                cmds = "select %s from %s;"%(argnum[:-1],tblname)% colnames
            cur.execute(cmds)
            result = cur.fetchall()
        except Exception(e):
            print (traceback.format_exc())
            logging.debug("select data from database error,%s",str(e))
        finally:
            cur.close()
        return result


    def tbldelete(self,tblname,cnt=None):
        cur = self.db_connect()
        try:
            if cnt:
                cmds = "delete from %s where %s"%(tblname,cnt)
            else:
                cmds = "delete from %s"%tblname
            cur.execute(cmds)
            self.conn.commit()
        except Exception(e):
            print (traceback.format_exc())
            logging.debug("delete data from %s error,%s",(tblname,str(e)))
            self.conn.rollback()
        finally:
            cur.close()


    def tbldrop(self,tblname):
        cur = self.db_connect()
        try:
            cmds = "drop table if exists %s"%tblname
            cur.execute(cmds)
            self.conn.commit()
        except Exception(e):
            print (traceback.format_exc())
            logging.debug("drop table error,%s",str(e))
            self.conn.rollback()
        finally:
            cur.close()


    def maxid(self, idname):
        cur = self.db_connect()
        try:
            cmds = "select idvaluemax from \"TR_MaxID\" where idname=%s"%idname
            cur.execute(cmds)
            result = cur.fetchall()
        except Exception(e):
            print (traceback.format_exec())
            logging.debug("drop table error, %s", str(e))
        finally:
            cur.close()



