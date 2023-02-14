#!/usr/bin/python


def val_quote_marked_(v):
    if (not (v[0] == "'" and v[len(v) - 1] == "'") and not (v[0] == '"' and v[len(v) - 1] == '"')):
        v = val_quote_marked2_(v)
    else:
        v2 = val_quote_marked2_(v[1:-1])
        v = v[0] + v2 + v[len(v)-1]
    return v


def val_quote_marked2_(v):
    v1 = v.replace("'", "####")
    v2 = v1.replace('"', 'xxxx')
    return v2


if __name__ == '__main__':
    v = "463,462,'file','sql',310,'ground',\"2016-08-26 11:12:16\""
    v = val_quote_marked_(v)
    print (v)