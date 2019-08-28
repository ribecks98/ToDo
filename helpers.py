titles = ["In Progress", "Code Reviews", "In QA", "Blocked"]

## Reads a file into a list of strings, where the ith element in the list is
## the content of the ith line of the file
def readLines(fileName):
  with open(fileName, 'r') as file:
    lines = file.readlines()
    for i in range(len(lines)):
      lines[i] = lines[i][:-1]
  return lines

## Writes a list of strings to a file, where each string is separated by a
## newline
def writeLines(fileName, lines):
  with open(fileName, 'w') as file:
    for line in lines:
      file.write(line)
      file.write('\n')

## Determines the file name of the output of the script based on whether it
## is a test or not
def outputFileName(flag):
  if flag == "test":
    return "testOut.md"
  return "bugs.md"

## Constructs the MarkDown file based from the row groups
def constructFile(rowGroups):
  lines = ["<title>Bug Checklists</title>","","[Back to Archive](./archive.md)"]
  for i in range(4):
    lines.extend(constructTable(rowGroups[i],titles[i]))
  return lines

## Returns the row with the card number
def sortKey(row):
  return row[0][2]

## Constructs a single table from the rows in it
def constructTable(rows, title):
  lines = ["", "## "+ title, "", "<table>", "  <tr><th>Bug</th><th>Checklist</th><th>Links</th>"]
  for row in sorted(rows,key=sortKey):
    lines.extend(row[0])
  lines.append("</table>")
  return lines

## Prints a list of strings to the console
def printLines(lines):
  for line in lines:
    print(line)

## Searches a list of strings for an input string. Returns the line number if
## found and -1 if not
def searchLines(string, lines):
  for i in range(len(lines)):
    if string in lines[i]:
      return i
  return -1

## Splits the lines into the rows of the HTML table based on the row template
def getRows(lines, template):
  rows = []
  start = 0
  while start < len(lines):
    result = getRow(lines, template, start)
    rows.append(result)
    start = result[2]
  return rows[:-1]

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

## Given a list of rows, finds the index of the row corresponding to the
## input card
def getRowNum(rows, cardNum):
  for i in range(len(rows)):
    if cardNum in rows[i][0][2]:
      return i

def getRowGroups(rows,lines):
  rowGroups = []
  lineNums = []
  for title in titles:
    lineNums.append(searchLines("## " + title,lines))
  lineNums.append(len(lines))
  for i in range(4):
    rowGroups.append(selectRows(rows,lineNums[i],lineNums[i+1]))
  return rowGroups

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

## Inserts a row into the file at the given line number
def pushRow(row, lines, linenum):
  while row[0]:
    thing = row[0].pop()
    lines.insert(linenum, thing)

## Finds the line number where the specified row should be inserted in the 
## QA table. Returns the start of the table if there are no cards in QA
def findPosition(row, qaRows, qaStart):
  if not type(qaRows) is list:
    return qaStart + 3
  for i in range(len(qaRows)):
    if row[0][2] < qaRows[i][0][2]:
      return qaRows[i][1]
  return qaRows[-1][2]

## Deletes lines from the original file at the given starting index until
## the file is its original length
def deleteOld(lines, start, totalLines):
  while len(lines) > totalLines:
    lines.pop(start)

def getTemplateLine(row):
  return searchLines("cards/template.md",row[0]) + row[1]

def deleteExcept(row, rowGroups, toExclude):
  for i in range(len(rowGroups)):
    if i in toExclude:
      continue
    if row in rowGroups[i]:
      rowGroups[i].remove(row)
