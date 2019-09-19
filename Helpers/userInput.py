import sys, printing

def readThingInList(aList):
    print("Please enter a value from the following list:")
    printing.printLines(aList)
    print("")
    thing = sys.stdin.readline()[:-1]
    while not thing in aList:
        print("")
        print("Not an option. Your options are: ")
        printing.printLines(aList)
        print("")
        thing = sys.stdin.readline()[:-1]
    return thing

