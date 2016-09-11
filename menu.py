#!python2
# -*- coding: UTF-8 -*-

bashCommand_1 = "source virtualenvwrapper.sh"
bashCommand_2 = "workon cv"
bashCommand_3 = "deactivate"
# p = subprocess.call()

import subprocess
import sys
from src_additional.manualcontrol import ManualControl

imported = True
try:
    from src.shapeDetectNav import *
except ImportError:
    print('Error in importing shapeDetectNav - probably OS == Windows')
    imported = False

def main():
    choice = 0

    while choice != 1 or choice != 2:
        print('Choose module:')
        print('1 - manual control (throttle 1.0)')
        print('2 - manual control (throttle 0.1)')
        if imported:
            print('3 - automatic navigation (display on, cli on')
            print('4 - automatic navigation (display off, cli on')
        print('')
        print('5 - EXIT')
        choice = raw_input()

        if choice == '1':
            c = ManualControl(throttle = 1.0)
            c.main()
        elif choice == '2' and imported:
            c = ManualControl(throttle = 0.1)
            c.main()
        elif choice == '3' and imported:
            authonomic_control(1)
        elif choice == '4' and imported:
            authonomic_control(0)
        elif choice == '5':
            sys.exit(0)
        else:
            continue



if __name__ == "__main__":
    main()
