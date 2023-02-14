

class GlobalData:
    # this class is used for storing data about the all project.

    def __init__(self):
        self.dbserver_       = []           # of type dbtool.DatabaseTool
        self.encrytkey_      = []
        self.dbconn_         = []           # Database connections
        self.dbnm_           = []           # Database names
        self.dbtype_         = []           # Database names
        self.db_tbl_lst_     = []           # Database table names
        self.db_proc_lst_    = []           # Database proc names
        self.noderoots_      = {}           # Node_
        self.sqls_           = {}           # SQL_
        self.tabletosqls_    = {}           # TabletoSQL_
        self.sqltotables_    = {}           # SQLtoTable_
        self.casecategories_ = {}           # CaseCategory_
        self.nodeid          = 0

        self.serverid        = 0
        self.dbid            = 0
        self.tableid         = 0
        self.procid          = 0
        self.columnid        = 0

        self.fileid          = 0
        self.sqlid           = 0
        self.sqlid_p         = 0
        self.sqlid_insert    = 0
        self.offset          = 0            # global offset inside file, for processing multiple sqls in the file
        self.offset_select   = 0            # offset in single query, from "insert" to "select"
        self.offset_from     = 0            # offset in single query, from "select" to "from"
        self.tables_tr       = Tables_TR()

        self.list_tr_sqlquerysrctables = []
        self.list_tr_sqlqueryselcols   = []
        self.list_tr_sqlquerytrace     = []
        self.list_tr_sqlinsertselcls   = []
        self.list_tr_sqlqueryfilter    = []
        self.list_tr_node = []
        self.list_tr_file = []
        self.list_tr_sql  = []
        self.nodelist        = []
        self.sqlqueryselcols = []
        self.sqltrace        = []
        self.sqlinsertsels   = []


# a DatabaseTool object has all information needed to login into a particular database.
# and, if needed, actually provide the connection by using db_connect() method.

# ------------------- database --------------------------

class Table:

    def __init__(self):
        #autoincrement in DB,from Database_ ---> id of Database,[] [Column_, Column, ... ],[TableRelate_, TableRelate_, ... ]
        self.__table_info_col =['table_id','tablename','db_id','cols','relate']
        self.__table_info = []

    def set_info(self, data):
        self.__table_info = data

    @property
    def table_info(self):
        return self.__table_info


class Column:

    def __init__(self):
        # autoincrement in DB,# from Table_ ---> id of Table,id of db
        self.__column_info_col = ['col_id','colname','datatype','table_id','db_id']
        self.__column_info = []

    def set_info(self, data):
        self.__column_info = data

    @property
    def column_info(self):
        return self.__column_info


class TableRelate:

    def __init__(self):
        ## from Database_ ---> id of Database,# from Table_    ---> id of table_, tbl1 has fk to tbl2
        self.__tablerelate_info_col = ['db_id','table1_id','col1_id','table2_id','col2_id','relate']
        self.__tablerelate_info = []

    def set_info (self, data):
        self.__tablerelate_info = data

    @property
    def tablerelate_info(self):
        return self.__tablerelate_info


# ------------------- New tables --------------------------

class Tables_TRO:
    def __init__(self):

        self.tro_maxid = "CREATE TABLE if not exists public.\"TRO_MaxID\"  \
        ( idname text, idvaluemax integer)                   \
        WITH (OIDS=FALSE);                                   \
        ALTER TABLE public.\"TRO_MaxID\" OWNER TO postgres;  \
        COMMENT ON  TABLE public.\"TRO_MaxID\" IS \'stores the maximum values of various IDs\';   \
        COMMENT ON COLUMN public.\"TRO_MaxID\".idname     IS \'IDName: name of the IDs\';         \
        COMMENT ON COLUMN public.\"TRO_MaxID\".idvaluemax IS \'IDValueMax: maximum value of the ID\';"

    def reset_count(self, idname, dbserver):

        sql = "select idvaluemax from public.\"TRO_MaxID\" where idname=\'%s\'" % idname
        rows = dbserver.sqlexec(sql)
        if rows:
            sql = "update public.\"TRO_MaxID\"" + \
                  " set idvaluemax = 0 "  + \
                  " where idname=\'" + idname + "\'"
            dbserver.sqlexec(sql)

    def maxid_insert(self, col, idname, dbserver):
        sql = "select idvaluemax from public.\"TRO_MaxID\" where idname=\'%s\'" % idname
        rows = dbserver.sqlexec(sql)
        if rows:
            sql = "update public.\"TRO_MaxID\"" + \
            " set idvaluemax = (select max(" + col + ") from public.\"" + idname + "\")" + \
            " where idname=\'" + idname + "\'"
        else:
            sql = "insert into public.\"TRO_MaxID\"" + \
                " select \'" + idname + "\', max(" + col + ") from public.\"" + idname +"\""
        dbserver.sqlexec(sql)

    def maxid_select(self,idname, dbserver):
        sql = "select idvaluemax from public.\"TRO_MaxID\" where idname=\'%s\'" % idname
        rows = dbserver.sqlexec(sql)
        n = -1
        for i in rows:
            n = i[0]
        if not type(n) == type(1):
            n = 0
        return n


