#!/usr/bin/python

from trg.tool.val_quote_marked import val_quote_marked_


def insert_stmt_val_quoted_(insert_stmt, values):

    # print("insert_stmt_val_quoted.py,   insert_stmt=", insert_stmt, "        values=", values)

    [v1, idx1] = val_to_list_(insert_stmt)
    quoted = ""
    i = 0
    for format in v1:
        if i > 0:
            quoted += ","
        if format.strip() == '%s':
            if values[i] =='':
                quoted += "''"
                i += 1
                continue
            v = str(values[i]).strip()
            
            if len(v) > 0:
                if (not (v[0] == "'" and v[len(v)-1] == "'") and not (v[0] == '"' and v[len(v)-1] == '"')):
                    v = val_quote_marked_(v)
                    quoted += "'" + v + "'"
                else:
                    v1 = val_quote_marked_(v[1:len(v)-1])
                    if v[0] == "'":
                        quoted += "'" + v1 + "'"
                    else:
                        quoted += '"' + v1 + '"'
            else:
                quoted += "'" + v + "'"
        else:
            quoted += str(values[i])

        i += 1
    insert_stmt_ = insert_stmt[:idx1] + "values (" + quoted + ")"
    return insert_stmt_


def val_to_list_(stmt):
    idx1 = stmt.index('values')
    v1   = stmt[idx1 + 6:]
    v1   = v1.strip('(').strip(')')
    v1   = v1.split(',')
    len_ = len(v1)
    for i in range(len_):
        v1[i] = v1[i].strip()
    return v1, idx1


if __name__=='__main__':
    s2 = [0, 3, 'xxx', 7, 13, "hellow", "tian"]
    insert_stmt = "insert into public.\"TR_Node\" values( %d, %d, %s, %d, %d, %s, %s)"
    insert_stmt_s2 = insert_stmt_val_quoted_(insert_stmt, s2)
    print ("insert_stmt_s2=", insert_stmt_s2)
