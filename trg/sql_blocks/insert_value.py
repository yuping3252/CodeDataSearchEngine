__author__ = 'Administrator'
import re

from trg.tool             import block_strip
from trg.tool.block_strip import block_strip


class Insert_Value:
    def __init__(self):
        self.seq = 0

    def insert_value_(self, list_pairs, statement, insert_value_sqlid, values, level, glo):
        insert_value_offset = statement.find(values)
        value_paren = re.compile(r'^(values\s*)((.*))[\s*|;]$')
        m_value_paren = value_paren.match(values)
        if m_value_paren:
            value_string = re.compile(r'^(\()(.*)(\))$')
            m_v_string = value_string.match(m_value_paren.group(2))
            list_v_string = m_v_string.group(2)
            list_v = list_v_string.split(",")
            base = glo.offset + insert_value_offset
            scope_le = 0
            scope_ri = len(values)
            for v in list_v:
                le = values[scope_le:scope_ri].find(v)
                ri = le + len(v)
                v_pair = [glo.sqlid, insert_value_sqlid, "",\
                          base + le, base + ri, "value", "insert value", v, False, level, ""]
                v_pair = block_strip(v_pair)
                list_pairs.append(v_pair)
                base     += ri
                scope_le += ri
                glo.sqlid += 1
        else:
            print("insert_value.py,   values=", values, "............. no match")
        return list_pairs
