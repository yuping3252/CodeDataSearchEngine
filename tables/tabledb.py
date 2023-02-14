import traceback
import pymssql
import psycopg2
from PyQt4.QtCore import *
from PyQt4.QtGui  import *


class TableDB:
    def __init__(self, host, port, user, password, dbname, dbtype):
        self.host   = host
        self.port   = port
        self.user   = user
        self.passwd = password      # unenscrypted password
        self.dbname = dbname
        self.dbtype = dbtype

        print("host=", host)
        print("port=", port)
        print("user=", user)
        print("password=", password)
        print("dbname=", dbname)
        print("dbtype=", dbtype)

        try:
            if self.dbtype == 'postgresql':
                self.conn = psycopg2.connect(host=self.host, port=self.port, \
                                             user=self.user, password=self.passwd, database=self.dbname)
            elif self.dbtype == 'mssql': 
                self.conn = pymssql.connect(host=self.host,user=self.user,password=self.passwd,database=self.dbname,charset='UTF8')
            self.cur = self.conn.cursor()

            if not self.cur:
                raise(NameError, "connect to database failed")

        except Exception(e):
            print (traceback.format_exc())
            logging.debug("sql_tool server database connect error.%s",str(e))


    def execproc(self, cmds, list1):
        try:
            self.cur.callproc(cmds, list1)
            self.conn.commit()

        except Exception(e):
            print(traceback.format_exec())
            logging.debug("sql_tool command exec error,%s", str(e))


    def execsql(self, cmds):
        try:
            if cmds.strip().startswith("select"):
                self.cur.execute(cmds)
                data = self.cur.fetchall()
                lst = []
                for row in data:
                    lst.append(row)
                rows = self.cur.rowcount

                return lst, rows

        except Exception(e):
            print(traceback.format_exec())
            logging.debug("sql_tool command exec error,%s", str(e))