class Tables_TR:
    def __init__(self):
        self.tbl_list = ['tr_sqlinsertselcols', 'tr_sqlqueryfilter', 'tr_sqlquerytrace', \
                         'tr_sqlquerysrctables', 'tr_sqlqueryselcols', 'tr_node',  'tr_file', \
                         'tr_sql', 'tr_column', 'tr_db', 'tr_dbcross', 'tr_sqltablecross', \
                         'tr_server', 'tr_smallcolumn', 'tr_storedproc', \
                         'tr_table', 'tr_treecolumns', 'tr_treefiles', 'tr_treetables', 'tr_searchstarts']
        self.tbl_insert_list   = []
        self.tbl_select_list   = []
        self.tbl_truncate_list = []


        self.tr_sqlinsertselcols = "CREATE TABLE if not exists public.\"TR_SQLInsertSelCols\"\
        ( file_id        integer,\
          query_sqlid    integer,\
          insrtposition  text,   \
          insrttblid     integer,\
          insrttblnm     text,   \
          insrtcolnm     text,   \
          selquery_sqlid integer,\
          seltblnm       text,   \
          selcolnm       text )  \
        WITH( OIDS=FALSE );      \
        ALTER TABLE public.\"TR_SQLInsertSelCols\" OWNER TO postgres;"
        self.tbl_insert_list.append("insert into public.\"TR_SQLInsertSelCols\" \
                                                values (%d, %d, %s, %d, %s, %s, %d, %s, %s)")
        self.tbl_select_list.append("select * from public.\"TR_SQLInsertSelCols\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_SQLInsertSelCols\"")

        self.tr_sqlqueryfilter = "CREATE TABLE if not exists public.\"TR_SQLQueryFilter\"\
        ( file_id integer, \
          qid1    integer, \
          qid2    integer, \
          cond_id integer, \
          w_id    integer, \
          cond    text,    \
          cmp     text,    \
          tbl1    text,    \
          col1    text,    \
          tbl2    text,    \
          col2    text,    \
          tbl3    text,    \
          col3    text)    \
        WITH( OIDS=FALSE );\
        ALTER TABLE public.\"TR_SQLQueryFilter\" OWNER TO postgres;"
        self.tbl_insert_list.append("insert into public.\"TR_SQLQueryFilter\" \
                            values (%d, %d, %d, %d, %d, %s, %s, %s, %s, %s, %s, %s, %s)")
        self.tbl_select_list.append("select * from public.\"TR_SQLQueryFilter\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_SQLQueryFilter\"")

        self.tr_sqlquerytrace = "CREATE TABLE if not exists public.\"TR_SQLQueryTrace\"\
        ( file_id        integer, \
          query_sqlid    integer,\
          inner_query_id integer,\
          selcolpos      integer, \
          colpos         text,   \
          tablenm        text,   \
          colnm          text  ) \
        WITH( OIDS=FALSE );      \
        ALTER TABLE public.\"TR_SQLQueryTrace\" OWNER TO postgres;"
        self.tbl_insert_list.append(
            "insert into public.\"TR_SQLQueryTrace\" values (%d, %d, %d, %d, %s, %s, %s)")
        self.tbl_select_list.append("select * from public.\"TR_SQLQueryTrace\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_SQLQueryTrace\"")

        self.tr_sqlquerysrctables = "CREATE TABLE if not exists public.\"TR_SQLQuerySrcTables\"\
        ( file_id     integer,\
          query_sqlid integer,\
          tablenm     text )  \
        WITH( OIDS=FALSE );   \
        ALTER TABLE public.\"TR_SQLQuerySrcTables\" OWNER TO postgres;"
        self.tbl_insert_list.append("insert into public.\"TR_SQLQuerySrcTables\" values (%d, %d, %s)")
        self.tbl_select_list.append("select * from public.\"TR_SQLQuerySrcTables\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_SQLQuerySrcTables\"")

        self.tr_sqlqueryselcols = "CREATE TABLE if not exists public.\"TR_SQLQuerySelCols\"\
        ( file_id        integer, \
          query_sqlid    integer, \
          inner_query_id integer, \
          tbl            text,    \
          alias          text,    \
          col            text,    \
          subqueryid     text,    \
          colpos         text,    \
          upperblockid   integer, \
          unionornot     text,    \
          inqueryoffset  integer )\
        WITH( OIDS=FALSE );\
        ALTER TABLE public.\"TR_SQLQuerySelCols\" OWNER TO postgres;"
        self.tbl_insert_list.append("insert into public.\"TR_SQLQuerySelCols\" \
                                               values (%d, %d, %d, %s, %s, %s, %s, %s, %d, %s, %d)")
        self.tbl_select_list.append("select * from public.\"TR_SQLQuerySelCols\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_SQLQuerySelCols\"")

        self.tr_node = "CREATE TABLE if not exists public.\"TR_Node\" \
        ( nodeid   integer,   \
          node_pid integer,   \
          parent   text,      \
          type     text,      \
          objectid integer,   \
          content  text,      \
          lastupdate timestamp with time zone default current_timestamp ) \
        WITH (OIDS=FALSE);                                                \
        ALTER TABLE public.\"TR_Node\" OWNER TO postgres;                 \
        COMMENT ON COLUMN public.\"TR_Node\".nodeid IS \'ID of the node\';                   \
        COMMENT ON COLUMN public.\"TR_Node\".node_pid IS \'Parent ID of the node\';          \
        COMMENT ON COLUMN public.\"TR_Node\".parent IS \'name of the parent, dir, file, db\';\
        COMMENT ON COLUMN public.\"TR_Node\".type IS \'type, file or sto proc, col\';        \
        COMMENT ON COLUMN public.\"TR_Node\".objectid IS \'ID of the object\';               \
        COMMENT ON COLUMN public.\"TR_Node\".content IS \'content of the object\';           \
        COMMENT ON COLUMN public.\"TR_Node\".lastupdate IS \'date of last update\';"
        self.tbl_insert_list.append("insert into public.\"TR_Node\" values (%d, %d, %s, %s, %d, %s, %s)")
        self.tbl_select_list.append("select * from public.\"TR_Node\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_Node\"")

        self.tr_file = "CREATE TABLE if not exists public.\"TR_File\" \
        ( fileid      integer,\
          serverid    integer,\
          ip          text,   \
          port        text,   \
          type        text,   \
          subtype     text,   \
          filepath    text,   \
          filename    text,   \
          filecontent text,   \
          msg         text,   \
          lastupdate timestamp with time zone )           \
        WITH (OIDS=FALSE);                                \
        ALTER TABLE public.\"TR_File\" OWNER TO postgres; \
        COMMENT ON TABLE  public.\"TR_File\" IS 'stores the content of files';             \
        COMMENT ON COLUMN public.\"TR_File\".fileid IS 'ID of the file';                   \
        COMMENT ON COLUMN public.\"TR_File\".serverid IS 'ID of the server, fopreign key'; \
        COMMENT ON COLUMN public.\"TR_File\".ip IS 'IP address';                       \
        COMMENT ON COLUMN public.\"TR_File\".port IS 'Port port number of the server'; \
        COMMENT ON COLUMN public.\"TR_File\".type IS 'file type';                      \
        COMMENT ON COLUMN public.\"TR_File\".subtype IS 'file sub type, suffix';       \
        COMMENT ON COLUMN public.\"TR_File\".filepath IS 'access path to the file';    \
        COMMENT ON COLUMN public.\"TR_File\".filename IS 'name of the file';           \
        COMMENT ON COLUMN public.\"TR_File\".filecontent IS 'content of a file';       \
        COMMENT ON COLUMN public.\"TR_File\".msg IS 'message about a file';       \
        COMMENT ON COLUMN public.\"TR_File\".lastupdate IS 'date of last update';"
        self.tbl_insert_list.append("insert into public.\"TR_File\" values (%d, %d, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        self.tbl_select_list.append("select * from public.\"TR_File\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_File\"")

        self.tr_sql = "CREATE TABLE if not exists public.\"TR_SQL\" \
        ( sqlid         integer,\
          sql_pid       integer,\
          name          text,   \
          boundryleft   integer,\
          boundaryright integer,\
          type          text,   \
          use_as        text,   \
          sqlblock      text,   \
          reserve       boolean,\
          level         integer,\
          hash          text  ) \
        WITH(OIDS=FALSE);       \
        ALTER TABLE public.\"TR_SQL\" OWNER TO postgres;                        \
        COMMENT ON TABLE public.\"TR_SQL\" IS \'SQL decomposed\';               \
        COMMENT ON COLUMN public.\"TR_SQL\".sqlid IS \'SQL block ID\';          \
        COMMENT ON COLUMN public.\"TR_SQL\".sql_pid IS \'parent SQL block ID\'; \
        COMMENT ON COLUMN public.\"TR_SQL\".name IS \'name of the sql block\';  \
        COMMENT ON COLUMN public.\"TR_SQL\".boundryleft IS \'Left boundary of sql block\';        \
        COMMENT ON COLUMN public.\"TR_SQL\".boundaryright IS \'right boundary of the sql block\'; \
        COMMENT ON COLUMN public.\"TR_SQL\".type IS \'type of the sql block\';          \
        COMMENT ON COLUMN public.\"TR_SQL\".use_as IS \'use as of the sql block\';      \
        COMMENT ON COLUMN public.\"TR_SQL\".sqlblock IS \'content of the sql block\';   \
        COMMENT ON COLUMN public.\"TR_SQL\".reserve IS \'reserved field\';              \
        COMMENT ON COLUMN public.\"TR_SQL\".level IS \'level of the sql block\';        \
        COMMENT ON COLUMN public.\"TR_SQL\".hash IS \'hash value of the sql block\';"
        self.tbl_insert_list.append("insert into public.\"TR_SQL\" values (%d, %d, %s, %d, %d, %s, %s, %s, %s, %d, %s)")
        self.tbl_select_list.append("select * from public.\"TR_SQL\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_SQL\"")

        self.tr_column = "CREATE TABLE if not exists public.\"TR_Column\"  \
        ( columnid integer,           \
          column_  text,              \
          tableid  integer,            \
          datatype text,              \
          distinctvaluecount integer, \
          lastupdate timestamp without time zone)           \
        WITH (OIDS=FALSE);                                  \
        ALTER TABLE public.\"TR_Column\" OWNER TO postgres; \
        COMMENT ON  TABLE public.\"TR_Column\" IS \'column level database info\';                 \
        COMMENT ON COLUMN public.\"TR_Column\".columnid   IS \'ID that globally unique\';         \
        COMMENT ON COLUMN public.\"TR_Column\".tableid    IS \'ID of the table\';                 \
        COMMENT ON COLUMN public.\"TR_Column\".datatype   IS \'data type of the column\';         \
        COMMENT ON COLUMN public.\"TR_Column\".distinctvaluecount IS \'count of distinct values\';\
        COMMENT ON COLUMN public.\"TR_Column\".lastupdate IS \'date of last update\';"

        self.tbl_insert_list.append("insert into public.\"TR_Column\" values (%d, %s, %d, %s, %d, %s)")
        self.tbl_select_list.append("select * from public.\"TR_Column\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_Column\"")

        self.tr_db = "CREATE TABLE if not exists public.\"TR_DB\"       \
        ( dbid integer,       \
          dbname text,        \
          dbport integer,     \
          dbtype text,        \
          dbdescription text, \
          serverid integer,   \
          connectionstring text) \
        WITH (OIDS=FALSE);       \
        ALTER TABLE public.\"TR_DB\" OWNER TO postgres; \
        COMMENT ON TABLE public.\"TR_DB\" IS \'TR_DB stores a list of databases\';    \
        COMMENT ON COLUMN public.\"TR_DB\".dbid     IS \'ID, globally uniquely\';     \
        COMMENT ON COLUMN public.\"TR_DB\".dbname   IS \'name of a database\';        \
        COMMENT ON COLUMN public.\"TR_DB\".dbport   IS \'port of a database\';        \
        COMMENT ON COLUMN public.\"TR_DB\".dbtype   IS \'DBType : type of a database, \
                     such as oracle, mssql, mysql, postgresql, db2, teradata, etc.\'; \
        COMMENT ON COLUMN public.\"TR_DB\".dbdescription IS \'desc of db\';           \
        COMMENT ON COLUMN public.\"TR_DB\".serverid IS \'ID of a server\';            \
        COMMENT ON COLUMN public.\"TR_DB\".connectionstring IS \'connection string of db\';"
        self.tbl_insert_list.append("insert into public.\"TR_DB\" values (%d, %s, %d, %s, %s, %d, %s)")
        self.tbl_select_list.append("select * from public.\"TR_DB\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_DB\"")

        self.tr_dbcross = "CREATE TABLE if not exists public.\"TR_DBCross\" \
        ( dbid1 integer,     \
          tableid1 integer,  \
          columnid1 integer, \
          dbid2 integer,     \
          tableid2 integer,  \
          columnid2 integer, \
          columnid2pk text,  \
          linkmethod integer,\
          lastupdate timestamp without time zone)              \
        WITH (OIDS=FALSE);                                     \
        ALTER TABLE public.\"TR_DBCross\" OWNER TO postgres;   \
        COMMENT ON COLUMN public.\"TR_DBCross\".dbid1       IS \'ID of database 1\';               \
        COMMENT ON COLUMN public.\"TR_DBCross\".tableid1    IS \'ID of table of database 1\';      \
        COMMENT ON COLUMN public.\"TR_DBCross\".columnid1   IS \'ID of column 1\';                 \
        COMMENT ON COLUMN public.\"TR_DBCross\".dbid2       IS \'ID of database 2\';               \
        COMMENT ON COLUMN public.\"TR_DBCross\".tableid2    IS \'ID of table of database 2\';      \
        COMMENT ON COLUMN public.\"TR_DBCross\".columnid2   IS \'ID of column 2\';                 \
        COMMENT ON COLUMN public.\"TR_DBCross\".columnid2pk IS \'column 2 is primary key, T or F\';\
        COMMENT ON COLUMN public.\"TR_DBCross\".linkmethod  IS \'relate columnid1 and columnid2\'; \
        COMMENT ON COLUMN public.\"TR_DBCross\".lastupdate  IS \'last update\';"
        self.tbl_insert_list.append("insert into public.\"TR_DBCross\" values (%d, %d, %d, %d, %d, %d, %s, %d, %s)")
        self.tbl_select_list.append("select * from public.\"TR_DBCross\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_DBCross\"")

        self.tr_sqltablecross = "CREATE TABLE if not exists public.\"TR_SQLTableCross\"  \
        ( nodeid1  integer,    \
          nodeid2  integer,    \
          dbid1    integer,    \
          dbid2    integer,    \
          tableid  integer,    \
          columnid integer,    \
          linkmethod text,     \
          direction text,      \
          sourceorfilter text, \
          lastupdate timestamp without time zone)                  \
        WITH (OIDS=FALSE);                                         \
        ALTER TABLE public.\"TR_SQLTableCross\" OWNER TO postgres; \
        COMMENT ON COLUMN public.\"TR_SQLTableCross\".nodeid1    IS \'ID of node on side 1\';     \
        COMMENT ON COLUMN public.\"TR_SQLTableCross\".nodeid2    IS \'ID of node on side 2\';     \
        COMMENT ON COLUMN public.\"TR_SQLTableCross\".dbid1      IS \'ID of database on side 1\'; \
        COMMENT ON COLUMN public.\"TR_SQLTableCross\".dbid2      IS \'ID of database on side 2\'; \
        COMMENT ON COLUMN public.\"TR_SQLTableCross\".tableid    IS \'ID of table on side 2\';    \
        COMMENT ON COLUMN public.\"TR_SQLTableCross\".columnid   IS \'ID of column on side 2\';   \
        COMMENT ON COLUMN public.\"TR_SQLTableCross\".linkmethod IS \'relate SQL and table\';     \
        COMMENT ON COLUMN public.\"TR_SQLTableCross\".direction  IS \'to or from database\';      \
        COMMENT ON COLUMN public.\"TR_SQLTableCross\".sourceorfilter IS \'source/target/filter\'; \
        COMMENT ON COLUMN public.\"TR_SQLTableCross\".lastupdate IS \'last update date\';"
        self.tbl_insert_list.append("insert into public.\"TR_SQLTableCross\" values (%d, %d, %d, %d, %d, %d, %s, %s, %s, %s)")
        self.tbl_select_list.append("select * from public.\"TR_SQLTableCross\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_SQLTableCross\"")

        self.tr_server = "CREATE TABLE if not exists public.\"TR_Server\"  \
        ( serverid integer, \
          server   text)    \
        WITH (OIDS=FALSE);  \
        ALTER TABLE public.\"TR_Server\" OWNER TO postgres;  \
        COMMENT ON  TABLE public.\"TR_Server\"          IS \'TR_Server stores a list of servers\';  \
        COMMENT ON COLUMN public.\"TR_Server\".serverid IS \'ServerID ID of the server\';           \
        COMMENT ON COLUMN public.\"TR_Server\".server     IS 'Server server IP address or DNS URL \';"

        self.tbl_insert_list.append("insert into public.\"TR_Server\" values (%d, %s)")
        self.tbl_select_list.append("select * from public.\"TR_Server\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_Server\"")

        self.tr_smallcolumn = "CREATE TABLE if not exists public.\"TR_SmallColumn\"  \
        ( dbid               integer,\
          tableid            integer,\
          distinctvaluecount integer,\
          distinctvalue1 text, \
          distinctvalue2 text, \
          distinctvalue3 text, \
          distinctvalue4 text, \
          distinctvalue5 text, \
          distinctvalue6 text, \
          distinctvalue7 text, \
          distinctvalue8 text, \
          distinctvalue9 text, \
          distinctvalue10 text)\
        WITH (OIDS=FALSE);     \
        ALTER TABLE public.\"TR_SmallColumn\" OWNER TO postgres;                                   \
        COMMENT ON  TABLE public.\"TR_SmallColumn\" IS \'no more than 10 distinct values\';        \
        COMMENT ON COLUMN public.\"TR_SmallColumn\".dbid IS \'DBID ID of the database';            \
        COMMENT ON COLUMN public.\"TR_SmallColumn\".tableid IS \'TableID denotes the table';       \
        COMMENT ON COLUMN public.\"TR_SmallColumn\".distinctvaluecount IS \'count distinct values';\
        COMMENT ON COLUMN public.\"TR_SmallColumn\".distinctvalue1 IS \'DistinctValue1\';\
        COMMENT ON COLUMN public.\"TR_SmallColumn\".distinctvalue2 IS \'DistinctValue2\';\
        COMMENT ON COLUMN public.\"TR_SmallColumn\".distinctvalue3 IS \'DistinctValue3\';\
        COMMENT ON COLUMN public.\"TR_SmallColumn\".distinctvalue4 IS \'DistinctValue4\';\
        COMMENT ON COLUMN public.\"TR_SmallColumn\".distinctvalue5 IS \'DistinctValue5\';\
        COMMENT ON COLUMN public.\"TR_SmallColumn\".distinctvalue6 IS \'DistinctValue6\';\
        COMMENT ON COLUMN public.\"TR_SmallColumn\".distinctvalue7 IS \'DistinctValue7\';\
        COMMENT ON COLUMN public.\"TR_SmallColumn\".distinctvalue8 IS \'DistinctValue8\';\
        COMMENT ON COLUMN public.\"TR_SmallColumn\".distinctvalue9 IS \'DistinctValue9\';\
        COMMENT ON COLUMN public.\"TR_SmallColumn\".distinctvalue10 IS \'DistinctValue10\';"
        self.tbl_insert_list.append("insert into public.\"TR_SmallColumn\" values (%d, %d, %d, %s, %s, %s, %s, %s, %s, %s, %d, %s, %s)")
        self.tbl_select_list.append("select * from public.\"TR_SmallColumn\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_SmallColumn\"")

        self.tr_storedproc = "CREATE TABLE if not exists public.\"TR_StoredProc\"    \
        ( storedprocid      integer,\
          dbid              integer,\
          storedprocname    text,   \
          storedproccontent text)   \
        WITH (OIDS=FALSE);          \
        ALTER TABLE public.\"TR_StoredProc\" OWNER TO postgres;                                \
        COMMENT ON  TABLE public.\"TR_StoredProc\" IS \'stores content\';                      \
        COMMENT ON COLUMN public.\"TR_StoredProc\".storedprocid IS \'ID of the stored proc\';  \
        COMMENT ON COLUMN public.\"TR_StoredProc\".dbid IS \'ID of the database\';             \
        COMMENT ON COLUMN public.\"TR_StoredProc\".storedprocname    IS \'name stored proc\';  \
        COMMENT ON COLUMN public.\"TR_StoredProc\".storedproccontent IS \'content stored proc\';"\

        self.tbl_insert_list.append("insert into public.\"TR_StoredProc\" values (%d, %d, %s)")
        self.tbl_select_list.append("select * from public.\"TR_StoredProc\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_StoredProc\"")

        self.tr_table = "CREATE TABLE if not exists public.\"TR_Table\"    \
        ( tableid    integer, \
          tablename  text,  \
          primarykey text, \
          primarykeycolumnid1 integer, \
          primarykeycolumnid2 integer, \
          primarykeycolumnid3 integer, \
          tableproperty text,          \
          rowcount integer,            \
          dbid integer,                \
          createdate timestamp without time zone, \
          lastupdate timestamp without time zone) \
        WITH (OIDS=FALSE);                        \
        ALTER TABLE public.\"TR_Table\" OWNER TO postgres; \
        COMMENT ON  TABLE public.\"TR_Table\" IS \'TR_Table stores a list of tables\';              \
        COMMENT ON COLUMN public.\"TR_Table\".tableid    IS \'TableID is the ID of a db table\';    \
        COMMENT ON COLUMN public.\"TR_Table\".tablename  IS \'TableName is the name of a table\';   \
        COMMENT ON COLUMN public.\"TR_Table\".primarykey IS \'PrimaryKey  has primary key. T or F\';\
        COMMENT ON COLUMN public.\"TR_Table\".primarykeycolumnid1 IS \'ID of the primary key\';     \
        COMMENT ON COLUMN public.\"TR_Table\".primarykeycolumnid2 IS \'ID of the primary key.   \'; \
        COMMENT ON COLUMN public.\"TR_Table\".primarykeycolumnid3 IS \'ID ot primary column    \';  \
        COMMENT ON COLUMN public.\"TR_Table\".tableproperty IS \'TableProperty  temp, regular,   \';\
        COMMENT ON COLUMN public.\"TR_Table\".rowcount   IS \'RowCount  the count of rows\';        \
        COMMENT ON COLUMN public.\"TR_Table\".dbid       IS \'DBID ID of the database\';            \
        COMMENT ON COLUMN public.\"TR_Table\".createdate IS \'CreateDate  date of creation\';       \
        COMMENT ON COLUMN public.\"TR_Table\".lastupdate IS \'LastUpdate date of last update\';"
        self.tbl_insert_list.append("insert into public.\"TR_Table\" values (%d, %s, %s, %d, %d, %d, %s, %d, %d, %s, %s)")
        self.tbl_select_list.append("select * from public.\"TR_Table\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_Table\"")

        self.tr_treecolumns = "CREATE TABLE if not exists public.\"TR_TreeColumns\"   \
        ( nodeid integer,       \
          nodeparentid integer, \
          linkmethod text,      \
          tableid integer,      \
          columnid integer,     \
          lastupdate timestamp without time zone) \
        WITH (OIDS=FALSE);                        \
        ALTER TABLE public.\"TR_TreeColumns\" OWNER TO postgres; \
        COMMENT ON TABLE public.\"TR_TreeColumns\"               \
          IS \'TreeColumns is the \"lower level\" of the (TreeTables, TreeColumns)\';               \
        COMMENT ON COLUMN public.\"TR_TreeColumns\".nodeid       IS \'ID of node of the column\';   \
        COMMENT ON COLUMN public.\"TR_TreeColumns\".nodeparentid IS \'ID of parent node\';          \
        COMMENT ON COLUMN public.\"TR_TreeColumns\".linkmethod   IS \'relate node and parent node\';\
        COMMENT ON COLUMN public.\"TR_TreeColumns\".tableid      IS \'ID of the table\';            \
        COMMENT ON COLUMN public.\"TR_TreeColumns\".columnid     IS \'ID of column\';               \
        COMMENT ON COLUMN public.\"TR_TreeColumns\".lastupdate   IS \'last update date\';"
        self.tbl_insert_list.append("insert into public.\"TR_TreeColumns\" values (%d, %d, %s, %d, %d, %s)")
        self.tbl_select_list.append("select * from public.\"TR_TreeColumns\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_TreeColumns\"")

        self.tr_treefiles = "CREATE TABLE if not exists public.\"TR_TreeFiles\"  \
        ( nodeid integer,                 \
          nodeparentid integer,           \
          linkmethod text,                \
          fileid integer,                 \
          lineoffsetinfile1 integer,      \
          lineoffsetinfile2 integer,      \
          lastupdate timestamp without time zone)    \
        WITH (OIDS=FALSE);                           \
        ALTER TABLE public.\"TR_TreeFiles\" OWNER TO postgres; \
        COMMENT ON TABLE public.\"TR_TreeFiles\"               \
          IS \'store the result of a first, unversal scan over the entire file system.\';          \
        COMMENT ON COLUMN public.\"TR_TreeFiles\".nodeid IS \'globally unique, auto generated.     \
                                  It stores the result of the first and universal scan over the    \
                                  entire file system that can be reached with given start point,   \
                                  which are usually root directories in the file system.\';        \
        COMMENT ON COLUMN public.\"TR_TreeFiles\".nodeparentid      IS \'NodeID of another node,   \
                                  Together, (NodeID, NodeParentID) a tree structure of nodes\';    \
        COMMENT ON COLUMN public.\"TR_TreeFiles\".linkmethod        IS \'parent-child\';           \
        COMMENT ON COLUMN public.\"TR_TreeFiles\".fileid            IS \'ID of a file\';           \
        COMMENT ON COLUMN public.\"TR_TreeFiles\".lineoffsetinfile1 IS \'code section start\';     \
        COMMENT ON COLUMN public.\"TR_TreeFiles\".lineoffsetinfile2 IS \'end point code section\'; \
        COMMENT ON COLUMN public.\"TR_TreeFiles\".lastupdate        IS \'date last update\';"
        self.tbl_insert_list.append("insert into public.\"TR_TreeFiles\" values (%d, %d, %s, %d, %d, %d, %s)")
        self.tbl_select_list.append("select * from public.\"TR_TreeFiles\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_TreeFiles\"")

        self.tr_treetables = "CREATE TABLE if not exists public.\"TR_TreeTables\"    \
        ( nodeid integer,                         \
          nodeparentid integer,                   \
          linkmethod integer,                     \
          serverid integer,                       \
          dbid integer,                           \
          tableid integer,                        \
          lastupdate timestamp without time zone) \
        WITH (OIDS=FALSE);                        \
        ALTER TABLE public.\"TR_TreeTables\" OWNER TO postgres; \
        COMMENT ON TABLE public.\"TR_TreeTables\"               \
         IS \'result of the first scan of the entire database system.\';                           \
        COMMENT ON COLUMN public.\"TR_TreeTables\".nodeid       IS \'globally unique integers\';   \
        COMMENT ON COLUMN public.\"TR_TreeTables\".nodeparentid IS \'NodeID of parent node\';      \
        COMMENT ON COLUMN public.\"TR_TreeTables\".linkmethod   IS \'relate NodeParentID NodeID.\';\
        COMMENT ON COLUMN public.\"TR_TreeTables\".serverid     IS \'ID of a server\';             \
        COMMENT ON COLUMN public.\"TR_TreeTables\".dbid         IS \'ID of the database\';         \
        COMMENT ON COLUMN public.\"TR_TreeTables\".tableid      IS \'ID of the table\';            \
        COMMENT ON COLUMN public.\"TR_TreeTables\".lastupdate   IS \'date last updatee\';"
        self.tbl_insert_list.append("insert into public.\"TR_TreeTables\" values (%d, %d, %d, %d, %d, %d, %s)")
        self.tbl_select_list.append("select * from public.\"TR_TreeTables\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_TreeTables\"")

        self.tr_searchstarts = "CREATE TABLE if not exists public.\"TR_SearchStarts\"  \
        ( nodeid integer,  \
          startpoint text, \
          lastupdate timestamp without time zone) \
        WITH (OIDS=FALSE);                        \
        ALTER TABLE public.\"TR_SearchStarts\" OWNER TO postgres; \
        COMMENT ON TABLE public.\"TR_SearchStarts\"               \
         IS \'starting points of searches in file system.\';                                       \
        COMMENT ON COLUMN public.\"TR_SearchStarts\".nodeid     IS \'globally unique integers\';   \
        COMMENT ON COLUMN public.\"TR_SearchStarts\".startpoint IS \'Starting point of searching\';\
        COMMENT ON COLUMN public.\"TR_SearchStarts\".lastupdate IS \'date last updatee\';"
        self.tbl_insert_list.append("insert into public.\"TR_SearchStarts\" values (%d, %s, %s)")
        self.tbl_select_list.append("select * from public.\"TR_SearchStarts\"")
        self.tbl_truncate_list.append("truncate table public.\"TR_SearchStarts\"")


    def get_sql_stmt_(self, tblname, stmt_type):
        if tblname.find(".") >= 0:
            [schema, tblname] = tblname.lower().split('.')
        else:
            tblname = tblname.lower()
        stmt = ""
        for i in range(len(self.tbl_list)):
            if self.tbl_list[i] == tblname:
                if   stmt_type == "select":
                    stmt = self.tbl_select_list[i]
                elif stmt_type == "insert":
                    stmt = self.tbl_insert_list[i]
                elif stmt_type == 'truncate':
                    stmt = self.tbl_truncate_list[i]
                break
        return stmt


