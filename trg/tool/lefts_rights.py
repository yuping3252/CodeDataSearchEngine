__author__ = 'Administrator'

class Lefts_Rights:
    def get_lefts_rights_(self,ss, symbol_left, symbol_right):
        s = ss
        lefts  = []
        rights = []
        base_  = 0
        len_ = len(s)
        # -------- collect positions of left parentheses
        for i in range(len_):
            p = s.find(symbol_left)
            if p == -1:
                break
            s = s[p+1:]
            lefts.append(base_ + p)
            base_ += p+1
#        if ss == "select c11, c12, c22, c32 from test_t1 t1 join (select c22, c23, c32  from test_t2  join (select c32, c33   from test_t3   union   select c41, c42   from test_t4) t3   union   select c51, c52  on c21 = c33) t2 on t1.c11 = t2.c23;":

        # -------- collect position of right parentheses
        s = ss
        base_ = 0
        for i in range(len_):
            p = s.find(symbol_right)
            if p == -1:
                break
            s = s[p+1:]
            rights.append(base_ + p)
            base_ += p+1
        if len(lefts) != len(rights):
            print ("error in lefts_rights_()")

            print ("symbol_left=", symbol_left)
            print ("symbol_right=", symbol_right)

            print ("lefts=", lefts)
            print ("rights=", rights)

            print ("ss=", ss)

            assert(len(lefts) == len(rights))
        return lefts, rights
