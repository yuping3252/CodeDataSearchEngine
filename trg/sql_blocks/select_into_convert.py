__author__ = 'Administrator'


class Select_Into:
    def __init__(self):
        seq = 0

    def select_into_convert_(self, regx_result):
        column_strs = regx_result.group(2)
        target_table = regx_result.group(4)
        source_table = regx_result.group(6)
        # translate select ... into ... from ...       -->  ... select ... from ...  sql_tool
        #           (  1) ( 2 )(3 )(4 )(5) ( 6   )
        simple_cols = self.simple_columns_(column_strs)
        insert_sql = 'insert into ' + target_table + '(' + simple_cols + ')'
        select_sql = "select " + column_strs + ' from ' + source_table
        whole_sql = insert_sql + " " + select_sql
        return whole_sql

    def simple_columns_(self, column_str):
        cnt = column_str.count(",")
        simple_cols = ""
        for i in range(cnt):
            simple_cols += "c" + str(i) + ", "
        simple_cols = simple_cols[:len(simple_cols)-2]
        return simple_cols


