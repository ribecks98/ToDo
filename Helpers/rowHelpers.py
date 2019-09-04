import fileConstruct as construct
import fileio
import general
import helperClasses as classes
import searchAndReplace as sar

def cleanLines(lines,length):
  for i in range(len(lines)):
    if lines[i] == length:
      j = i+1
      while j < len(lines):
        if lines[j] < length:
          lines[i] = lines[j]
          break
        j = j+1

def constructNewChecklist(template,cardType,cardNum,newColour):
  checklist = fileio.readLines("Templates/"+cardType+".md")[2:]
  sar.replaceInLines("<colour>",newColour,checklist)
  line = sar.searchLines("<checklist>",template)
  del template[line]
  general.insertLines(template,checklist,line)
  sar.replaceInLines("<cardNum>",cardNum,template)
  return template[5:-1]

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
  titles = construct.getTitles(fileFlag)
  for title in titles:
    lineNums.append(sar.searchLinesHigh("## " + title,lines))
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

def getRowsByCard(lines, template, config):
  cardInfos = {}
  start = 0
  while start < len(lines):
    result = getRow(lines, template, start)
    if result[2] >= len(lines):
      break
    cardNum = fileio.sortKey(result)
    cardKey = str(cardNum)
    cardInfos[cardKey] = classes.CardInfo(cardNum,row=result)
    cardInfos[cardKey].setStatus(config.colour)
    start = result[2]
  return cardInfos

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