class Tables_TRC:
    def __init__(self):
        self.trc_case = "CREATE TABLE if not exists public.\"TRC_Case\" \
        (caseid integer, casename text, casedescription text, lastupdate timestamp without time zone)\
        WITH (OIDS=FALSE) ;                                                                    \
        ALTER TABLE public.\"TRC_Case\" OWNER TO postgres;                                     \
        COMMENT ON  TABLE public.\"TRC_Case\" IS \'TRC_Case stores a list of cases\';          \
        COMMENT ON COLUMN public.\"TRC_Case\".caseid IS \'ID of the case.\';                   \
        COMMENT ON COLUMN public.\"TRC_Case\".casename IS \'CaseName  name of the case\';      \
        COMMENT ON COLUMN public.\"TRC_Case\".casedescription IS \'description of the case\';  \
        COMMENT ON COLUMN public.\"TRC_Case\".lastupdate IS \'date of the last update\';  "


        self.trc_casesearchcross = "CREATE TABLE if not exists public.\"TRC_CaseSearchCross\" \
        (caseid integer, searchid integer, listed text, listorder integer, opened text,  \
         openorder integer, lastupdate timestamp without time zone)                      \
        WITH(OIDS=FALSE);                                                                           \
        ALTER TABLE public.\"TRC_CaseSearchCross\" OWNER TO postgres;                               \
        COMMENT ON TABLE  public.\"TRC_CaseSearchCross\" IS \'cross linkage case and search\';      \
        COMMENT ON COLUMN public.\"TRC_CaseSearchCross\".caseid IS \'CaseID  ID of the case\';      \
        COMMENT ON COLUMN public.\"TRC_CaseSearchCross\".searchid IS \'SearchID ID of the search\'; \
        COMMENT ON COLUMN public.\"TRC_CaseSearchCross\".listed IS \'Listed  T or F\';              \
        COMMENT ON COLUMN public.\"TRC_CaseSearchCross\".listorder IS \'order of search in case\';  \
        COMMENT ON COLUMN public.\"TRC_CaseSearchCross\".opened IS \'Opened  T or F\';              \
        COMMENT ON COLUMN public.\"TRC_CaseSearchCross\".openorder IS \'order of search in case \'; \
        COMMENT ON COLUMN public.\"TRC_CaseSearchCross\".lastupdate IS \'date of the last update\';"


        self.trc_display = "CREATE TABLE if not exists public.\"TRC_Display\"  \
        (displayid integer, lastupdate timestamp without time zone)        \
        WITH (OIDS=FALSE);                                                 \
        ALTER TABLE public.\"TRC_Display\" OWNER TO postgres;                                  \
        COMMENT ON TABLE public.\"TRC_Display\" IS \'holds a Display ID\';                     \
        COMMENT ON COLUMN public.\"TRC_Display\".displayid IS \'DisplayID  ID of the display\';\
        COMMENT ON COLUMN public.\"TRC_Display\".lastupdate IS \'date of the last update\'; "


        self.trc_displaycasecross = "CREATE TABLE if not exists public.\"TRC_DisplayCaseCross\"  \
        (displayid integer, caseid integer, listed text, listorder integer, opened text,    \
         openorder integer, lastupdate timestamp without time zone)                         \
        WITH (OIDS=FALSE);                                 \
        ALTER TABLE public.\"TRC_DisplayCaseCross\"        \
          OWNER TO postgres;                               \
        COMMENT ON TABLE public.\"TRC_DisplayCaseCross\"   \
          IS \'TRC_DisplayCaseCross  cross linkage between displays and cases.          \
              A display scenario may be used by multiple search cases.\';               \
        COMMENT ON COLUMN public.\"TRC_DisplayCaseCross\".displayid  IS \'DisplayID\';  \
        COMMENT ON COLUMN public.\"TRC_DisplayCaseCross\".caseid     IS \'CaseID\';     \
        COMMENT ON COLUMN public.\"TRC_DisplayCaseCross\".listed     IS \'T or F, listed or not\';  \
        COMMENT ON COLUMN public.\"TRC_DisplayCaseCross\".listorder  IS \'display order of case\';  \
        COMMENT ON COLUMN public.\"TRC_DisplayCaseCross\".opened     IS \'Opened   T or F\';        \
        COMMENT ON COLUMN public.\"TRC_DisplayCaseCross\".openorder  IS \'open order of case\';     \
        COMMENT ON COLUMN public.\"TRC_DisplayCaseCross\".lastupdate IS \'date last update \';"

        self.trc_nodedisplaycoordinate = "CREATE TABLE if not exists public.\"TRC_NodeDisplayCoordinate\" \
        (nodeid integer, displaycoordinateid integer, x integer, y integer, color text,             \
         size integer,comment text, lastupdate timestamp without time zone)                         \
        WITH (OIDS=FALSE);                                                                          \
        ALTER TABLE public.\"TRC_NodeDisplayCoordinate\" OWNER TO postgres;                         \
        COMMENT ON  TABLE public.\"TRC_NodeDisplayCoordinate\" IS \'screen properties display\';    \
        COMMENT ON COLUMN public.\"TRC_NodeDisplayCoordinate\".nodeid IS \'node to be displayed\';  \
        COMMENT ON COLUMN public.\"TRC_NodeDisplayCoordinate\".displaycoordinateid IS \'coord IDs\';\
        COMMENT ON COLUMN public.\"TRC_NodeDisplayCoordinate\".x IS \'x coordinate\';               \
        COMMENT ON COLUMN public.\"TRC_NodeDisplayCoordinate\".y IS \'y  coordinate\';              \
        COMMENT ON COLUMN public.\"TRC_NodeDisplayCoordinate\".color IS \'Color of the node\';      \
        COMMENT ON COLUMN public.\"TRC_NodeDisplayCoordinate\".size IS \'size of the node\';        \
        COMMENT ON COLUMN public.\"TRC_NodeDisplayCoordinate\".comment IS \'Comment of the node\';  \
        COMMENT ON COLUMN public.\"TRC_NodeDisplayCoordinate\".lastupdate IS \'date last update\'; "

        self.trc_searchnodecross = "CREATE TABLE if not exists public.\"TRC_SearchNodeCross\"     \
        (searchid integer, nodeid integer, centervalue text, opened text, openorder integer, \
         displaycoordinateid integer, lastupdate timestamp without time zone)                \
        WITH (OIDS=FALSE);                                                                            \
        ALTER TABLE public.\"TRC_SearchNodeCross\" OWNER TO postgres;                                 \
        COMMENT ON  TABLE public.\"TRC_SearchNodeCross\" IS \'the layout info of nodes on screen.\';  \
        COMMENT ON COLUMN public.\"TRC_SearchNodeCross\".searchid IS \'ID of the search\';            \
        COMMENT ON COLUMN public.\"TRC_SearchNodeCross\".nodeid IS \'ID of the node in the search\';  \
        COMMENT ON COLUMN public.\"TRC_SearchNodeCross\".centervalue IS \'value in center on screen\';\
        COMMENT ON COLUMN public.\"TRC_SearchNodeCross\".opened IS \'T or F. opened on the screen\';  \
        COMMENT ON COLUMN public.\"TRC_SearchNodeCross\".openorder IS \'order of open, from left \';  \
        COMMENT ON COLUMN public.\"TRC_SearchNodeCross\".displaycoordinateid IS \'ID display coordi\';\
        COMMENT ON COLUMN public.\"TRC_SearchNodeCross\".lastupdate IS \'date of the last update\';"


