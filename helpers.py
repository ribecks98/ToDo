## Add the colourWrap and getArchiveFile functions, and change the search,
## constructFile, and getRowGroups functions to allow for automatic
## archiving. Also alphabetize the functions and delete a couple unused ones

def colourWrap(string, colour):
  return "  <span style=\"color:" + colour + "\">" + string.strip() + "</span>"

## Constructs the MarkDown file based from the row groups
def constructFile(rowGroups, fileFlag="bugs"):
  lines = ["<title>Bug Checklists</title>","","[Back to Archive](./archive.md)"]
  titles = getTitles(fileFlag)
  for i in range(len(titles)):
    lines.extend(constructTable(rowGroups[i],titles[i]))
  return lines

## Constructs a single table from the rows in it
def constructTable(rows, title):
  lines = ["", "## "+ title, "", "<table>", "  <tr><th>Bug</th><th>Checklist</th><th>Links</th>"]
  for row in sorted(rows,key=sortKey):
    lines.extend(row[0])
  lines.append("</table>")
  return lines

def deleteExcept(row, rowGroups, toExclude):
  for i in range(len(rowGroups)):
    if i in toExclude:
      continue
    if row in rowGroups[i]:
      rowGroups[i].remove(row)

def getArchiveFile(card):
  config = readLines("config.md")
  for line in config:
    bounds = line.split(" ")
    if card > bounds[0] and card < bounds[1]:
      archiveFile = "archive/" + bounds[0] + "-" + bounds[1] + ".md"
      break
  return archiveFile

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

def getTemplateLine(row):
  return searchLines("cards/template.md",row[0]) + row[1]

def getTitles(fileFlag):
  bugTitles = ["In Progress", "Code Reviews", "In QA", "Blocked"]
  archiveTitles = ["Completed", "No Action Required"]
  if fileFlag == "bugs":
    return bugTitles
  else:
    return archiveTitles

## Determines the file name of the output of the script based on whether it
## is a test or not
def outputFileName(fileName,flag):
  if flag == "test":
    return "testOut.md"
  return fileName

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

## Returns the row with the card number
def sortKey(row):
  return row[0][2]

## Writes a list of strings to a file, where each string is separated by a
## newline
def writeLines(fileName, lines):
  with open(fileName, 'w') as file:
    for line in lines:
      file.write(line)
      file.write('\n')

