__author__ = 'Administrator'
import re

from trg.tool            import tree_strip
from trg.tool.tree_strip import tree_strip
from trg.sql_blocks.insert_table import InsertTable
from trg.sql_blocks.insert_value import Insert_Value


class Insert_Blocks:
    def __init__(self):
        self.insert_table = InsertTable()
        self.insert_value = Insert_Value()

    def insert_blocks_(self, statement, level, glo):
        tree1 = []
        # whole insert stmt .glo.sqlid --> sqlid_insert
        tree1.append([glo.sqlid, glo.sql_list_id, "", glo.offset, glo.offset + len(statement), \
                      "insert", "sql", statement, False, level, ""])
        glo.sqlid_insert = glo.sqlid
        glo.sqlid += 1
        level     += 1
        insert_type = ""
        matched_lst = []

        insert_select_ = re.compile(r'^(insert\s+into\s+)(\S+\s+)(select\s+.*)$')
        insert_sel   = insert_select_.match(statement)

        insert_param_select_ = re.compile(r'^(insert\s+into\s+)(\S+\s*)\(([\s*\S+\s*,|\s]*\S+\s*)\)\s+(select\s+.*)$')
        insert_param_sel = insert_param_select_.match(statement)

        insert_value   = re.compile(r'^(insert\s+into\s+)(\S+)\s+(values\s+(.*))$')
        insert_v = insert_value.match(statement)

        insert_param_value = re.compile(r'^(insert\s+into\s+)([\S|\s]+)\s*\(([\S+\s*,|\s]*\S+)\)\s+(values\s*(.*))$')
        insert_param_v = insert_param_value.match(statement)

        matched_lst = []
        param_      = ""
        if insert_sel:
            insert_type = "insert select"
            param_      = "none"
            matched_lst.append(insert_sel)
        elif insert_param_sel:
            insert_type = "insert select"
            param_      = "param"
            matched_lst.append(insert_param_sel)
        elif insert_v:
            insert_type = "insert value"
            param_      = "none"
            matched_lst.append(insert_v)
        elif insert_param_v:
            insert_type = "insert value"
            param_      = "param"
            matched_lst.append(insert_param_v)

        #print("insert_blocks.py,   statement=", statement)
        #print("insert_blocks.py,   matched_lst=", matched_lst)

        [list_pairs, select_sql] = self.decomp_(statement, param_, matched_lst, insert_type, level, glo)

        tree1.extend(list_pairs)
        tree_strip(tree1)
        return insert_type,  param_,  tree1,    select_sql

    def decomp_(self, statement, type_, matched_, insert_type, level, glo):
        list_pairs = []
        matched = matched_[0]
        ss        = matched.group(0)
        tablename = matched.group(2).strip()
        insert_tbl_sqlid = glo.sqlid
        le = ss[12:].find(tablename) + 12
        if type_=="none":
            ri = le + len(tablename) + 1
        else:
            ri = le + len(tablename)
        # sqlid_insert is the top SQLID of this insert sql
        block1 = [insert_tbl_sqlid, glo.sqlid_insert, "", glo.offset + le, glo.offset + ri, \
                  "insert", "table", tablename, False, level, ""]
        list_pairs.append(block1)
        glo.sqlid += 1

        if type_=="none":
            select_v  = matched.group(3)           # either select stmt or value clause
        elif type_ == "param":
            param_lst = matched.group(3).strip()
            select_v  = matched.group(4)
            le = ss.find(param_lst)
            ri = ss.find(select_v)
#            block_paramlist = [glo.sqlid, insert_tbl_sqlid, "", glo.offset + le, glo.offset + ri - 1,\
#                      "insert", "paramlist", param_lst, False, level, ""]
#            list_pairs.append(block_paramlist)
#            paramlist_sqlid = glo.sqlid
#            glo.sqlid += 1

            params = param_lst.split(",")
            i = 0
            for p in params:
                le1 = le + param_lst.find(p)
                ri  = le + param_lst.find(p) + len(p)
                p = p.strip(",")
                block_param = [glo.sqlid, insert_tbl_sqlid, "", glo.offset + le1, glo.offset + ri - 1, \
                               "insert", "param", p, False, level, str(i)]
                list_pairs.append(block_param)
                glo.sqlid += 1
                i += 1
            ri += 2

        glo.offset_select = ri  # insert into   table    select/value *****
        select_sql = ""
        self.insert_table.insert_table_(list_pairs, statement, insert_tbl_sqlid, tablename, level + 1, glo)

        if   insert_type == "insert select":
            select_sql = select_v
        elif insert_type == "insert value":
            insert_value_sqlid = glo.sqlid
            block2  = [insert_value_sqlid, glo.sqlid_insert, "", glo.offset + ri, glo.offset + ri + len(select_v), \
                       "insert", "value", select_v, False, level, ""]
            list_pairs.append(block2)
            glo.sqlid += 1
            glo.offset_select += len(select_v)
            self.insert_value.insert_value_(list_pairs,statement,insert_value_sqlid,select_v,level+1,glo)
        return list_pairs, select_sql