class Tables_TRR:
    def __init__(self):
        self.trr_filedataflow = "CREATE TABLE if not exists public.\"TRR_FileDataFlow\"         \
        (nodeid1 integer, filepath1 text, filename1 text, nodeid2 integer, filepath2 text, \
         filename2 text, linkmethod text, lastupdate timestamp without time zone)          \
        WITH (OIDS=FALSE);                                                                 \
        ALTER TABLE public.\"TRR_FileDataFlow\" OWNER TO postgres;                         \
        COMMENT ON  TABLE public.\"TRR_FileDataFlow\" IS \'record the data flow between codes\'; \
        COMMENT ON COLUMN public.\"TRR_FileDataFlow\".nodeid1    IS \'source node\';         \
        COMMENT ON COLUMN public.\"TRR_FileDataFlow\".filepath1  IS \'path to file 1\';      \
        COMMENT ON COLUMN public.\"TRR_FileDataFlow\".filename1  IS \'file name of file 1\'; \
        COMMENT ON COLUMN public.\"TRR_FileDataFlow\".nodeid2    IS \'node of file 2\';      \
        COMMENT ON COLUMN public.\"TRR_FileDataFlow\".filepath2  IS \'path to file 2\';      \
        COMMENT ON COLUMN public.\"TRR_FileDataFlow\".filename2  IS \'file name of file 2\'; \
        COMMENT ON COLUMN public.\"TRR_FileDataFlow\".linkmethod IS \'forward or backward\'; \
        COMMENT ON COLUMN public.\"TRR_FileDataFlow\".lastupdate IS \'date of last update\';"

        self.trr_filefile = "CREATE TABLE if not exists public.\"TRR_FileFile\"                \
        (nodeid1 integer, filepath1 text, filename1 text, nodeid2 integer, filepath2 text, \
         filename2 text, linkmethod text, lastupdate timestamp without time zone)          \
        WITH (OIDS=FALSE);                                                                 \
        ALTER TABLE public.\"TRR_FileFile\" OWNER TO postgres;                             \
        COMMENT ON  TABLE public.\"TRR_FileFile\"            IS \'defines file - file relationship\';\
        COMMENT ON COLUMN public.\"TRR_FileFile\".nodeid1    IS \'denotes the node on side 1\';      \
        COMMENT ON COLUMN public.\"TRR_FileFile\".filepath1  IS \'path to the file of NodeID1\';     \
        COMMENT ON COLUMN public.\"TRR_FileFile\".filename1  IS \'file on side 1p\';                 \
        COMMENT ON COLUMN public.\"TRR_FileFile\".nodeid2    IS \'node on side 2\';                  \
        COMMENT ON COLUMN public.\"TRR_FileFile\".filepath2  IS \'path to the node NodeID2\';        \
        COMMENT ON COLUMN public.\"TRR_FileFile\".filename2  IS \'file on side 2\';                  \
        COMMENT ON COLUMN public.\"TRR_FileFile\".linkmethod IS \'has values: call, becalled\';      \
        COMMENT ON COLUMN public.\"TRR_FileFile\".lastupdate IS \'date of last update     \';"


