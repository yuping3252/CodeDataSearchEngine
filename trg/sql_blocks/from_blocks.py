__author__ = 'Administrator'


class From_Blocks:
    def __init__(self):
        self.seq = 0

    def from_cut_short_(self, tree):
        len_ = len(tree)
        for i in range(len_):
            if tree[i][5] == "from":
                endpoint = 1000000
                for b1 in tree:
                    if b1[1] == tree[i][0] and b1[6] != "parenthensis" and endpoint > b1[3]:
                        endpoint = b1[3] - 1
                if endpoint < 1000000:
                    tree[i][4] = endpoint
                    tree[i][7] = tree[i][7][:endpoint - tree[i][3]]
        return tree













