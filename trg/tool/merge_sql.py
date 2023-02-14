__author__ = 'Administrator'


class Merge_SQLs:
    def __init__(self):
        seq = 0

    def merge_sqls_(self, sql_list):
        whole_file_sql = ""
        for b in sql_list:
            b[0] = b[0].strip()
            if b[0][len(b[0])-1] == ";":
                whole_file_sql += b[0] + " "
            else:
                whole_file_sql += b[0] + "; "
        whole_file_sql = whole_file_sql.strip().replace('\t', ' ').replace('   ',' ').replace('  ', ' ')
        return whole_file_sql