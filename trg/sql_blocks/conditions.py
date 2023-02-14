__author__ = 'Administrator'

class Conditions:
    def __init__(self):
        self.seq = 0

    def conditions_(self, tree, glo):
        new_list = []
        for b in tree:
            if b[5]=="where" or b[5]=="join on":
                le = 0
                c1 = b[7].strip()
                if b[5]=="where":
                    c1 = c1[6:]
                    le = b[3] + 6
                if b[5]=="join on":
                    c1 = c1[3:]
                    le = b[3] + 3
                ri = le + len(c1)
                pair = [glo.sqlid, b[0], "", le, ri, "condition", "condition", c1, False, b[9] + 1, ""]
                new_list.append(pair)
                glo.sqlid += 1
        tree.extend(new_list)
        return tree

