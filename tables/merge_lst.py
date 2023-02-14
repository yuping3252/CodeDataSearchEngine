import sys


class MergeList:

    def merge_lsts(self, t_lst1, c_lst1, t_lst2, c_lst2, c_nbr):
        if t_lst2 == []:
            t_headers = t_lst1
            c_headers = []
            for cols in c_lst1:
                for col in cols:
                    c_headers.append(col)
            col_grp_lst = c_lst1
            return t_headers, c_headers, col_grp_lst

        b_nbr, c_lst1_len = self.c_nbr_2_b_nbr(c_lst1, c_nbr)
        nbr,   c_lst2_len = self.c_nbr_2_b_nbr(c_lst2, 0)

        # ------------------ c_base: left position of table containing c_nbr
        b         = 0
        c_base    = 0
        for cols in c_lst1:
            if b == b_nbr:
                break
            b      += 1
            c_base += len(cols)

        # ------------------ c_lst1_restart: starting position to use c_lst1
        c_lst1_restart = c_nbr + c_lst2_len

        # ------------------ b_restart: starting index of table in c_lst1
        junk, b_restart = self.flatten_lst(c_lst1, c_lst1_restart)

        # ----------------------------- left part of c_lst1
        t_headers = self.left_t_headers(t_lst1, c_lst1, c_nbr)
        c_headers, junk = self.flatten_lst(c_lst1, c_nbr)
        col_grp_lst = self.left_col_grp_lst(c_lst1, c_nbr)

        # ----------------------------- mid part, c_lst2:
        b = 0
        for cols in c_lst2:
            t_headers.append(t_lst2[b])
            col_grp_lst.append(cols)
            for col in cols:
                c_headers.append(col)
            b += 1

        # ----------------------------- right part, c_lst1 again
        c = 0
        b = 0
        for cols in c_lst1:
            cols_ = []
            for col in cols:
                if c >= c_lst1_restart:
                    cols_.append(col)
                    c_headers.append(col)
                c += 1
            if len(cols_) > 0:
                t_headers.append(t_lst1[b])
                col_grp_lst.append(cols_)
            b += 1

        return t_headers, c_headers, col_grp_lst


    def left_t_headers(self, t_lst, c_lst, c_nbr):
        t_headers = []
        c = 0
        b = 0
        j = 0
        for cols in c_lst:
            has_column = 0
            for col in cols: 
                if c == c_nbr:
                    j = 1
                    break
                has_column = 1
                c += 1
            if has_column == 1: 
                t_headers.append(t_lst[b])
            if j == 1:
                break
            b += 1

        return t_headers


    def left_col_grp_lst(self, c_lst, c_nbr):
        grp_lst = []
        c = 0
        j = 0
        for cols in c_lst:
            c_left = c
            for col in cols:
                if c == c_nbr: 
                    j = 1
                    break
                c += 1
            if j == 1:
                if c_left == c: 
                    break
                else:
                    cols_ = []
                    for c_ in range(0, c - c_left):
                        cols_.append(cols[c_])
                    grp_lst.append(cols_)
                    break
            grp_lst.append(cols)
        return grp_lst


    # ----------------------------- b_nbr:   index of table containing column at position c_nbr
    def c_nbr_2_b_nbr(self, c_lst, c_nbr):
        b_nbr = 0
        c = 0
        b = 0
        for cols in c_lst:
            for col in cols:
                if c == c_nbr:
                    b_nbr = b
                c += 1
            b += 1
        return b_nbr, c


    def flatten_lst(self, c_lst, c_nbr):
        c = 0
        c_headers = []
        b = 0
        j = 0
        for cols in c_lst:
            for col in cols: 
                if c == c_nbr:
                    j = 1
                    break
                c_headers.append(col)
                c += 1
            if j == 1:
                break
            b += 1
        return c_headers, b


def main1(n):
    print(".......................... test ", n, "............................... head break, end whole, end < len1")

    tbl_lst1 = ['t1', 't2', 't3', 't4']
    col_lst1 = [['a1', 'a2'], ['b1', 'b2', 'b3', 'b4', 'b5'], ['c1', 'c2'], ['d1', 'd2']]
    tbl_lst2 = ['t11', 't22']
    col_lst2 = [['w6', 'w7'], ['u1', 'u2', 'u3', 'u4']]
    print("tbl_lst1=", tbl_lst1)
    print("col_lst1=", col_lst1)
    print("tbl_lst2=", tbl_lst2)
    print("col_lst2=", col_lst2)
    print("c_nbr=3")

    m = MergeList()
    tbl_merged, col_merged, col_lst3 = m.merge_lsts(tbl_lst1, col_lst1, tbl_lst2, col_lst2, 3)
    print("tbl_merged=", tbl_merged, ",      col_merged=", col_merged)
    print("3")
    print("")


