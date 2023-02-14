#!/usr/bin/python

class Merge_Lines:
    def merge_lines_(self, lines):
        merged = ""
        new_c  = ""
        for c in lines:
            new_c = c
            if c == "\n":
                new_c = " "
            merged += new_c
        return merged



