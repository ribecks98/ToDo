import cardInfo

def appendToTestFile(fileName):
  with open("testOut.md","a") as testFile:
    testFile.write("- ["+fileName+"]("+fileName+")\n")   

## Reads a file into a list of strings, where the ith element in the list is
## the content of the ith line of the file
def readLines(fileName):
  with open(fileName, 'r') as file:
    lines = file.readlines()
    for i in range(len(lines)):
      lines[i] = lines[i][:-1]
      if lines[i] and lines[i][-1] == '\r':
        lines[i] = lines[i][:-1]
  return lines

## Returns the row with the card number
def sortKey(row):
  return int(cardInfo.getCardNum(row[0][2]))

def writeToFile(fileName, lines, testFlag=""):
  if testFlag == "test":
    if "/" in fileName:
      fileName = fileName.replace("/","Test/",1)
    else:
      fileName = fileName.replace(".","Test.")
    appendToTestFile(fileName)
  writeLines(fileName, lines)

## Writes a list of strings to a file, where each string is separated by a
## newline
def writeLines(fileName, lines):
  with open(fileName, 'w') as file:
    for line in lines:
      file.write(line)
      file.write('\n')

