from trg.globaldata      import GlobalData
from trg.initialize      import Initialize
from trg.sql_tool.db     import Database


class GlobalSetting:
    def __init__(self, config_info):
        [host, port, username, passwd, dbname, dbtype] = config_info.read_()
        dbsrv = Database(host, port, username, passwd, dbname, dbtype)

        self.glo = GlobalData()
        self.glo.dbserver_.append(dbsrv)
        init = Initialize(self.glo)

        print("")
        print("global_set.py,   Database( host,     port,  username,  passwd,  dbname,   dbtype ) created --> glo.dbserver_")
        print("global_set.py,   Database(", host, port, username, passwd, dbname, dbtype, ")  created --> glo.dbserver_")
        print("")

    def get_glo(self):
        return self.glo

    def write(self, dataInitFlag):
        i = 1
