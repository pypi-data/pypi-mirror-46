from polarishub import setup
from polarishub import manage
import sys
def operation():
    setup.initialization()

from polarishub import manage
def runHub():
    #print(sys.argv)
    manage.runserver()

def main():
    commandArgv = sys.argv
    if len(commandArgv) == 1:
        print("Wrong command! Please use -h for help.")
        return
    if commandArgv[1] == "-h":
        print("Commands:")
        print("  setup:\tSetup the environment for polarishub.")
        print("  run:\trun the polarishub on your computer.")
    if commandArgv[1] == "setup":
        operation()
    if commandArgv[1] == "run":
        runHub()