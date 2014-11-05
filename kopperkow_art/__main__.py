import sys
from sys import argv
from controller.MainController import MainController

__author__ = 'Kody'

usage = ["Pixel Art Usage:",
         "",
         "  -h , -help    : Open help dialogue",
         "  -f            : Input file",
         "  -o            : Output file",
         "  -v            : View only no edit"]

def main():
    __init__()

def __init__():
    if len(argv) >= 2:
        if argv[1] == "-help" or argv[1] == "-h":
            displayHelp("all")
        else:
            f = ""
            o = ""
            view = False
            if len(argv) == 2:
                myController = MainController(outFile=argv[2])
            else:
                for x in range(0,len(argv)):
                    if argv[x] == "-f":
                        f = argv[x + 1]
                    elif argv[x] == "-o":
                        o = argv[x + 1]
                    elif argv[x] == "-v":
                        view = True
                try:
                    myController = MainController(f, o, view)
                except:
                    print("Exiting PixelArt")
    elif len(argv) == 1:
        myController = MainController()
    else:
        displayHelp("no input")

def displayHelp(userInput):
    if userInput == "no input":
        for x in range(3):
            print(usage[x])
    else:
        for line in usage:
            print(line)
    sys.exit()

if __name__ == "__main__":
    main()