def main2(n):
    print(".......................... test ", n, "............................... head break, end break, end < len1")

    tbl_lst1 = ['t1', 't2', 't3', 't4']
    col_lst1 = [['a1', 'a2'], ['b1', 'b2', 'b3', 'b4', 'b5'], ['c1', 'c2'], ['d1', 'd2']]
    tbl_lst2 = ['t11', 't22']
    col_lst2 = [['w6', 'w7'], ['u1', 'u2', 'u3']]
    print("tbl_lst1=", tbl_lst1)
    print("col_lst1=", col_lst1)
    print("tbl_lst2=", tbl_lst2)
    print("col_lst2=", col_lst2)
    print("3")

    m = MergeList()
    tbl_merged, col_merged, col_lst3 = m.merge_lsts(tbl_lst1, col_lst1, tbl_lst2, col_lst2, 3)


def main3(n):
    print(".......................... test ", n, "............................... head break, end = len1")

    tbl_lst1 = ['t1', 't2', 't3', 't4']
    col_lst1 = [['a1', 'a2'], ['b1', 'b2', 'b3', 'b4', 'b5'], ['c1', 'c2'], ['d1', 'd2']]
    tbl_lst2 = ['t11', 't22', 't33']
    col_lst2 = [['w6', 'w7'], ['u1', 'u2', 'u3', 'u4'], ['v1', 'v2']]
    print("tbl_lst1=", tbl_lst1)
    print("col_lst1=", col_lst1)
    print("tbl_lst2=", tbl_lst2)
    print("col_lst2=", col_lst2)
    print("3")
    print("")

    m = MergeList()
    tbl_merged, col_merged, col_lst3 = m.merge_lsts(tbl_lst1, col_lst1, tbl_lst2, col_lst2, 3)
    print("tbl_merged=", tbl_merged, ",      col_merged=", col_merged)
    print("")


def main4(n):
    print(".......................... test ", n, "............................... head break, end > len1")
    tbl_lst1 = ['t1', 't2', 't3', 't4']
    col_lst1 = [['a1', 'a2'], ['b1', 'b2', 'b3', 'b4', 'b5'], ['c1', 'c2'], ['d1', 'd2']]
    tbl_lst2 = ['t11', 't22', 't33']
    col_lst2 = [['w6', 'w7'], ['u1', 'u2', 'u3', 'u4'], ['v1', 'v2', 'v3', 'v4']]
    print("tbl_lst1=", tbl_lst1)
    print("col_lst1=", col_lst1)
    print("tbl_lst2=", tbl_lst2)
    print("col_lst2=", col_lst2)
    print("3")
    print("")

    m = MergeList()
    tbl_merged, col_merged, col_lst3 = m.merge_lsts(tbl_lst1, col_lst1, tbl_lst2, col_lst2, 3)
    print("tbl_merged=", tbl_merged, ",      col_merged=", col_merged)
    print("")



def main5(n):
    print(".......................... test ", n, "............................... head whole, end break, end < len1")

    tbl_lst1 = ['t1', 't2', 't3', 't4']
    col_lst1 = [['a1', 'a2'], ['b1', 'b2', 'b3', 'b4', 'b5'], ['c1', 'c2'], ['d1', 'd2']]
    tbl_lst2 = ['t11', 't22', 't33']
    col_lst2 = [['w6', 'w7'], ['u1', 'u2', 'u3', 'u4'], ['v1', 'v2']]
    print("tbl_lst1=", tbl_lst1)
    print("col_lst1=", col_lst1)
    print("tbl_lst2=", tbl_lst2)
    print("col_lst2=", col_lst2)
    print("2")
    print("")

    m = MergeList()
    tbl_merged, col_merged, col_lst3 = m.merge_lsts(tbl_lst1, col_lst1, tbl_lst2, col_lst2, 2)
    print("tbl_merged=", tbl_merged, ",      col_merged=", col_merged)
    print("")


def main6(n):
    print(".......................... test ", n, "............................... head whole, end whole, end < len1")

    tbl_lst1 = ['t1', 't2', 't3', 't4']
    col_lst1 = [['a1', 'a2'], ['b1', 'b2', 'b3', 'b4', 'b5'], ['c1', 'c2'], ['d1', 'd2']]
    tbl_lst2 = ['t11', 't22', 't33']
    col_lst2 = [['w6', 'w7'], ['u1', 'u2', 'u3', 'u4'], ['v1']]
    print("tbl_lst1=", tbl_lst1)
    print("col_lst1=", col_lst1)
    print("tbl_lst2=", tbl_lst2)
    print("col_lst2=", col_lst2)
    print("2")
    print("")

    m = MergeList()
    tbl_merged, col_merged, col_lst3 = m.merge_lsts(tbl_lst1, col_lst1, tbl_lst2, col_lst2, 2)
    print("tbl_merged=", tbl_merged, ",      col_merged=", col_merged)
    print("")


