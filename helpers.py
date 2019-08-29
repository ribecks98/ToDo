## Use the revised CardInfo class and the new Config class
import re, colours, helperClasses14 as helpers

def addZeroes(num):
  string = str(num)
  while len(string) < 5:
    string = "0"+string
  return string

def appendToTestFile(fileName):
  with open("testOut.md","a") as testFile:
    testFile.write("- ["+fileName+"]("+fileName+")\n")   

def archiveLine(cardNum, description, colour):
  return "- "+colourWrap("K"+cardNum, colour).strip()+" "+description

def cleanLines(lines,length):
  for i in range(len(lines)):
    if lines[i] == length:
      j = i+1
      while j < len(lines):
        if lines[j] < length:
          lines[i] = lines[j]
          break
        j = j+1

def colourWrap(string, colour):
  return "  <span style=\"color:" + colour + "\">" + string.strip() + "</span>"

def constructArchiveFromPartition(archiveLines, partition, config):
  archiveOut = archiveLines[:9]
  for i in range(len(config)):
    archiveOut.extend([constructArchiveLink(config[i]),""])
    archiveOut.extend(partition[i])
    archiveOut.append("")
  return archiveOut

def constructArchiveLink(configLine):
  start = addZeroes(configLine[0])
  end = addZeroes(configLine[1])
  return "##### [K" + start + "-K" + end + \
  "](archive/" + start + "-" + end + ".md)"

## Constructs the MarkDown file based from the row groups
def constructFile(rowGroups, fileFlag="bugs"):
  lines = getStartLines(fileFlag)
  titles = getTitles(fileFlag)
  for i in range(len(titles)):
    if rowGroups[i] != []:
      lines.extend(constructTable(rowGroups[i],titles[i]))
  return lines

def constructFileName(configLine):
  return addZeroes(configLine[0]) + "-" + addZeroes(configLine[1]) + ".md"

## Constructs a single table from the rows in it
def constructTable(rows, title):
  lines = ["", "## "+ title, "", "<table>", "  <tr><th>Bug</th><th>Checklist</th><th>Links</th>"]
  for row in sorted(rows,key=sortKey):
    lines.extend(row[0])
  lines.append("</table>")
  return lines

def deleteExcept(row, rowGroups, toExclude):
  for i in range(len(toExclude)):
    toExclude[i] = toExclude[i] % len(rowGroups)
  for i in range(len(rowGroups)):
    if i in toExclude:
      continue
    if row in rowGroups[i]:
      rowGroups[i].remove(row)

def getArchiveFile(card, partitionConfig):
  for i in range(len(partitionConfig)):
    if int(card) >= partitionConfig[i][0] and int(card) <= partitionConfig[i][1]:
      archiveFile = "archive/" + addZeroes(partitionConfig[i][0]) + "-" + addZeroes(partitionConfig[i][1]) + ".md"
      break
  return archiveFile

def getArchiveIndex(card, partitionConfig):
  for i in range(len(partitionConfig)):
    if int(card) >= partitionConfig[i][0] and int(card) <= partitionConfig[i][1]:
      return i
  return -1


def getCardLines(archiveLines):
  cardLines = {}
  for line in archiveLines:
    card = getCardNum(line)
    if card and not "#####" in line:
      cardLines[int(card)] = (helpers.CardInfo(line=line))
  return cardLines

def getCardNum(line):
  match = re.search(">.*<", line)
  if match:
    return match.group(0)[2:-1]
  match = re.search("K[0-9]*", line)
  if match:
    return match.group(0)[1:]

def getCardType(row):
  if colours.inProgressTable["blocked"] in row[0][2]:
    return "blocked"
  for key in colours.inProgressTable.keys():
    if colours.inProgressTable[key] in row[0][9]:
      return key

def getPartition(cardLines, config):
  count = 0
  partition = [[]]
  for card in cardLines.keys():
    if card > config[count][1]:
      partition.append([])
      count = count + 1
    partition[-1].append(cardLines[card].line)
    cardLines[card].partition = count
  return partition