class Tables_TRSQL:
    def __init__(self):
        self.trsql_block = "CREATE TABLE if not exists public.\"TRSQL_Block\" \
        (blockid integer,     \
        blockparentid integer,\
        blockname text,       \
        left_idx integer,     \
        right_idx integer,    \
        type text,            \
        use_as text,          \
        content text,         \
        union_ boolean,       \
        level integer,        \
        hashvalue text        \
        )                                                      \
        WITH (OIDS=FALSE);                                     \
        ALTER TABLE public.\"TRSQL_Block\" OWNER TO postgres;  \
        COMMENT ON  TABLE public.\"TRSQL_Block\" IS \'server info where the SQL resides.\';    \
        COMMENT ON COLUMN public.\"TRSQL_Block\".blockid IS \'ID of the SQL block.\';          \
        COMMENT ON COLUMN public.\"TRSQL_Block\".blockparentid IS \'ID of the parent block\';  \
        COMMENT ON COLUMN public.\"TRSQL_Block\".blockname IS \'name of the with statement\';  \
        COMMENT ON COLUMN public.\"TRSQL_Block\".left_idx IS \'position of the left boundary of the block in the sql, start from 0\';  \
        COMMENT ON COLUMN public.\"TRSQL_Block\".right_idx IS \'position of the right boundary of the block in the sql, start from 0\';\
        COMMENT ON COLUMN public.\"TRSQL_Block\".type IS \'block type: select, from, join, where, group by, order by, table, column\'; \
        COMMENT ON COLUMN public.\"TRSQL_Block\".content IS \'original text of the block in the sql\';           \
        COMMENT ON COLUMN public.\"TRSQL_Block\".level IS \'logical level of nesting. top level is 1\';          \
        COMMENT ON COLUMN public.\"TRSQL_Block\".union_ IS \'whether this block is unioned to other block\';     \
        COMMENT ON COLUMN public.\"TRSQL_Block\".hashvalue IS \'hashvalue so this record is easily searchable\';"

        self.trsql_blockhost = "CREATE TABLE if not exists public.\"TRSQL_BlockHost\" \
        (blockid integer, nodeid integer)                                         \
        WITH (OIDS=FALSE);                                                        \
        ALTER TABLE public.\"TRSQL_BlockHost\" OWNER TO postgres;                 \
        COMMENT ON  TABLE public.\"TRSQL_BlockHost\" IS \'server info where the SQL resides.\'; \
        COMMENT ON COLUMN public.\"TRSQL_BlockHost\".blockid IS \'ID of the SQL block.\';       \
        COMMENT ON COLUMN public.\"TRSQL_BlockHost\".nodeid  IS \'ID of the node.\' "

        self.trsql_blockcolumn = "CREATE TABLE if not exists public.\"TRSQL_BlockColumn\"  \
        (blockid integer,\
        server text,     \
        db text,         \
        table_  text,    \
        column_ text,    \
        serverid integer,\
        dbid integer,    \
        tableid integer, \
        columnid integer,\
        columnfunc text  \
        )                \
        WITH (OIDS=FALSE);                                                      \
        ALTER TABLE public.\"TRSQL_BlockColumn\" OWNER TO postgres;             \
        COMMENT ON  TABLE public.\"TRSQL_BlockColumn\" IS \'table and column used in block\';        \
        COMMENT ON COLUMN public.\"TRSQL_BlockColumn\".blockid IS \'ID of the block\';               \
        COMMENT ON COLUMN public.\"TRSQL_BlockColumn\".server IS \'ip address, or url ofthe server\';\
        COMMENT ON COLUMN public.\"TRSQL_BlockColumn\".db IS \'database name\';                  \
        COMMENT ON COLUMN public.\"TRSQL_BlockColumn\".table_ IS 'table name\';                  \
        COMMENT ON COLUMN public.\"TRSQL_BlockColumn\".column_ IS \'column name\';               \
        COMMENT ON COLUMN public.\"TRSQL_BlockColumn\".serverid IS \'ID of the server\';         \
        COMMENT ON COLUMN public.\"TRSQL_BlockColumn\".dbid IS \'ID ofthe database\';            \
        COMMENT ON COLUMN public.\"TRSQL_BlockColumn\".tableid IS \'Id of the table\';           \
        COMMENT ON COLUMN public.\"TRSQL_BlockColumn\".columnid IS \'ID of the column\';         \
        COMMENT ON COLUMN public.\"TRSQL_BlockColumn\".columnfunc IS \'source, target, filter\';"

# Search result
class Tables_TRSR:
    def __init__(self):

        self.trsr_chain = "CREATE TABLE if not exists public.\"TRSR_Chain\"  \
        (chainid integer,                                                \
        nodeid1 integer, nodeid2  integer,nodeid3  integer,nodeid4  integer,nodeid5  integer,  \
        nodeid6 integer, nodeid7  integer,nodeid8  integer,nodeid9  integer,nodeid10 integer,  \
        nodeid11 integer,nodeid12 integer,nodeid13 integer,nodeid14 integer,nodeid15 integer,  \
        nodeid16 integer,nodeid17 integer,nodeid18 integer,nodeid19 integer,nodeid20 integer,  \
        nodeid21 integer,nodeid22 integer,nodeid23 integer,nodeid24 integer,nodeid25 integer,  \
        nodeid26 integer,nodeid27 integer,nodeid28 integer,nodeid29 integer,nodeid30 integer,  \
        nodeid31 integer,nodeid32 integer,nodeid33 integer,nodeid34 integer,nodeid35 integer,  \
        nodeid36 integer,nodeid37 integer,nodeid38 integer,nodeid39 integer,nodeid40 integer,  \
        nodeid41 integer,nodeid42 integer,nodeid43 integer,nodeid44 integer,nodeid45 integer,  \
        nodeid46 integer,nodeid47 integer,nodeid48 integer,nodeid49 integer,nodeid50 integer   ) \
        WITH (OIDS=FALSE);                                                    \
        ALTER TABLE public.\"TRSR_Chain\" OWNER TO postgres;                  \
        COMMENT ON  TABLE public.\"TRSR_Chain\" IS \'chains are frequently passed routes\';    \
        COMMENT ON COLUMN public.\"TRSR_Chain\".chainid IS \'ID of the chain. A common path\'; \
        COMMENT ON COLUMN public.\"TRSR_Chain\".nodeid1 IS \'ID of the first node in the chain\';"

        self.trsr_pickupnodecross = "CREATE TABLE if not exists public.\"TRSR_PickupNodeCross\"  \
        (searchid integer, pickupnodeid integer)     \
        WITH (OIDS=FALSE);                           \
        ALTER TABLE public.\"TRSR_PickupNodeCross\" OWNER TO postgres;                            \
        COMMENT ON  TABLE public.\"TRSR_PickupNodeCross\" IS \'nodes that actually be opened\';   \
        COMMENT ON COLUMN public.\"TRSR_PickupNodeCross\".searchid IS \'ID of a search\';         \
        COMMENT ON COLUMN public.\"TRSR_PickupNodeCross\".pickupnodeid IS \'ID of a pick up node\';"

        self.trsr_result = "CREATE TABLE if not exists public.\"TRSR_Result\"              \
        (nodeid integer, previousnodeid integer, linkmethod integer, searchid integer) \
        WITH (OIDS=FALSE);                                                             \
        ALTER TABLE public.\"TRSR_Result\" OWNER TO postgres;                          \
        COMMENT ON  TABLE public.\"TRSR_Result\" IS \'result of the search as a linklist.\';        \
        COMMENT ON COLUMN public.\"TRSR_Result\".nodeid IS \'ID of the node in the search result\'; \
        COMMENT ON COLUMN public.\"TRSR_Result\".previousnodeid IS \'NodeID of the previous node\'; \
        COMMENT ON COLUMN public.\"TRSR_Result\".linkmethod IS \' how this node is linked.          \
        by calling sequence, by data flow, by data relation similar to ER relation, etc.\';         \
        COMMENT ON COLUMN public.\"TRSR_Result\".searchid IS \'SearchID  ID of the search\'; "

        self.trsr_resultnodelist = "CREATE TABLE if not exists public.\"TRSR_ResultNodeList\" \
        (                   \
          searchid integer, \
          nodeid1 integer, nodeid2  integer, nodeid3  integer, nodeid4 integer, nodeid5  integer, \
          nodeid6 integer, nodeid7  integer, nodeid8  integer, nodeid9 integer, nodeid10 integer, \
          nodeid11 integer,nodeid12 integer, nodeid13 integer, nodeid14 integer,nodeid15 integer, \
          nodeid16 integer,nodeid17 integer, nodeid18 integer, nodeid19 integer,nodeid20 integer, \
          nodeid21 integer,nodeid22 integer, nodeid23 integer, nodeid24 integer,nodeid25 integer, \
          nodeid26 integer,nodeid27 integer, nodeid28 integer, nodeid29 integer,nodeid30 integer, \
          nodeid31 integer,nodeid32 integer, nodeid33 integer, nodeid34 integer,nodeid35 integer, \
          nodeid36 integer,nodeid37 integer, nodeid38 integer, nodeid39 integer,nodeid40 integer, \
          nodeid41 integer,nodeid42 integer, nodeid43 integer, nodeid44 integer,nodeid45 integer, \
          nodeid46 integer,nodeid47 integer, nodeid48 integer, nodeid49 integer,nodeid50 integer  \
        )                                          \
        WITH (OIDS=FALSE);                         \
        ALTER TABLE public.\"TRSR_ResultNodeList\" OWNER TO postgres;                          \
        COMMENT ON  TABLE public.\"TRSR_ResultNodeList\" IS \'stores the result of searches\'; \
        COMMENT ON COLUMN public.\"TRSR_ResultNodeList\".searchid IS \'ID of the search \';    \
        COMMENT ON COLUMN public.\"TRSR_ResultNodeList\".nodeid1  IS \'first node\'; "

        self.trsr_searchchaincross = "CREATE TABLE if not exists public.\"TRSR_SearchChainCross\"   \
        (searchid integer,  chainid integer)                                                   \
        WITH (OIDS=FALSE);                                                                     \
        ALTER TABLE public.\"TRSR_SearchChainCross\" OWNER TO postgres;                        \
        COMMENT ON  TABLE public.\"TRSR_SearchChainCross\" IS \'cross link searches and chains\';\
        COMMENT ON COLUMN public.\"TRSR_SearchChainCross\".searchid IS \'ID of a search\';       \
        COMMENT ON COLUMN public.\"TRSR_SearchChainCross\".chainid IS \'ID of a chain\'; "


