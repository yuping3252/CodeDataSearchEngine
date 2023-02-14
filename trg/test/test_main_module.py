#!/usr/bin/python

import os, sys
import time

if __name__ == "__main__":
    print("Hello python !!!")


    def func_print():
        print("in func_print")


    def main():
        print("In main")
        func_print()


    main()