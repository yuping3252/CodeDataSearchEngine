__author__ = 'Administrator'

from trg.tool.lefts_rights     import Lefts_Rights
from trg.tool.list_add_num     import list_add_num_

class With_Convert:
    def __init__(self):
        self.left_right = Lefts_Rights()

    def with_convert_(self, sql_):
        [sql, with_p, as_p, with_name] = self.with_first_name_(sql_)
        with_pairs   = self.with_pairs_(sql, with_p, as_p)
        with_statems = self.with_statems_(sql, with_pairs)
        insert_statems = self.with_insert_tmptbl_(with_statems)
        return insert_statems

    def with_first_name_(self, sql_):
        sql = sql_.lower().strip()
        with_p = sql.find("with ")
        as_p   = sql.find(" as ")
        with_name = sql[with_p + 5:as_p].strip()
        return sql, with_p, as_p, with_name

    def with_pairs_(self, sql, with_p, as_p):
        # remove with xxxxx --in the --> with xxxxx as ( sql )
        [left1, right1] = self.left_right.get_lefts_rights_(sql, "(", ")")
        right1 = list_add_num_(right1, 1)
        left2  = []
        right2 = []
        for le in left1:
            if le > as_p:
                left2.append(le)
        for ri in right1:
            if ri > as_p:
                right2.append(ri)

        # get all "select" positions
        cnt_s = sql.count("select")
        ss = sql
        select_locs = []
        base = 0
        for i in range(cnt_s):
            p = ss.find("select")
            if p > as_p:
                select_locs.append(base + p)
            ss = ss[p + 1:]
            base += p + 1

        # get numbers of parenthenses
        cnt_le = len(left2)
        cnt_ri = len(right2)

        # match pairs of "(" and ")"
        parenpairs = []
        for i in range(cnt_le):
            le = left2.pop()
            pair = []
            for j in range(cnt_ri):
                if le < right2[j]:
                    ri = right2[j]
                    right2.remove(right2[j])
                    pair = [le, ri]
                    break
            parenpairs.append(pair)
        parenpairs.reverse()

        # only keep those top parenthenses
        cnt_pairs = len(parenpairs)
        top_parenpairs = []
        for i in range(cnt_pairs):
            if i == 0:
                pair = parenpairs[0]
                top_parenpairs.append(pair)
            else:
                pair = parenpairs[i]
                top_ = True
                for m in parenpairs:
                    if m[0] < pair[0] and pair[1] < m[1]:
                        top_ = False
                if top_ and lastpair[1] < pair[0]:
                    top_parenpairs.append(pair)
            lastpair = pair

        with_pairs_ = []
        for b in top_parenpairs:
            if b[0] > 20:
                le = b[0] - 20
            else:
                le = 0
            as_p = -1
            for p in range(b[0] - 4, le, -1):
                if sql[p:p + 4] == " as ":
                    as_p = p
            if as_p > 0:
                with_pairs_.append([as_p, b])
        with_pairs = []
        lastp = sql.find("with ") + 5
        for w in with_pairs_:
            with_name = sql[lastp:w[0]].strip()
            with_pairs.append([with_name, w[0], w[1], ""])
            lastp = w[1][1] + 1
        return with_pairs

    def with_statems_(self, sql_, with_pairs):
        num_1 = True
        for w in with_pairs:
            sqlblock = sql_[w[2][0]:w[2][1]]
            startp = sqlblock.find("(")
            w[3] = sqlblock[startp + 1:len(sqlblock) - 1].strip()
        with_pairs.append(["__main_select__", -1, -1, sql_[w[2][1]:]])
        return with_pairs

    def with_insert_tmptbl_(self, with_statems):
        insert_statems = []
        for w in with_statems:
            if w[0] == "__main_select__":
                sql = w[3].strip()
            else:
                sql = "insert into " + w[0] + " " + w[3] + ";"
            insert_statems.append(sql)
        return insert_statems