class Tables_TRS:
    def __init__(self):

        self.trs_condcross = "CREATE TABLE if not exists public.\"TRS_CondCross\"    \
        (searchid text, searchconditionid integer)                               \
        WITH (OIDS=FALSE);                                                       \
        ALTER TABLE public.\"TRS_CondCross\" OWNER TO postgres;                  \
        COMMENT ON COLUMN public.\"TRS_CondCross\".searchid IS \'SearchID is the ID of the search\';\
        COMMENT ON COLUMN public.\"TRS_CondCross\".searchconditionid IS \'ID of the condition\';"

        self.trs_condition = "CREATE TABLE if not exists public.\"TRS_Condition\"   \
        ( searchconditionid integer,     \
          searchconditiontype text,      \
          searchconditionname text,      \
          searchconditionvaluetype text, \
          searchconditionvalue text)     \
        WITH (OIDS=FALSE);               \
        ALTER TABLE public.\"TRS_Condition\" OWNER TO postgres; \
        COMMENT ON TABLE public.\"TRS_Condition\"               \
          IS \'contains info of search conditions.\';           \
        COMMENT ON COLUMN public.\"TRS_Condition\".searchconditionid    IS \'ID of the condition\';  \
        COMMENT ON COLUMN public.\"TRS_Condition\".searchconditiontype  IS \'type of the condition\';\
        COMMENT ON COLUMN public.\"TRS_Condition\".searchconditionname  IS \'name of the confition\';\
        COMMENT ON COLUMN public.\"TRS_Condition\".searchconditionvaluetype IS \'type of the value\';\
        COMMENT ON COLUMN public.\"TRS_Condition\".searchconditionvalue IS \'value in condition.\';"

        self.trs_searchhead = "CREATE TABLE if not exists public.\"TRS_SearchHead\" \
        ( searchid text,        \
          startitemid1 integer, \
          startitemid2 integer, \
          starttype1 text,      \
          starttype2 text,      \
          searchuser text,      \
          starttime timestamp without time zone, \
          endtime text)         \
        WITH (OIDS=FALSE);      \
        ALTER TABLE public.\"TRS_SearchHead\" OWNER TO postgres; \
        COMMENT ON TABLE public.\"TRS_SearchHead\"               \
          IS \'info for search actions\';                        \
        COMMENT ON COLUMN public.\"TRS_SearchHead\".searchid IS \'globally unique ID of a search\';\
        COMMENT ON COLUMN public.\"TRS_SearchHead\".startitemid1 IS \'NodeID of the node\';\
        COMMENT ON COLUMN public.\"TRS_SearchHead\".startitemid2 IS \'odeID of the node    \
        A search can be constrainted on two ends.\';                                       \
        COMMENT ON COLUMN public.\"TRS_SearchHead\".starttype1 IS \'type of StartItemID1\';        \
        COMMENT ON COLUMN public.\"TRS_SearchHead\".starttype2 IS \'type of StartItemID2\';        \
        COMMENT ON COLUMN public.\"TRS_SearchHead\".searchuser IS \'user who started the search\'; \
        COMMENT ON COLUMN public.\"TRS_SearchHead\".starttime IS \'start time of the search\';     \
        COMMENT ON COLUMN public.\"TRS_SearchHead\".endtime IS \'end time of the search\';"

        self.trs_startitem = "CREATE TABLE if not exists public.\"TRS_StartItem\"   \
        ( startitemid integer,   \
          server text,           \
          dbid integer,          \
          columnid integer,      \
          value text,            \
          path text,             \
          filename text,         \
          logicblock text)       \
        WITH (OIDS=FALSE);       \
        ALTER TABLE public.\"TRS_StartItem\" OWNER TO postgres;                           \
        COMMENT ON TABLE public.\"TRS_StartItem\" IS \'start item of the search.          \
                             start items are the physical locations of the system\';      \
        COMMENT ON COLUMN public.\"TRS_StartItem\".startitemid IS \'ID of the start item\';          \
        COMMENT ON COLUMN public.\"TRS_StartItem\".server      IS \'IP address or DNS nm of server\';\
        COMMENT ON COLUMN public.\"TRS_StartItem\".dbid        IS \'ID of the database\';            \
        COMMENT ON COLUMN public.\"TRS_StartItem\".columnid    IS \'ID of the column\';              \
        COMMENT ON COLUMN public.\"TRS_StartItem\".value       IS \'Value of the start item\';       \
        COMMENT ON COLUMN public.\"TRS_StartItem\".path        IS \'path to the start item.\';       \
        COMMENT ON COLUMN public.\"TRS_StartItem\".filename    IS \'name of the file\';              \
        COMMENT ON COLUMN public.\"TRS_StartItem\".logicblock  IS \'a subsection in the file\'; "


class Tables_TRT:
        def __init__(self):

            self.trt_categoryassoc = "CREATE TABLE if not exists public.\"TRT_CategoryAssoc\"           \
            (cmmncategoryid integer, techcategoryid integer, catechassocstrength double precision) \
            WITH (OIDS=FALSE);                                          \
            ALTER TABLE public.\"TRT_CategoryAssoc\" OWNER TO postgres; \
            COMMENT ON TABLE public.\"TRT_CategoryAssoc\"               \
              IS \'association (linkage) info between common categories and tech categories.\';   \
            COMMENT ON COLUMN public.\"TRT_CategoryAssoc\".cmmncategoryid IS \'common category\'; \
            COMMENT ON COLUMN public.\"TRT_CategoryAssoc\".techcategoryid IS \'tech category\';   \
            COMMENT ON COLUMN public.\"TRT_CategoryAssoc\".catechassocstrength IS \'level of assoc\';"

            self.trt_categorycommon = "CREATE TABLE if not exists public.\"TRT_CategoryCommon\"  \
            (cmmncategoryid integer, cmmncategory text, lastupdateownerid integer,          \
             lastupdate timestamp without time zone)                     \
            WITH (OIDS=FALSE);                                           \
            ALTER TABLE public.\"TRT_CategoryCommon\" OWNER TO postgres; \
            COMMENT ON TABLE public.\"TRT_CategoryCommon\"               \
              IS \'common categories. Common Categories are categories that displayble to users.\';  \
            COMMENT ON COLUMN public.\"TRT_CategoryCommon\".cmmncategoryid    IS \'common category\';\
            COMMENT ON COLUMN public.\"TRT_CategoryCommon\".cmmncategory      IS \'common category\';\
            COMMENT ON COLUMN public.\"TRT_CategoryCommon\".lastupdateownerid IS \'ID of the owner\';\
            COMMENT ON COLUMN public.\"TRT_CategoryCommon\".lastupdate        IS \'date last update\';"

            self.trt_categorycommonhistory="CREATE TABLE if not exists public.\"TRT_CategoryCommonHistory\"\
            (cmmncategoryid integer, cmmncategory text, updateownerid integer,  \
             update timestamp without time zone)                                \
            WITH (OIDS=FALSE);                                                  \
            ALTER TABLE public.\"TRT_CategoryCommonHistory\" OWNER TO postgres; \
            COMMENT ON TABLE public.\"TRT_CategoryCommonHistory\"               \
              IS \'TRT_CategoryCommonHistory  is the history table of TRT_CategoryCommon table.       \
                 Each time a row in TRT_CategoryCommon is created updated, a new row in this table.\';\
            COMMENT ON COLUMN public.\"TRT_CategoryCommonHistory\".cmmncategoryid IS \'cmmn categ\';  \
            COMMENT ON COLUMN public.\"TRT_CategoryCommonHistory\".cmmncategory   IS \'cmmn categ\';  \
            COMMENT ON COLUMN public.\"TRT_CategoryCommonHistory\".updateownerid  IS \'ID of owner\'; \
            COMMENT ON COLUMN public.\"TRT_CategoryCommonHistory\".update         IS \'date last up\';"

            self.trt_categorytech = "CREATE TABLE if not exists public.\"TRT_CategoryTech\"   \
            (techcategoryid integer, techcategory text, lastupdateownerid integer, \
             lastupdate timestamp without time zone)                               \
            WITH (OIDS=FALSE);                                           \
            ALTER TABLE public.\"TRT_CategoryTech\" OWNER TO postgres;   \
            COMMENT ON TABLE public.\"TRT_CategoryTech\"                 \
              IS \'TRT_CategoryTech  stores a list of tech categories\'; \
            COMMENT ON COLUMN public.\"TRT_CategoryTech\".techcategoryid    IS \'Tech Category\';   \
            COMMENT ON COLUMN public.\"TRT_CategoryTech\".techcategory      IS \'tech category\';   \
            COMMENT ON COLUMN public.\"TRT_CategoryTech\".lastupdateownerid IS \'ID of the owner\'; \
            COMMENT ON COLUMN public.\"TRT_CategoryTech\".lastupdate        IS \'date last update\';"

            self.trt_categorytechhistory = "CREATE TABLE if not exists public.\"TRT_CategoryTechHistory\"  \
            (techcategoryid integer, techcategory text, updateownerid integer, \
             update timestamp without time zone)                               \
            WITH (OIDS=FALSE);                                                 \
            ALTER TABLE public.\"TRT_CategoryTechHistory\" OWNER TO postgres;  \
            COMMENT ON TABLE public.\"TRT_CategoryTechHistory\"                \
              IS \'TRT_CategoryTechHistory is the history table of TRT_CategoryTech table.    \
                  Each insert update in TRT_Category, a new row inserted into history table\';\
            COMMENT ON COLUMN public.\"TRT_CategoryTechHistory\".techcategoryid IS \'Tech Category\';\
            COMMENT ON COLUMN public.\"TRT_CategoryTechHistory\".techcategory   IS \'Tech category\';\
            COMMENT ON COLUMN public.\"TRT_CategoryTechHistory\".updateownerid  IS \'ID of owner\';  \
            COMMENT ON COLUMN public.\"TRT_CategoryTechHistory\".update         IS \'date last upd\';"

            self.trt_commonterm = "CREATE TABLE if not exists public.\"TRT_CommonTerm\"  \
            (cmmntermid integer, cmmnterm text, cmmncategoryid integer,    \
             caassocstrength double precision, parenttermid1 integer,      \
             parenttermid2 integer, assoctermid3 integer,                  \
             assocstrength3 double precision, assoctermid4 integer, assocstrength4 double precision) \
            WITH (OIDS=FALSE);                                       \
            ALTER TABLE public.\"TRT_CommonTerm\" OWNER TO postgres; \
            COMMENT ON TABLE public.\"TRT_CommonTerm\"               \
              IS \'TRT_CommonTerm table stores common terms\';       \
            COMMENT ON COLUMN public.\"TRT_CommonTerm\".cmmntermid      IS \'ID common term\';       \
            COMMENT ON COLUMN public.\"TRT_CommonTerm\".cmmnterm        IS \'Desc common term\';     \
            COMMENT ON COLUMN public.\"TRT_CommonTerm\".cmmncategoryid  IS \'common category\';\
            COMMENT ON COLUMN public.\"TRT_CommonTerm\".caassocstrength IS \'strength assoc betweeen \
                             common category and common terms. sum up to 1\';                        \
            COMMENT ON COLUMN public.\"TRT_CommonTerm\".parenttermid1   IS \'ID parent common term\';\
            COMMENT ON COLUMN public.\"TRT_CommonTerm\".parenttermid2   IS \'ID parent common term\';\
            COMMENT ON COLUMN public.\"TRT_CommonTerm\".assoctermid3    IS \'ID assoc common term\'; \
            COMMENT ON COLUMN public.\"TRT_CommonTerm\".assocstrength3  IS \'strength AssocTerm3\';  \
            COMMENT ON COLUMN public.\"TRT_CommonTerm\".assoctermid4    IS \'ID assoc common term\'; \
            COMMENT ON COLUMN public.\"TRT_CommonTerm\".assocstrength4  IS \'assoc AssocTermID4\';"

            self.trt_commontermassoc = "CREATE TABLE if not exists public.\"TRT_CommonTermAssoc\"     \
            ( cmmntermid1 integer,                    \
              cmmntermid2 integer,                    \
              ccassocstrength double precision,       \
              clustercenterid1 integer,               \
              clustercenterid2 integer,               \
              thresholddirectlink double precision,   \
              thresholdrelated double precision)      \
            WITH (OIDS=FALSE);                        \
            ALTER TABLE public.\"TRT_CommonTermAssoc\" OWNER TO postgres;  \
            COMMENT ON TABLE public.\"TRT_CommonTermAssoc\"                \
            IS \'TRT_CommonTermAssoc  stores the relationship among common terms\';                  \
            COMMENT ON COLUMN public.\"TRT_CommonTermAssoc\".cmmntermid1      IS \'ID common term1\';\
            COMMENT ON COLUMN public.\"TRT_CommonTermAssoc\".cmmntermid2      IS \'ID common term2\';\
            COMMENT ON COLUMN public.\"TRT_CommonTermAssoc\".ccassocstrength  IS \'cmmn-cmmn assoc\';\
            COMMENT ON COLUMN public.\"TRT_CommonTermAssoc\".clustercenterid1 IS \'ID common term \';\
            COMMENT ON COLUMN public.\"TRT_CommonTermAssoc\".clustercenterid2 IS \'ID common term \';\
            COMMENT ON COLUMN public.\"TRT_CommonTermAssoc\".thresholddirectlink IS \'threshold   \';\
            COMMENT ON COLUMN public.\"TRT_CommonTermAssoc\".thresholdrelated IS \'threshold \';"

            self.trt_owner = "CREATE TABLE if not exists public.\"TRT_Owner\"    \
            (ownerid integer, ownername text, ownerdept text, createdate timestamp without time zone)\
            WITH (OIDS=FALSE);                                     \
            ALTER TABLE public.\"TRT_Owner\" OWNER TO postgres;    \
            COMMENT ON TABLE public.\"TRT_Owner\"                  \
              IS \'TRT_Owner stores owner who create categories\'; \
            COMMENT ON COLUMN public.\"TRT_Owner\".ownerid    IS \'ID of the owner\';     \
            COMMENT ON COLUMN public.\"TRT_Owner\".ownername  IS \'name of the owner\';   \
            COMMENT ON COLUMN public.\"TRT_Owner\".ownerdept  IS \'OwnerDepartment\';     \
            COMMENT ON COLUMN public.\"TRT_Owner\".createdate IS \'date that this owner is created\';"

            self.trt_techterm = "CREATE TABLE if not exists public.\"TRT_TechTerm\"    \
            ( techtermid integer,                \
              techterm text,                     \
              techcategoryid integer,            \
              caassocstrength double precision,  \
              parenttermid1 integer,             \
              parenttermid2 integer,             \
              assoctermid3 integer,              \
              assocstrength3 double precision,   \
              assoctermid4 integer,              \
              assocstrength4 double precision)   \
            WITH (OIDS=FALSE);                   \
            ALTER TABLE public.\"TRT_TechTerm\" OWNER TO postgres; \
            COMMENT ON TABLE public.\"TRT_TechTerm\" IS \'TRT_TechTerm stores tech terms\';          \
            COMMENT ON COLUMN public.\"TRT_TechTerm\".techtermid      IS \'ID of this tech term\';   \
            COMMENT ON COLUMN public.\"TRT_TechTerm\".techterm        IS \'desc of this tech term\'; \
            COMMENT ON COLUMN public.\"TRT_TechTerm\".techcategoryid  IS \'ID tech category\';       \
            COMMENT ON COLUMN public.\"TRT_TechTerm\".caassocstrength IS \'tech term to tech cat.\'; \
            COMMENT ON COLUMN public.\"TRT_TechTerm\".parenttermid1   IS \'ID parent tech term\';    \
            COMMENT ON COLUMN public.\"TRT_TechTerm\".parenttermid2   IS \'ID parent tech term\';    \
            COMMENT ON COLUMN public.\"TRT_TechTerm\".assoctermid3    IS \'ID associated tech term\';\
            COMMENT ON COLUMN public.\"TRT_TechTerm\".assocstrength3  IS \'strength of AssocTerm3\'; \
            COMMENT ON COLUMN public.\"TRT_TechTerm\".assoctermid4    IS \'ID associated tech term\';\
            COMMENT ON COLUMN public.\"TRT_TechTerm\".assocstrength4  IS \'strength of AssocTermID4\';"


