__author__ = 'Administrator'


class Level_Adjust:
    def __init__(self):
        self.seq = 0

    def level_adjust_(self, tree, level):
        partial_order  = self.partial_order_lists_(tree)
        lists_sorted   = self.partial_order_sort_(partial_order)
        lists_assigned = self.level_assign_(lists_sorted, level)
#        self.double_list_print2_(lists_assigned)
        tree = self.lists_merge_(lists_assigned)
        return tree

    def partial_order_lists_(self, tree):
        for b in tree:
            b[9] = -1
        partial_order_redundant = []
        for b in tree:
            if b[9] < 0:
                b_chain = []
                for b1 in tree:
                    if b1[9] < 0 and (b1[3] <= b[3] and b[4] < b1[4] or b1[3] < b[3] and b[4] <= b1[4]):
                        if b_chain.count(b1) == 0:
                            b_chain.append(b1)
                partial_order_redundant.append([b, b_chain])
        partial_order_index = []
        for p in partial_order_redundant:
            i = 0
            for p1 in partial_order_redundant:
                if p[1].count(p1[0]) > 0:
                    partial_order_index.append(i)
                i += 1
        partial_order = []
        len_ = len(partial_order_redundant)
        for i in range(len_):
            if partial_order_index.count(i) == 0:
                partial_order.append(partial_order_redundant[i])
        return partial_order

    # partial_order_redundant   each   [b,    [b, b, b, b, ...] ]

    def partial_order_sort_(self, partial_order):
        lists_sorted = []
        for pair in partial_order:
            plist = pair[1]
            plist.sort(key=lambda x:len(x[7]))
            plist.reverse()
            plist.append(pair[0])
            lists_sorted.append(plist)
            lists_sorted.sort(key=lambda x:len(x))
            lists_sorted.reverse()
        return lists_sorted

    # plist = [b, b, b, ...], each  [idx, idx_p, "", b[3], b[4], type, useas, content, False, level, "" ]
    # lists_sorted    [  plist, plist, plist, ...]

    def level_assign_(self, lists_sorted, level):
        for lst in lists_sorted:
            lvl = level
            for p in lst:
                if p[9] < 0:
                    p[9] = lvl
                lvl += 1
        return lists_sorted

    def lists_merge_(self, sorted_partial_order):
        tree = []
        for lst in sorted_partial_order:
            for b in lst:
                if tree.count(b) == 0:
                    tree.append(b)
        return tree

    def double_list_print1_(self, double_lst):
        for s in double_lst:
            for b in s[1]:
                print(b[0], b[1], " len=", b[4] - b[3], b[3], b[4], b[9], "||   ",)
            print (s[0],)
            print ("\n")

    def double_list_print2_(self, double_lst):
        for s in double_lst:
            for b in s:
                print (b[0], b[1], " len=", b[4] - b[3], b[3], b[4], b[9], "||   ",)
            print ("\n")

    def level_print_(self, tree):
        for b in tree:
            print (b)
