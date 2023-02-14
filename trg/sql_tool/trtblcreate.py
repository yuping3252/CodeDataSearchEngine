

from trg.globaldata import GlobalData, \
    Tables_TRO,   \
    Tables_TR,    \
    Tables_TRC,   \
    Tables_TRR,   \
    Tables_TRSQL, \
    Tables_TRSR,  \
    Tables_TRS,   \
    Tables_TRT,   \
    Tbls_db_sql,  \
    Tbls_node_sql,\
    Tbls_sql_sql, \
    Tbls_sqlvstable_sql,\
    Tbl_search_sql

def trtblcreate_(dbsrv):
    #descriptrion: create all tr tables if not already created
    tblcreate_cmds = []

# -------------------------------- new tables ---------------------------------
    tables_tro = Tables_TRO()
    tblcreate_cmds.append(tables_tro.tro_maxid)

    tables_tr  = Tables_TR()
    tblcreate_cmds.append(tables_tr.tr_node)
    tblcreate_cmds.append(tables_tr.tr_column)
    tblcreate_cmds.append(tables_tr.tr_db)
    tblcreate_cmds.append(tables_tr.tr_dbcross)
    tblcreate_cmds.append(tables_tr.tr_file)
    tblcreate_cmds.append(tables_tr.tr_server)
    tblcreate_cmds.append(tables_tr.tr_smallcolumn)
    tblcreate_cmds.append(tables_tr.tr_sqltablecross)
    tblcreate_cmds.append(tables_tr.tr_storedproc)
    tblcreate_cmds.append(tables_tr.tr_table)
    tblcreate_cmds.append(tables_tr.tr_treecolumns)
    tblcreate_cmds.append(tables_tr.tr_treefiles)
    tblcreate_cmds.append(tables_tr.tr_treetables)

    tables_trc = Tables_TRC()
    tblcreate_cmds.append(tables_trc.trc_case)
    tblcreate_cmds.append(tables_trc.trc_casesearchcross)
    tblcreate_cmds.append(tables_trc.trc_display)
    tblcreate_cmds.append(tables_trc.trc_displaycasecross)
    tblcreate_cmds.append(tables_trc.trc_nodedisplaycoordinate)
    tblcreate_cmds.append(tables_trc.trc_searchnodecross)

    tables_trr = Tables_TRR()
    tblcreate_cmds.append(tables_trr.trr_filedataflow)
    tblcreate_cmds.append(tables_trr.trr_filefile)

    tables_trsql = Tables_TRSQL()
    tblcreate_cmds.append(tables_trsql.trsql_block)
    tblcreate_cmds.append(tables_trsql.trsql_blockhost)
    tblcreate_cmds.append(tables_trsql.trsql_blockcolumn)

    tables_trsr = Tables_TRSR()
    tblcreate_cmds.append(tables_trsr.trsr_chain)
    tblcreate_cmds.append(tables_trsr.trsr_pickupnodecross)
    tblcreate_cmds.append(tables_trsr.trsr_result)
    tblcreate_cmds.append(tables_trsr.trsr_resultnodelist)
    tblcreate_cmds.append(tables_trsr.trsr_searchchaincross)

    tables_trs = Tables_TRS()
    tblcreate_cmds.append(tables_trs.trs_condcross)
    tblcreate_cmds.append(tables_trs.trs_condition)
    tblcreate_cmds.append(tables_trs.trs_searchhead)
    tblcreate_cmds.append(tables_trs.trs_startitem)

    tables_trt = Tables_TRT()
    tblcreate_cmds.append(tables_trt.trt_categoryassoc)
    tblcreate_cmds.append(tables_trt.trt_categorycommon)
    tblcreate_cmds.append(tables_trt.trt_categorycommonhistory)
    tblcreate_cmds.append(tables_trt.trt_categorytech)
    tblcreate_cmds.append(tables_trt.trt_categorytechhistory)
    tblcreate_cmds.append(tables_trt.trt_commonterm)
    tblcreate_cmds.append(tables_trt.trt_commontermassoc)
    tblcreate_cmds.append(tables_trt.trt_owner)
    tblcreate_cmds.append(tables_trt.trt_techterm)

# -------------------------------- old tables ---------------------------------
    db_sql = Tbls_db_sql()

    tblcreate_cmds.append(db_sql.db_table)
    tblcreate_cmds.append(db_sql.table_table)
    tblcreate_cmds.append(db_sql.column_table)
    tblcreate_cmds.append(db_sql.tablerelate_table)

    node_sql = Tbls_node_sql()

    tblcreate_cmds.append(node_sql.node_table)
    tblcreate_cmds.append(node_sql.nodecontent_table)

    sql_sql  = Tbls_sql_sql()

    tblcreate_cmds.append(sql_sql.sql_table)
    tblcreate_cmds.append(sql_sql.sqlselect_table)
    tblcreate_cmds.append(sql_sql.sqlfrom_table)
    tblcreate_cmds.append(sql_sql.sqljoin_table)
    tblcreate_cmds.append(sql_sql.sqlwhere_table)

    sqlvstable = Tbls_sqlvstable_sql()

    tblcreate_cmds.append(sqlvstable.sqlvstable_table)

    sqlsearch = Tbl_search_sql()
    tblcreate_cmds.append(sqlsearch.searchproject_table)
    tblcreate_cmds.append(sqlsearch.searchcase_table)
    tblcreate_cmds.append(sqlsearch.search_table)
    tblcreate_cmds.append(sqlsearch.searchcond_table)
    tblcreate_cmds.append(sqlsearch.searchnode_table)

    for tblcmd in tblcreate_cmds:
        dbsrv.sqlexec(tblcmd)
