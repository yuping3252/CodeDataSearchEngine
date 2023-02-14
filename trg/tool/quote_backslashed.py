#!/usr/bin/python

def quote_backslashed_(v):
    if (not (v[0] == "'" and v[len(v) - 1] == "'") and not (v[0] == '"' and v[len(v) - 1] == '"')):
        v = quote_backslashed2_(v)
    else:
        v1 = quote_backslashed2_(v[1:-1])
        v = v[0] + v1 + v[len(v)-1]
    return v


def quote_backslashed2_(v):
    v1list = v.split("'")
    vlist = []
    for v1 in v1list:
        v2list = v1.split('"')
        vlist.extend(v2list)
    print ("quote_backslashed2_():  vlist=", vlist)

    accum = 0
    len_ = len(vlist)
    backslashedlist = [vlist[0]]
    for i in range(1, len_, 1):
        backslashedlist.append("####" + vlist[i])
        accum += len(vlist[i])
    backslashed = ''.join(backslashedlist)
    return backslashed

if __name__ == '__main__':
    v = "insert into public.\"TR_Node\" values (463,462,'file','sql',310,'ground','2016-08-26 11:12:16')"
    v = quote_backslashed_(v)
    print(v)