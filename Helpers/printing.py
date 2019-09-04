import fileio

def printHelp():
  printLines(fileio.readLines("help"))

## Prints a list of strings to the console
def printLines(lines):
  for line in lines:
    print(line)

