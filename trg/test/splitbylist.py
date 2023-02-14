
# top_blocks that within a string
def splitbylist_(stringsss, top_commas):
    sss = stringsss
    segments = []
    if len(top_commas) >= 1:
        last_c = 0
        for c in top_commas:
            segments.append(sss[last_c:c])
            last_c = c
        segments.append(sss[last_c:len(stringsss)])
    return segments

if __name__ == '__main__':
    s = "from (select c31 from t31,t32 where t31.c = t32.c ) t3, ( select c42 from t42 ) t4"
    blocks = [[5, 50], [56, 78]]
    top_commas = [54]
    segments = splitbylist_(s, top_commas)
    print segments




















