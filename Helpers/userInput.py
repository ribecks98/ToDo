import sys

def readThingInList(aList):
    print("Please enter a value from the following list:")
    print(aList)
    thing = sys.stdin.readline()[:-1]
    while not thing in aList:
        print("Not an option. Your options are: ")
        print(aList)
        thing = sys.stdin.readline()[:-1]
    return thing

