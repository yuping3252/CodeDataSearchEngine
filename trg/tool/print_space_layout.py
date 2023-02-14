__author__ = 'Administrator'

class Print_Layout:
    def __init__(self):
        seq = 0

    def print_(self,tree, phrase):
        tree.sort(key=lambda x: x[3])
        print (phrase, ":")
        dot = "."
        line_ = ""
        for i in range(57):
            line_ += dot
        for i in range(300):
            if (i/50)*50==i:
                segment = str(i)
                len_ = len(segment)
                segment += ".................................................."[:50 - len_]
                line_ += segment
            i += 1
        print (line_)
        self.print_recursive_(tree, tree[0])
        print ("\n")
        return True

    def print_recursive_(self, tree, block):
        self.print_line_(block)
        for b in tree:
            if b == block:
                continue
            if ((block[3] <= b[3] and b[4] < block[4]) or (block[3] < b[3] and b[4] <= block[4])) == False:
                continue
            # verified that b is a sub block of "block"
            b_is_top_sub_block = True
            span_ = 0
            for b1 in tree:
                if b1 == b or b1 == block:
                    continue
                if ((block[3] <= b1[3] and b1[4] < block[4]) or (block[3] < b1[3] and b1[4] <= block[4])) and \
                        ((b1[3] <= b[3] and b[4] < b1[4]) or (b1[3] < b[3] and b[4] <= b1[4])):
                    b_is_top_sub_block = False
            if b_is_top_sub_block:
                self.print_recursive_(tree, b)

    def print_line_(self, block):
        len_ = len(str(block[0]))
        prefix1 = ",    "[:5 - len_]
        len_ = len(str(block[1]))
        prefix2 = ",    "[:5 - len_]
        len_ = len(str(block[9]))
        prefix3 = "] "[:2 - len_]
        len_ = len(block[5])
        prefix4 = "[                 "[:17 - len_]
        len_ = len(block[6])
        prefix5 = ",                "[:18 - len_]
        prefix = "[" + str(block[0]) + prefix1 + str(block[1]) + prefix2 + str(block[9]) + prefix3 + prefix4 + block[5] + prefix5 + block[6] +"] "
        dot = "."
        dots = ""
        for i in range(block[3] + 7):
            dots += dot
        line_ = prefix + dots + block[7]
        print (line_)
