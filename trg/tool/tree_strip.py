__author__ = 'Administrator'

from trg.tool             import block_strip
from trg.tool.block_strip import block_strip


def tree_strip(tree):
    len_ = len(tree)
    for i in range(len_):
        b = block_strip(tree[i])
        tree[i] = b
    return tree


