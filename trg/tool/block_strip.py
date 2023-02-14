__author__ = 'Administrator'

def block_strip(block):
    b1 = block[7]
    b2 = b1.strip()
    offset = b1.find(b2)
    left   = block[3] + offset
    right  = block[3] + offset + len(b2)
    block[3] = left
    block[4] = right
    block[7] = b2
    return block


