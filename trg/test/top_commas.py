from trg.tool.top_blocks   import Top_Blocks


def top_commas_(stringsss, le, ri):
    top_blocks = Top_Blocks()
    top_blocks = top_blocks.top_blocks_(stringsss, le, ri)
    print "top_blocks=", top_blocks
    cnt = stringsss.count(",")
    sss = stringsss
    base = 0
    commas = []
    for i in range(cnt):
        idx1 = sss.find(",")
        commas.append(base + idx1)
        sss = sss[idx1+1:]
        base += idx1+1
    print "commas=", commas
    top_commas = []
    for c in commas:
        top_comma = True
        for b in top_blocks:
            if b[0] < c and c < b[1]:
                top_comma = False
                break
        if top_comma == True:
            top_commas.append(c)
    return top_commas

if __name__ == '__main__':
    fromclause = "0123(567,(012)456)89,12(4, 7(9))23"

    top_commas_ = top_commas_(fromclause,"(", ")")
    print top_commas_




