def main7(n):
    print(".......................... test ", n, "............................... head whole, end = len1")

    tbl_lst1 = ['t1', 't2', 't3', 't4']
    col_lst1 = [['a1', 'a2'], ['b1', 'b2', 'b3', 'b4', 'b5'], ['c1', 'c2'], ['d1', 'd2']]
    tbl_lst2 = ['t11', 't22', 't33']
    col_lst2 = [['w6', 'w7'], ['u1', 'u2', 'u3', 'u4'], ['v1', 'v2', 'v3']]
    print("tbl_lst1=", tbl_lst1)
    print("col_lst1=", col_lst1)
    print("tbl_lst2=", tbl_lst2)
    print("col_lst2=", col_lst2)
    print("2")
    print("")

    m = MergeList()
    tbl_merged, col_merged, col_lst3 = m.merge_lsts(tbl_lst1, col_lst1, tbl_lst2, col_lst2, 2)
    print("tbl_merged=", tbl_merged, ",      col_merged=", col_merged)
    print("")


def main8(n):
    print(".......................... test ", n, "............................... head whole, end > len1")

    tbl_lst1 = ['t1', 't2', 't3', 't4']
    col_lst1 = [['a1', 'a2'], ['b1', 'b2', 'b3', 'b4', 'b5'], ['c1', 'c2'], ['d1', 'd2']]
    tbl_lst2 = ['t11', 't22', 't33']
    col_lst2 = [['w6', 'w7'], ['u1', 'u2', 'u3'], ['v1']]
    print("tbl_lst1=", tbl_lst1)
    print("col_lst1=", col_lst1)
    print("tbl_lst2=", tbl_lst2)
    print("col_lst2=", col_lst2)
    print("2")
    print("")

    m = MergeList()
    tbl_merged, col_merged, col_lst3 = m.merge_lsts(tbl_lst1, col_lst1, tbl_lst2, col_lst2, 2)
    print("tbl_merged=", tbl_merged)
    print("col_merged=", col_merged)
    print("  col_lst3=", col_lst3)
    print("")


def main9(n):
    print(".......................... test ", n, "............................... head whole, end > len1")

    tbl_lst1 = ['t1', 't2', 't3', 't4']
    col_lst1 = [['a1', 'a2'], ['b1', 'b2'], [ 'b3', 'b4'], ['c1', 'c2']]
    tbl_lst2 = ['t1', 't2', 't33']
    col_lst2 = [['a1', 'a2'], ['b1', 'b2'], ['u1', 'u2', 'u3', 'u4', 'u5', 'u6']]
    print("-------------------------------------------------------")
    print("tbl_lst1=", tbl_lst1)
    print("col_lst1=", col_lst1)
    print("-------------------------------------------------------")
    print("tbl_lst2=", tbl_lst2)
    print("col_lst2=", col_lst2)
    print("c_lst2 start=", 2)

    m = MergeList()
    tbl_merged, col_merged, col_lst3 = m.merge_lsts(tbl_lst1, col_lst1, tbl_lst2, col_lst2, 2)
    print("tbl_merged=", tbl_merged)
    print("col_merged=", col_merged)
    print("  col_lst3=", col_lst3)
    print("2")
    print("")


def main10(n):
    print(".......................... test ", n, "............................... head whole, end > len1")

    tbl_lst1 = ['t1', 't2', 't3', 't4']
    col_lst1 = [['a1', 'a2'], ['b1', 'b2'], [ 'c1', 'c2', 'c3', 'c4', 'c5'], ['d1', 'd2']]
    tbl_lst2 = ['t2', 't4', 't3', 't']
    print("-------------------------------------------------------")
    col_lst2 = [['a1', 'a2'], ['b1', 'b2'], ['u1', 'u2', 'u3', 'u4', 'u5']]
    print("tbl_lst1=", tbl_lst1)
    print("col_lst1=", col_lst1)
    print("-------------------------------------------------------")
    print("tbl_lst2=", tbl_lst2)
    print("col_lst2=", col_lst2)
    print("3")
    print("")

    m = MergeList()
    tbl_merged, col_merged, col_lst3 = m.merge_lsts(tbl_lst1, col_lst1, tbl_lst2, col_lst2, 3)
    print("    tbl_merged=", tbl_merged)
    print("    col_merged=", col_merged)
    print("      col_lst3=", col_lst3)
    print("")


if __name__ == "__main__":
#    main1(1)
#    main2(2)
#    main3(3)
#    main4(4)
#    main5(5)
#    main6(6)
#    main7(7)
#    main8(8)
#    main9(9)
    main10(10)




