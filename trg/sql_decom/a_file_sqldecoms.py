__author__ = 'Administrator'
import re

from trg.sql_blocks.from_after_blocks  import From_After_Blocks
from trg.sql_blocks.join_on_blocks     import Join_On_Blocks
from trg.sql_blocks.conditions         import Conditions
from trg.sql_blocks.src_tables         import Src_Tables
from trg.sql_blocks.from_blocks        import From_Blocks
from trg.sql_blocks.insert_blocks      import Insert_Blocks
from trg.sql_blocks.select_blocks      import Select_Blocks
from trg.sql_blocks.select_from_blocks import Select_From_Blocks
from trg.sql_blocks.tracedecom_sql     import TraceDecomSQL
from trg.sql_blocks.union_blocks       import Union_Blocks
from trg.sql_blocks.level_adjust       import Level_Adjust
from trg.sql_blocks.with_              import WithConvAll
from trg.sql_blocks.select_into_convert import Select_Into
from trg.sql_blocks.sqls_semicolon_separated import SQLsSemiColonSeparated
from trg.tool.print_space_layout       import Print_Layout
from trg.tool.merge_sql                import Merge_SQLs


class SqlDecom:

    def __init__(self):
        self.select_into_pattern = re.compile("^(select)(.+)( into )([\w|\s]+)( from )(.+)")  # select ... into ..
        self.un           = Union_Blocks()
        self.sqls_separated = SQLsSemiColonSeparated()
        self.sf_block     = Select_From_Blocks()
        self.sblocks      = Select_Blocks()
        self.afblocks     = From_After_Blocks()
        self.jo_blocks    = Join_On_Blocks()
        self.conditions   = Conditions()
        self.srctables    = Src_Tables()
        self.fblocks      = From_Blocks()
        self.insert       = Insert_Blocks()
        self.level_adjust = Level_Adjust()
        self.trace_sql    = TraceDecomSQL()
        self.merge_sqls   = Merge_SQLs()
        self.with_conv_all= WithConvAll()
        self.select_into  = Select_Into()
        self.print_       = Print_Layout()

    def a_file_sqldecoms_(self, sql_, glo):                    # a sql file may have multiple sql statements
        sql__    = sql_.splitlines()
        sql      = ' '.join(sql__)
        self.sql = sql.strip().lower()
        sql_list = self.sqls_separated.identify_sql_list_(self.sql)
        sql_list = self.with_conv_all.with_(sql_list)
        whole_file_sqls = self.merge_sqls.merge_sqls_(sql_list)

        sql_list = self.sqls_separated.identify_sql_list_(whole_file_sqls)
        glo.offset = 0
        self.sql_file_id = glo.fileid       # file ID of the SQL file
