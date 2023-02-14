#!/usr/bin/python

import zipfile


def valueclause_quote_string_(insert_stmt, values):
    idx1 = insert_stmt.index('values')
    v1 = insert_stmt[idx1 + 6:]
    v1 = v1.strip('(').strip(')')
    v1 = v1.split(',')
    s2 = insert_stmt % tuple(values)
    idx2 = s2.index('values')
    v2 = s2[idx2 + 6:]
    v2 = v2.strip('(').strip(')')
    v2 = v2.split(',')
    i = 0
    len_ = len(v1)
    for i in range(len_):
        v1[i] = v1[i].strip()
        v2[i] = v2[i].strip()
        i += 1
    sss = ""
    i = 0
    for format in v1:
        if i > 0:
            sss += ","
        print "format=", format
        if format.strip() == '%s':
            sss += "'" + v2[i] + "'"
        else:
            sss += v2[i]
        i += 1
    insert_stmt_ = insert_stmt[:idx1] + "values (" + sss + ")"
    return insert_stmt_





if __name__=='__main__':
    s2 = [0, 3, 'xxx', 7, 13, "hellow", "tian"]
    insert_stmt = "insert into public.\"TR_Node\" values( %d, %d, %s, %d, %d, %s, %s)"
    insert_stmt_s2 = valueclause_quote_string_(insert_stmt, s2)
    print "insert_stmt_s2=", insert_stmt_s2