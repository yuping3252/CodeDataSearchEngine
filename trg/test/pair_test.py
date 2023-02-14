__author__ = 'Administrator'
from trg.tool.lefts_rights import Lefts_Rights
from trg.tool.make_pairs   import Make_Pairs

def pair_test_(fromclause, le, ri):
    lefts_rights = Lefts_Rights()
    make_pairs   = Make_Pairs()

    [lefts,rights] = lefts_rights.get_lefts_rights_(fromclause, le, ri)
    pairlist   = make_pairs.make_pairs_(lefts, rights, 0)
    excludecandidates = []
    for pair in pairlist:
        excludecandidates.append([pair[3],pair[4]])
    sorted_ = sorted(excludecandidates)
    print sorted_
    blocks = [sorted_[0]]
    i = 0
    for b in sorted_:
        if blocks[i][1] < b[0]:
            blocks.append(b)
            i += 1
    print blocks


if __name__ == '__main__':
    fromclause = "1234(678(xxx)xxx)xxx(xx(x))xx"

    pair_test_(fromclause,"(", ")")




