#        glo.fileid += 1
        glo.sql_list_id = glo.sqlid         # SQL ID of the collection of all sqls in the file
        level = 0
        tree  = []
        # make the first block ...... the whole file
        len_ = len(whole_file_sqls)
        pair = [glo.sql_list_id, self.sql_file_id, "", 0, len_, "sql collection", "whole file sqls", \
                                                whole_file_sqls, False, level, ""]
        tree.append(pair)
        glo.sqlid += 1                      # sqlid of the first sql in the file, if only one sql, then, it
                                            # appears two level of the same sql stmt, i.e., glo.sqlid_p
                                            # and glo.sqlid are two blocks, contain the same sql stmt. That's OK
        # make all rest of the sql blocks, ssql means: single SQL

        lst_trees = []
        for sql__ in sql_list:
            ssql  = sql__[0]
            type_ = sql__[1]
            tree1 = self.each_sql_(whole_file_sqls, ssql, type_, level, glo)
            lst_trees.append(tree1)

        for tree_ssql in lst_trees:
            if tree_ssql:
                tree_ssql = self.duplicate_remove_(tree_ssql)
                tree_ssql = self.level_adjust.level_adjust_(tree_ssql, 1)
                tree_ssql = self.jo_blocks.join_on_blocks_(tree_ssql, glo)
                if not tree_ssql or type(tree_ssql) == type(""):
                    return tree_ssql
                tree_ssql = self.level_adjust.level_adjust_(tree_ssql, 1)
                tree_ssql = self.conditions.conditions_(tree_ssql, glo)
                tree_ssql = self.fblocks.from_cut_short_(tree_ssql)
                tree_ssql = self.srctables.sourcetbls_(tree_ssql, "from", glo)
                tree_ssql = self.srctables.sourcetbls_(tree_ssql, "join table", glo)

                # ------------------ store a single sql to database --------------------------

                tree_ssql = self.trace_sql.tracedecom_sql_(tree_ssql, glo)

                if type(tree_ssql) == type([]):
                    tree.extend(tree_ssql)
                else:
                    return tree_ssql

        return tree

    def each_sql_(self, whole_file_sqls, ssql, type_, level, glo): # for each sql ("with" are several sqls)
        level += 1                                                 #  level that available
        glo.offset = whole_file_sqls.find(ssql)
        glo.sqlid_p = glo.sql_list_id
        tree_ssql = []                                           # tree_ssql for all selects in this single sql

        if type_ == "insert":
            glo.sqlid_insert = glo.sqlid                         # first SQLID, for the entire insert stmt, available
            [insert_type_, param_, tree_ssql, query] = self.insert.insert_blocks_(ssql, level, glo)  # parent is sql list
            if insert_type_ == "insert select":
                level += 1
                glo.sqlid_p = glo.sqlid_insert                   # parent: "insert"
                tree_ssql = self.complex_selects_(tree_ssql, query, level, glo)

        if type_ == "select":
            select_into = self.select_into_pattern.search(ssql)
            if select_into:
                insert_sql = self.select_into.select_into_convert_(select_into)
                glo.sqlid_insert = glo.sqlid                    # first SQLID, for the entire insert stmt, available
                [in_type_, param_, tree_ssql, query] = self.insert.insert_blocks_(insert_sql, level, glo) # parent:sql list
                level += 1
                glo.sqlid_p = glo.sqlid_insert                                      # parent: "insert"
                tree_ssql = self.complex_selects_(tree_ssql, query, level, glo)
            else:
                glo.offset_select = 0
                query = ssql    # a straightforward select
                tree_ssql = self.complex_selects_(tree_ssql, query, level, glo)    # parent: sql list
        return tree_ssql

    # "select ..." may be several selects joined by union and ().  The whole select is a Node, made in the unionbloc
    def complex_selects_(self, tree_ssql, select_sql, level, glo):
        tree_union = self.select_stmt_whole_(select_sql, level, glo)          # a block for the entire select stmt
        level += 1                                                            # level that available
        union_paren_list = self.un.union_blocks_(select_sql, level, glo)      # may have unions and parens
        tree_union.extend(union_paren_list)                                   # at the beginning of union_blocks
        tree_details = []                                                     # glo.offset_select is the distance from
        for block in tree_union:                                             # insert to select
            if self.check_one_select__(tree_union, block):
                tree1 = self.select_sub_tree_(tree_union, block, level, glo)
                tree_details.extend(tree1)
        tree_ssql.extend(tree_details)
        return tree_ssql

    def select_stmt_whole_(self, select_sql, level, glo):
        pair = [glo.sqlid, glo.sqlid_p, "", \
                glo.offset + glo.offset_select, glo.offset + glo.offset_select + len(select_sql), \
                                                    "complex query", "query", select_sql, False, level, ""]
        glo.sqlid_p = glo.sqlid      # select stmt's SQLID is the parent SQLID for all below
        glo.sqlid += 1
        tree_union = []              # tree_union starts here (for the main "select" in each single query)
        tree_union.append(pair)
        return tree_union

    def check_one_select__(self, tree_union, block):
#        if block[6] == "union":
#            return True
        oneSelect = True
        if block[6] == "query" or block[6] == "parenthensis" or block[6] == "union" or block[5] == "select":
            for b in tree_union:
                if b[1] == block[0] and b[6] == "union":
                    oneSelect = False
                    break
            if oneSelect == True:
                ss = block[7].strip()
                select_pattern1_ = re.compile(r'^(select\s+)(.*)$')
                select_grps1 = select_pattern1_.match(ss)
                select_pattern2_ = re.compile(r'^(\(\s*select\s+)(.*)$')
                select_grps2 = select_pattern2_.match(ss)
                oneSelect = False
                if select_grps1:
                    oneSelect = True
                if select_grps2:
                    oneSelect = True
        return oneSelect

    def duplicate_remove_(self, tree):
        distincts = []
        for b in tree:
            if distincts.count(b) == 0:
                distincts.append(b)
        return distincts

    # it is executed for each block of the union_paren_tree, which is for a single complex query in sql_list
    def select_sub_tree_(self, tree_union, block, level, glo):   # no union, no inner parenthensis processed here
        glo.offset_select = block[3] - glo.offset    # block[7]'s offset to the beginning of the entire single sql
        # each complex select may have multiple blocks (one of parens or unions), block is one of them
        glo.sqlid_p = block[0]
        tree_select_from = self.sf_block.select_from_blocks_(tree_union, block, level, glo)
        tree_column  = self.sblocks.select_blocks_(tree_select_from, glo)
        tree_orderby = self.afblocks.from_after_blocks_(tree_column, block,  "order by", glo)
        tree_having  = self.afblocks.from_after_blocks_(tree_orderby, block, "having",   glo)
        tree_group   = self.afblocks.from_after_blocks_(tree_having, block,  "group by", glo)
        tree_where   = self.afblocks.from_after_blocks_(tree_group, block,   "where",    glo)
        tree_join    = self.afblocks.from_after_blocks_(tree_where, block,   "join",     glo)
        return tree_join
