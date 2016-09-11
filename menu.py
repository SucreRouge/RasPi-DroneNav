#!python2
# -*- coding: UTF-8 -*-

import sys
from src_additional.manualcontrol import ManualControl

def main():
    choice = 0

    while choice != 1 or choice != 2:
        print('Choose module:')
        print('1 - manual control')
        print('2 - automatic navigation')
        print('3 - EXIT')
        choice = input()

        if choice == 1:
            c = ManualControl()
            c.main()
        elif choice == 2:
            pass
        elif choice == 3:
            sys.exit(0)
        else:
            continue



if __name__ == "__main__":
    main()