# ------------------- Old tables --------------------------

class Tbls_db_sql:

    def __init__(self):
        self.db_table           = "create table if not exists trdb         (db_id int, dbname text, db_path text, port varchar(20), usr text, passwd text, update_dt timestamp default current_timestamp)"
        self.table_table        = "create table if not exists trtable      (table_id int, tablename text, db_id int, update_dt timestamp default current_timestamp)"
        self.column_table       = "create table if not exists trcolumn     (col_id int, colname text, datatype varchar(20), table_id int, db_id int, update_dt timestamp default current_timestamp)"
        self.tablerelate_table  = "create table if not exists trtablerelate(db_id int, table1_id int, col1_id int, table2_id int, col2_id int, relate varchar(20), update_dt timestamp default current_timestamp)"

        self.db_insert          = "insert into trdb         (dbname, db_path, port, usr, passwd) values (%s, %s, %d, %s, %s)"
        self.table_insert       = "insert into trtable      (tablename, db_id) values (%s, %d)"
        self.column_insert      = "insert into trcolumn     (colname, datatype, table_id, db_id) values (%s, %s, %d, %d)"
        self.tablerelate_insert = "insert into trtablerelate(db_id, table1_id, col1_id, table2_id, col2_id, relate) values (%d, %d, %d, %d, %d, %s)"

        self.db_update          = "update trdb     set dbname=%s, db_path=%s, port=%d, usr=%s, passwd=%s where db_id=%d"
        self.table_update       = "update trtable  set tablename=%s where table_id=%d and db_id=%d"
        self.column_update      = "update trcolumn set colname=%s, datatype=%s where col_id=%d and table_id=%d and db_id=%d"

        self.db_select          = "select db_id,    dbname, db_path, port, usr, passwd from trdb where dbname=%s"
        self.table_select       = "select table_id, tablename, db_id from trtable where tablename=%s"
        self.column_select      = "select col_id,   colname, datatype, table_id, db_id from trcolumn where colname=%d and table_id=%d and db_id=%d"
        self.tablerelate_select = "select db_id,    table1_id, col1_id, table2_id, col2_id, relate from trtablerelate where col1_id = %d, col2_id = %d "

        self.db_id_max          = "select  case when (select count(*) from trdb)>0     then max(db_id)+1    else 0 end as db_id    from trdb"
        self.table_id_max       = "select  case when (select count(*) from trtable)>0  then max(table_id)+1 else 0 end as table_id from trtable"
        self.col_id_max         = "select  case when (select count(*) from trcolumn)>0 then max(col_id)+1   else 0 end as col_id from trcolumn"


# ------------------- Node --------------------------

class TR_Node:
    def __init__(self):
        self.__node_info_col = ['nodeid','nodeparentid','linkmethod', 'node_type', 'fileid', 'file_obj',\
                                'lineoffsetinfile1', 'lineoffsetinfile2', 'lastupdate']
        self.__node_info     = []

    @property
    def node_info(self):
        return self.__node_info

    @node_info.setter
    def set_info(self, data):
        self.__node_info = data


class TR_File:
    def __init__(self):
        self._file_info_col = ['fileid','serverid','port', 'filepath', 'filetype', 'filename', \
                               'fileupdate','filecontent']
        self._file_info = []

    @property
    def file_info(self):
        return self._file_info

    @file_info.setter
    def set_info(self, data):
        self._file_info = data

class TR_Server:
    def __init__(self):
        self.__server_info_col = ['serverid','server']
        self.__server_info = []

    def set_info(self, data):
        self.__server_info = data

    @property
    def server_info(self):
        return self.__file_info


class NodeContentDecomp:

    def __init__(self):
        self.__nodecontent_info_col =['node_id','contenttype','content']
        self.__nodecontent_info = []

    def set_info(self, data):
        self.__nodecontent_info = data

    def nodecotent_info(self):
        return self.__nodecontent_info


class Tbls_node_sql:
    def __init__(self):
        self.node_table         = "create table if not exists trnode(node_id int, node_pid int, nodetype varchar(20), nodesubtype varchar(20), filesuffix varchar(20), nodename text, contentraw text, obj_update_dt timestamp ,update_dt timestamp default current_timestamp)"
        self.nodecontent_table  = "create table if not exists trnodecontentdecomp(node_id int, nodecontenttype varchar(20), content text, update_dt timestamp default current_timestamp)"

        self.node_insert        = "insert into trnode(node_id,node_pid, nodetype, nodesubtype, filesuffix, nodename, contentraw, obj_update_dt) values %s"
        self.nodecontent_insert = "insert into trnodecontentdecomp(node_id, nodecontenttype, content) values (%d, %s, %d)"

        self.node_select        = "select node_id, nodetype, nodesubtype, filesuffix, nodename, contentraw, update_dt, sql_id from trnode where node_id=%d "
        self.nodecontent_select = "select node_id, nodecontenttype, content from trnodecontent where node_id=%d"
        self.node_id_select     = "select node_id from trnode where nodename='%s'"

        self.node_update        = "update trnode set nodetype=%s, nodesubtype=%s, filesuffix=%s, nodename=%s, contentraw=%s, update_dt=%s, sql_id=%d where node_id=%d"
        self.nodecontent_update = "update trnodecontentdecomp set nodecontenttype=%s, content=%s where node_id=%d"

        self.node_id_max        = "select  case when (select count(*) from trnode)>0 then max(node_id)+1 else 0 end as node_id from trnode"

# -----------------------SQL ------------------------------

class SQL:

    def __init__(self):
        #autoincrement in DB,it is parent's select, from, join, where,[]  [ Column_, Column_, Column_ , ... ]
        #[] [ SQLSelect_, SQLSelect_, ... ],[ SQLFrom_, SQLFrom_, ... ],[ SQLJoin_, SQLJoin_, ... ],[] [ SQLWhere_, SQLWhere_, ... ], [] [TempTable, ... ]
        self.__sql_info_col =['sql_id','sql_pid','parent_relate','tableinsert_id',
                              'tableinsertcol_id','sqlselect','sqlfrom','sqljoin',
                              'sqlwhere','cte','sqlstmt','selectclause','fromclause',
                              'joinclause','whereclause','otherclause']
        self.__sql_info = []

    def set_info(self, data):
        self.__sql_info =data

    @property
    def sql_info(self):
        return self.__sql_info


