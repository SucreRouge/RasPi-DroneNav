#!python2
# -*- coding: UTF-8 -*-

import sys
import subprocess
from src_additional.manualcontrol import ManualControl

imported = True
try:
    from src.shapeDetectNav import *
except ImportError:
    print('Error in importing shapeDetectNav - probably OS == Windows')
    imported = False

output = process.communicate()[0]
bashCommand_1 = "source virtualenvwrapper.sh"
bashCommand_2 = "workon cv"
bashCommand_3 = "deactivate"

def main():
    choice = 0

    while choice != 1 or choice != 2:
        print('Choose module:')
        print('1 - manual control')
            p = subprocess.Popen(bashCommand_3.split(), stdout=subprocess.PIPE)
        if imported:
            p = subprocess.Popen(bashCommand_1.split(), stdout=subprocess.PIPE)
            p = subprocess.Popen(bashCommand_2.split(), stdout=subprocess.PIPE)
            print('2 - automatic navigation')
        print('3 - EXIT')
        choice = input()

        if choice == 1:
            c = ManualControl()
            c.main()
        elif choice == 2 and imported:
            authonomic_control()
        elif choice == 3:
            sys.exit(0)
        else:
            continue



if __name__ == "__main__":
    main()
