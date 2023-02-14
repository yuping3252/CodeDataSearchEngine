import logging
from   trg.globaldata     import Tables_TR

class Initialize:
    def __init__(self, glo):
        sqlhub = Tables_TR()

        print("trgui322/trg/initialize.py    sqlhub.tr_sqlquerytrace=", sqlhub.tr_sqlquerytrace) 

        cds = glo.dbserver_[0].sqlexec(sqlhub.tr_sqlquerytrace)
        cds = glo.dbserver_[0].sqlexec(sqlhub.tr_sqlqueryfilter)
        cds = glo.dbserver_[0].sqlexec(sqlhub.tr_sqlquerysrctables)
        cds = glo.dbserver_[0].sqlexec(sqlhub.tr_sqlqueryselcols)
        cds = glo.dbserver_[0].sqlexec(sqlhub.tr_sqlinsertselcols)
        cds = glo.dbserver_[0].sqlexec(sqlhub.tr_sql)

