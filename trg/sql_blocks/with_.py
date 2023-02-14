__author__ = 'Administrator'

from trg.sql_blocks.with_convert import With_Convert


class WithConvAll:
    def __init__(self):
        self.with_conv = With_Convert()

    def with_(self, sql_list1):
        sql_list2 = []
        for sql in sql_list1:                        # go through all sql statements
            if sql[1] == "with":                    # if it is a "with"
                with_selects = self.with_conv.with_convert_(sql[0])
                with_num_ = len(with_selects)
                i = 0
                for withsql in with_selects:
                    if i < with_num_ - 1:
                        sql_list2.append([withsql, "insert"])
                    else:
                        sql_list2.append([withsql, "select"])
                    i += 1
            else:
                sql_list2.append([sql[0], sql[1]])
        return sql_list2



