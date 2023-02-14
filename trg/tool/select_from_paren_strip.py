__author__ = 'Administrator'

from trg.tool             import tree_strip, block_strip
from trg.tool.tree_strip  import tree_strip
from trg.tool.block_strip import block_strip

def select_from_paren_strip(tree):
    len_ = len(tree)
    tree = tree_strip(tree)
    for i in range(len_):
        b = tree[i]
        left  = b[7].count("(")
        right = b[7].count(")")
        if left > right and b[7][0] == "(" and b[7][len(b[7])-1] != ")":
            b[3] += 1
            b[7]  = b[7][1:]
            b = block_strip(b)
        if left < right and b[7][0] != "(" and b[7][len(b[7])-1] == ")":
            b[4] -= 1
            b[7]  = b[7][:len(b[7])-1]
        tree[i] = b
    return tree