class SQLSelect:

    def __init__(self):
        #name string of the to-be-insert table, same as source if no to-be-insert table
        #tbl_id of the to-be-insert table,               blank if no to-be-insert table
        #name string of the to-be-insert column,same as source if no to-be-insert table
        #col_id of the to-be-omsert column,              blank if no to-be-insert table
        self.__sqlselect_info_col =['table_id','col_id','target_col_id','value','sql_id','tblmapto_name','tblmapto_id','colmapto_name','colmapto_id']
        self.__sqlselect_info = []

    def set_info(self, data):
        self.__sqlselect_info= data

    @property
    def sqlselect_info(self):
        return self.__sqlselect_info


class SQLFrom:

    def __init__(self):
        #"from" type is the table type, could be dbtable, temp table, withtable
        self.__sqlfrom_info_col =['table_id','sql_id','from_type']
        self.__sqlfrom_info = []

    def set_info(self, data):
        self.__sqlfrom_info =data


    @property
    def sqlfrom_info(self):
        return self.__sqlfrom_info


class SQLJoin:

    def __init__(self):
        #join type is the table type, could be dbtable, temp table, withtable
        self.__sqljoin_info_col = ['table1_id','col1_id','value1','table2_id','col2_id','value2','sql_id','join_type']
        self.__sqljoin_info = []

    def set_info(self, data):
        self.__sqljoin_info = data

    @property
    def sqljoin_info(self):
        return self.__sqljoin_info


class SQLWhere:

    def __init__(self):
         # where type is the table type, could be dbtable, temp table, withtable
        self.__sqlwhere_info_col = ['table1_id','col1_id','value1','table2_id','col2_id','value2','sql_id','where_type']
        self.__sqlwhere_info = []

    def set_info(self, data):
        self.__sqlwhere_info = data

    @property
    def sqlwhere_info(self):
        return self.__sqlwhere_info


class Tbls_sql_sql:

    def __init__(self):
        self.sql_table        = "create table if not exists trsql      (sql_id    int, sql_pid int, parent_relate varchar(20), tableinsert_id int, sqlstmt text, selectclause text, fromclause text, joinclause text, whereclause text, otherclause text, update_dt timestamp default current_timestamp)"
        self.sqlselect_table  = "create table if not exists trsqlselect(table_id  int, col_id  int, value text, sql_id int, update_dt timestamp default current_timestamp)"
        self.sqlfrom_table    = "create table if not exists trsqlfrom  (table_id  int, sql_id  int, update_dt timestamp default current_timestamp)"
        self.sqljoin_table    = "create table if not exists trsqljoin  (table1_id int, col1_id int, value1 text, table2_id int, col2_id int, value2 text, sql_id int, update_dt timestamp default current_timestamp)"
        self.sqlwhere_table   = "create table if not exists trsqlwhere (table1_id int, col1_id int, value1 text, table2_id int, col2_id int, value2 text, sql_id int, update_dt timestamp default current_timestamp)"

        self.sql_update       = "update trsql       set sqlstmt = %s, selectclause = %s, fromclause = %s, joinclause = %s, whereclause = %s, otherclause = %s where sql_id = %d "
        self.sqlselect_update = "No need"
        self.sqlfrom_update   = "No need"
        self.sqljoin_update   = "No need"
        self.sqlwhere_update  = "No need"


        self.sql_select       = "select sql_id,    sql_pid, parent_relate, tableinsert_id, sqlstmt, selectclause, fromclause, joinclause, whereclause, otherclause from trsql where sql_id = %d "
        self.sqlselect_select = "select table_id,  col_id,  value, sql_id from trsqlselect where sql_id = %d "
        self.sqlfrom_select   = "select table_id,  sql_id   from trsqlfrom where sql_id = %d "
        self.sqljoin_select   = "select table1_id, col1_id, value1, table2_id, col2_id, value2, sql_id from  trsqljoin where sql_id = %d "
        self.sqlwhere_select  = "select table1_id, col1_id, value1, table2_id, col2_id, value2, sql_id from trsqlwhere where sql_id = %d "

        self.sql_id_max       = "select  case when (select count(*) from trsql)>0 then max(sql_id)+1 else 0 end as sql_id from trsql"

# -----------------------SQL vs Table ------------------------------

class TableColumn:

    def __init__(self):
        #from Database_,from Table_,from Column_
        self.__tablecolumn_info_col = ['db_id','table_id','col_id','value']
        self.__tablecolumn_info = []

    def set_info(self, data):
        self.__tablecolumn_info = data

    @property
    def tablecolumn_info(self):
        return self.__tablecolumn_info


class TabletoSQL:

    def __init__(self):
        # TableColumn_(),[ from SQL_ ... ]
        self.__tabletosql_info_col = ['col','sql_id']
        self.__tabletosql_info = []

    def set_info(self, data):
        self.__tabletosql_info = data

    @property
    def tabletosql_info(self):
        return self.__tabletosql_info


class SQLtoTable:

    def __init__(self):
        # from SQL_,[ TableColumn_, TableColumn_, ... ]
        self.__sqltotable_info_col = ['sql_id','cols']
        self.__sqltotable_info = []

    def set_info(self, data):
        self.__sqltotable_info = data

    @property
    def sqltotable_info(self):
        return self.__sqltotable_info


class Tbls_sqlvstable_sql:

    def __init__(self):
        self.sqlvstable_table         = "create table if not exists trsqlvstable(db_id int, table_id int, column_id int, sql_id int, update_dt timestamp default current_timestamp)"
        self.sqlvstable_insert        = "insert into trsqlvstable(db_id, table_id, column_id, sql_id) values (%d, %d, %d, %d) "

        self.sqlvstable_update_by_col = "update trsqlvstable set sql_id = %d where db_id = %d and table_id = %d and column_id = %d "
        self.sqlvstable_update_by_sql = "update trsqlvstable set db_id = %d, table_id = %d, column_id = %d where sql_id = %d "


# ----------------------- Travel ------------------------------

# query_tr_sql(table_name, OUT attrelid regclass, OUT attnum smallint, OUT attname name)
#
# query_tr_sql() is a stored function in postgresql, its content is:
#
# SELECT attrelid::regclass, attnum, attname        
# FROM   pg_attribute        
# WHERE  attrelid = table_name::regclass        
# AND    attnum > 0        
# AND    NOT attisdropped        
# ORDER  BY attnum;    



class TableInfo:
    def __init__(self):
        i = 1


    def table_info_(self, tablename, glo):

        # for getting column names
        query = "select * from query_tr_sql(\'public.\"" + tablename + "\"\')"

        try:
            cds = glo.dbserver_[0].sqlexec(query)
        except:
            cds = None

        return cds


# ----------------------- Search ------------------------------

class Project:

    def __init__(self):
        # autoincrement in DB,[]    [Case, Case, ... ]
        self.__project_info_col = ['project_id','project_name','cases']
        self.__project_info = []

    def set_info(self, data):
        self.__project_info = data

    @property
    def project_info(self):
        return self.__project_info


class Case:

    def __init__(self):
        # autoincrement in DB
        self.__case_info_col = ['case_id','case_name','project_id','searches']
        self.__case_info = []

    def set_info(self, data):
        self.__case_info = data

    @property
    def case_info(self):
        return self.__case_info


class Search:

    def __init__(self):
        #autoincrement, previous, related search,id of Case,[]   SearchCond,Node()
        self.__search_info_col = ['search_id','search_pid','searchtype','case_id','search_dt','searchcond','node_start']
        self.__search_info = []

    def set_info(self, data):
        self.__search_info = data

    @property
    def search_info(self):
        return self.__search_info


class SearchCond:

    def __init__(self):
        # id of Search,could be a 'pattern', 'callforward', 'callbackward','dataflowforward', 'dataflowbackward','system_id', whether his is a search condition or a display condition
        self.__searchcond_info_col = ['search_id','searchcond','searchcondtype']
        self.__searchcond_info = []

    def set_info(self, data):
        self.__searchcond_info = data

    @property
    def searchcond_info(self):
        return self.__searchcond_info


class SearchNode:

    def __init__(self):
        self.__searchnode_info_col = ['node_id','node_pre_id','search_id','sql_id','flow']
        self.__searchnode_info = []

    def set_info(self, data):
        self.__searchnode_info = data

    @property
    def searchnode_info(self):
        return self.__searchnode_info


class Tbl_search_sql:

    def __init__(self):
        self.searchproject_table   = "create table if not exists trsearchproject( project_id int, project_name text, update_dt timestamp default current_timestamp)"
        self.searchcase_table      = "create table if not exists trsearchcase   ( case_id    int, case_name text,    project_id int, update_dt timestamp default current_timestamp)"
        self.search_table          = "create table if not exists trsearch       ( search_id  int, search_pid int,    searchtype varchar(20), case_id int, search_dt text, update_dt timestamp default current_timestamp)"
        self.searchcond_table      = "create table if not exists trsearchcond   ( search_id  int, searchcond text,   update_dt timestamp default current_timestamp)"
        self.searchnode_table      = "create table if not exists trsearchnode   ( node_id    int, node_pre_id int,   search_id int, sql_id int, update_dt timestamp default current_timestamp)"

        self.searchproject_insert  = "insert into  trsearchproject( project_id, project_name) values (%d, %s) "
        self.searchcase_insert     = "insert into  trsearchcase   ( case_id, case_name, project_id) values (%d, %s, %d) "
        self.search_insert         = "insert into  trsearch       ( search_id, search_pid, searchtype, case_id, search_dt) values (%d, %d, %s, %d, %s) "
        self.searchcond_insert     = "insert into  trsearchcond   ( search_id, searchcond) values (%d, %s) "
        self.searchnode_insert     = "insert into  trsearchnode   ( node_id, node_pre_id, search_id, sql_id) values (%d, %d, %d, %d) "

        self.searchproject_select  = "select  project_id, project_name from trsearchproject where project_id = %d  "
        self.searchcase_select     = "select  case_id, case_name, project_id from trsearchcase where case_id = %d "
        self.search_select         = "select  search_id, search_pid, searchtype, case_id, search_dt from trsearch where search_id = %d "
        self.searchcond_select     = "select  search_id, searchcond from trsearchcond where search_id = %d "
        self.searchnode_select     = "select  node_id, node_pre_id, search_id, sql_id from  trsearchnode where node_id = %d "

        self.searchproject_update  = "update trsearchproject set project_name = %s where project_id = %s "
        self.searchcase_update     = "update trsearchcase    set case_name    = %s where case_id    = %d and project_id = %d "
        self.search_update         = "No need"
        self.searchcond_update     = "No need"
        self.searchnode_update     = "No need"

        self.project_id_max        = "select  case when (select count(*) from trsearchproject)>0 then max(project_id)+1 else 0 end as project_id from trsearchproject"
        self.case_id_max           = "select  case when (select count(*) from trsearchcase)>0 then max(case_id)+1 else 0 end as case_id from trsearchcase"
        self.search_id_max         = "select  case when (select count(*) from trsearch)>0 then max(search_id)+1 else 0 end as search_id from trsearch"