## Gets a single row in the table based on the card template, starting from
## the given start line. Returns the contents as a list of strings, along
## with the indexes of the first and last lines of the row in the original
## list of strings
def getRow(lines, template, start):
  for i in range(start, len(lines)):
    if template[5] == lines[i]:
      realStart = i
    if template[-3] == lines[i]:
      end = i
      return [lines[realStart:end+2], realStart, end + 2]

  return [[], start, len(lines)]

def getRowGroups(rows,lines,fileFlag="bugs"):
  rowGroups = []
  lineNums = []
  titles = getTitles(fileFlag)
  for title in titles:
    lineNums.append(searchLinesHigh("## " + title,lines))
  lineNums.append(len(lines))
  cleanLines(lineNums,len(lines))
  for i in range(len(titles)):
    rowGroups.append(selectRows(rows,lineNums[i],lineNums[i+1]))
  return rowGroups

## Given a list of rows, finds the index of the row corresponding to the
## input card
def getRowNum(rows, cardNum):
  for i in range(len(rows)):
    if cardNum in rows[i][0][2]:
      return i

## Splits the lines into the rows of the HTML table based on the row template
def getRows(lines, template):
  rows = []
  start = 0
  while start < len(lines):
    result = getRow(lines, template, start)
    rows.append(result)
    start = result[2]
  return rows[:-1]

def getStartLines(fileFlag):
  if fileFlag == "bugs":
    return ["<title>Bug Checklists</title>","","[Back to Archive](archive.md)"]
  return ["<title>Bug Checklists</title>","","[Back to Archive](../archive.md)"]

def getTitles(fileFlag):
  bugTitles = ["In Progress", "Code Reviews", "Investigations", "In QA", "Blocked"]
  archiveTitles = ["Completed", "No Action Required"]
  if fileFlag == "bugs":
    return bugTitles
  else:
    return archiveTitles

def printHelp():
  printLines(readLines("help"))

## Prints a list of strings to the console
def printLines(lines):
  for line in lines:
    print(line)

## Inserts a row into the file at the given line number
def pushRow(row, lines, linenum):
  while row[0]:
    thing = row[0].pop()
    lines.insert(linenum, thing)

## Reads a file into a list of strings, where the ith element in the list is
## the content of the ith line of the file
def readLines(fileName):
  with open(fileName, 'r') as file:
    lines = file.readlines()
    for i in range(len(lines)):
      lines[i] = lines[i][:-1]
  return lines

def replaceColour(card,colour1,colour2,lines):
  line = searchLines(card, lines)
  lines[line] = lines[line].replace(colour1,colour2)

def replaceInLines(target, string, lines):
  for i in range(len(lines)):
    lines[i] = lines[i].replace(target,string)

def searchInRow(string, row):
  return row[1] + searchLines(string, row[0])

## Searches a list of strings for an input string. Returns the line number if
## found and -1 if not
def searchLines(string, lines):
  for i in range(len(lines)):
    if string in lines[i]:
      return i
  return -1

def searchLinesHigh(string, lines):
  line = searchLines(string, lines)
  if line < 0:
    return len(lines)
  return line

## Gets a list of the cards in QA. Returns empty if there are none
def selectRows(rows, startLine, endLine):
  start = -1
  end = -1
  for i in range(len(rows)):
    if rows[i][1] > startLine and start < 0:
      start = i 
    if rows[i][1] > endLine and end < 0:
      end = i
  if start < 0:
    return []
  if end < 0:
    return rows[start:]
  return rows[start:end]

def setColour(card,colour,lines):
  for table in [colours.inProgressTable, colours.completedTable]:
    for key in table.keys():
      replaceColour(card,table[key],colour,lines)

## Returns the row with the card number
def sortKey(row):
  return int(getCardNum(row[0][2]))

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

