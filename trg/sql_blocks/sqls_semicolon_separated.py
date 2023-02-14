__author__ = 'Administrator'
import logging

from   trg.sql_blocks.identify_sql import IdentifySQL
from   trg.tool.lefts_rights       import Lefts_Rights
from   trg.tool.make_pairs         import Make_Pairs


class SQLsSemiColonSeparated:
    def __init__(self):
        self.lr = Lefts_Rights()
        self.mp = Make_Pairs()
        self.identify = IdentifySQL()

    def identify_sql_list_(self, content):
        semi_separate = content.split(';')
        len_ = len(semi_separate)
        for i in range(len_):
            semi_separate[i] = semi_separate[i] + ";"
        sql_types = []
        for semi1 in semi_separate:
            sql_type = self.identify.identify_sql_(semi1)
            if sql_type:
                sql_types.append(sql_type)
        return sql_types







