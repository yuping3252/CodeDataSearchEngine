__author__ = 'Administrator'
import re

from trg.tool             import block_strip
from trg.tool.block_strip import block_strip


class InsertTable:
    def __init__(self):
        self.seq = 0

    def insert_table_(self, list_pairs, statement, insert_tbl_sqlid, tbl_cols, level, glo):
        insert_table_offset = statement[12:].find(tbl_cols) + 12
        tbl_has_paren = re.compile(r'^(\S+)(\s*(.*))$')
        m_tbl_has_paren = tbl_has_paren.match(tbl_cols)
        le = glo.offset + insert_table_offset
        if m_tbl_has_paren.group(2).strip() != "":
            ri = glo.offset + insert_table_offset + len(m_tbl_has_paren.group(1))
            tbl_name = [glo.sqlid, insert_tbl_sqlid, "", \
                        le, ri, "table", "insert into", m_tbl_has_paren.group(1), False, level, ""]
            list_pairs.append(tbl_name)
            list_c_string = m_tbl_has_paren.group(2)
            list_c = list_c_string.split(",")
            base = glo.offset + insert_table_offset
            scope_le = 0
            scope_ri = len(tbl_cols)
            for c in list_c:
                le = tbl_cols[scope_le:scope_ri].find(c)
                ri = le + len(c)
                c_pair = [glo.sqlid, insert_tbl_sqlid, "",\
                          base + le, base + ri, "column", "insert column", c, False, level, ""]
                c_pair = block_strip(c_pair)
                list_pairs.append(c_pair)
                base     += ri
                scope_le += ri
                glo.sqlid += 1
        return list_pairs
