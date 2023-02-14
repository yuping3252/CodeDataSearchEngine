__author__ = 'Administrator'
from trg.cmd.global_set import global_setting_


def test_data_store_db_(tblname, listtobe):
    glo = global_setting_()
    for rowvalues in listtobe:
        if len(rowvalues)==3:
            insert_stmt_quoted = "insert into %s" % tblname + " values ('%s','%s','%s')" % rowvalues
        elif len(rowvalues)==5:
            insert_stmt_quoted = "insert into %s" % tblname + " values ('%s','%s','%s', '%s', '%s')" % rowvalues
        glo.dbserver_[0].sqlexec(insert_stmt_quoted)

def test_data_lists_():
    tblname = "test_t1"
    listtobe = [ \
        ('a1111', 'a1212', 'a1313'), ('a1121', 'a1222', 'a1323'), ('a1131', 'a1232', 'a1333'),\
        ('a1141', 'a1242', 'a1343'), ('a1151', 'a1252', 'a1353'), ('a1161', 'a1262', 'a1363'),\
        ('a1171', 'a1272', 'a1373'), ('a1181', 'a1282', 'a1383'), ('a1191', 'a1292', 'a1393') \
        ]
    test_data_store_db_(tblname, listtobe)

    tblname = "test_t2"
    listtobe = [ \
        ('a2111', 'a2212', 'a1111'), ('a2121', 'a2222', 'a1141'), ('a2131', 'a2232', 'a1171'),\
        ('a2141', 'a2242', 'a1121'), ('a2151', 'a2252', 'a1151'), ('a2161', 'a2262', 'a1181'),\
        ('a2171', 'a2272', 'a1131'), ('a2181', 'a2282', 'a1161'), ('a2191', 'a2292', 'a1191') \
        ]
    test_data_store_db_(tblname, listtobe)

    tblname = "test_t3"
    listtobe = [ \
        ('a3111', 'a3212', 'a2111'), ('a3121', 'a3222', 'a2141'), ('a3131', 'a3232', 'a2171'),\
        ('a3141', 'a3242', 'a2121'), ('a3151', 'a3252', 'a2151'), ('a3161', 'a3262', 'a2181'),\
        ('a3171', 'a3272', 'a2131'), ('a3181', 'a3282', 'a2161'), ('a3191', 'a3292', 'a2191') \
        ]
    test_data_store_db_(tblname, listtobe)

    tblname = "test_t4"
    listtobe = [ \
        ('a4111', 'a4212', 'a2111'), ('a4121', 'a4222', 'a2141'), ('a4131', 'a4232', 'a2171'),\
        ('a4141', 'a4242', 'a2121'), ('a4151', 'a4252', 'a2151'), ('a4161', 'a4262', 'a2181'),\
        ('a4171', 'a4272', 'a2131'), ('a4181', 'a4282', 'a2161'), ('a4191', 'a4292', 'a2191') \
        ]
    test_data_store_db_(tblname, listtobe)

    tblname = "test_t5"
    listtobe = [ \
        ('a5111', 'a5112', 'a4111', 'a5113', 'a5114'), ('a5121', 'a5122', 'a4141', 'a5123', 'a5124'),\
        ('a5131', 'a5232', 'a4171', 'a5133', 'a5134'), ('a5141', 'a5142', 'a4121', 'a5143', 'a5144'),\
        ('a5151', 'a5152', 'a4151', 'a5153', 'a5154'), ('a5161', 'a5162', 'a4181', 'a5163', 'a5164'),\
        ('a5171', 'a5172', 'a4131', 'a5173', 'a5174'), ('a5181', 'a5182', 'a4161', 'a5183', 'a5184'),\
        ('a5191', 'a5192', 'a4191', 'a5193', 'a5194')\
        ]
    test_data_store_db_(tblname, listtobe)

    tblname = "test_t6"
    listtobe = [ \
        ('a6111', 'a6212', 'a5111'), ('a6121', 'a6222', 'a5141'), ('a6131', 'a6232', 'a5171'),\
        ('a6141', 'a6242', 'a5121'), ('a6151', 'a6252', 'a5151'), ('a6161', 'a6262', 'a5181'),\
        ('a6171', 'a6272', 'a5131'), ('a6181', 'a6282', 'a5161'), ('a6191', 'a6292', 'a5191') \
        ]
    test_data_store_db_(tblname, listtobe)

    tblname = "test_t7"
    listtobe = [ \
        ('a7111', 'a7212', 'a3111'), ('a7121', 'a7222', 'a3141'), ('a6131', 'a6232', 'a3171'),\
        ('a7141', 'a7242', 'a3121'), ('a7151', 'a7252', 'a3151'), ('a6161', 'a6262', 'a3181'),\
        ('a7171', 'a7272', 'a3131'), ('a7181', 'a7282', 'a3161'), ('a6191', 'a6292', 'a3191') \
        ]
    test_data_store_db_(tblname, listtobe)

    tblname = "test_t8"
    listtobe = [ \
        ('a8111', 'a8212', 'a8111'), ('a8121', 'a8222', 'a8141'), ('a8131', 'a8232', 'a8171'),\
        ('a8141', 'a8242', 'a8121'), ('a8151', 'a8252', 'a8151'), ('a8161', 'a8262', 'a8181'),\
        ('a8171', 'a8272', 'a8131'), ('a8181', 'a8282', 'a8161'), ('a8191', 'a8292', 'a8191') \
        ]
    test_data_store_db_(tblname, listtobe)

    tblname = "test_t9"
    listtobe = [ \
        ('a9111', 'a9212', 'a9111'), ('a9121', 'a9222', 'a9141'), ('a9131', 'a9232', 'a9171'),\
        ('a9141', 'a9242', 'a9121'), ('a9151', 'a9252', 'a9151'), ('a9161', 'a9262', 'a9181'),\
        ('a9171', 'a9272', 'a9131'), ('a9181', 'a9282', 'a9161'), ('a9191', 'a9292', 'a9191') \
        ]
    test_data_store_db_(tblname, listtobe)

    tblname = "test_t10"
    listtobe = [ \
        ('a10111', 'a10212', 'a9111'), ('a10121', 'a10222', 'a9121'), ('a10131', 'a10232', 'a9131'),\
        ('a10141', 'a10242', 'a9242'), ('a10151', 'a10252', 'a9252'), ('a10161', 'a10262', 'a9262'),\
        ('a10171', 'a10272', 'a9131'), ('a10181', 'a10282', 'a9161'), ('a10191', 'a10292', 'a9191') \
        ]
    test_data_store_db_(tblname, listtobe)


def test_data_truncate_db_():
    tables = ['test_t1', 'test_t2', 'test_t3', 'test_t4', 'test_t5',\
              'test_t6', 'test_t7', 'test_t8', 'test_t9', 'test_t10']
    glo = global_setting_()
    for table in tables:
        insert_stmt_quoted = "truncate table %s" % table
        glo.dbserver_[0].sqlexec(insert_stmt_quoted)

if __name__=='__main__':
    test_data_truncate_db_()
    test_data_lists_()

