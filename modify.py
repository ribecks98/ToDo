## Prepend the test flag instead of appending it so the indexes of other 
## arguments don't change. Also fix a few bugs along the way
import colours

def addNotes(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[1])
  lineNum = helpers.searchInRow("cards/template.md",rows[rownum])
  lines[lineNum] = lines[lineNum].replace("template",args[1])
  helpers.writeToFile("bugs.md",lines,args[0])
  helpers.writeToFile("cards/"+args[1]+".md",["[Back to Cards](../bugs.md)",""],args[0])

def deleteNotes(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  startLines = len(lines)
  rows = helpers.getRows(lines,template)
  rownum = helpers.getRowNum(rows,args[1])
  del lines[helpers.searchInRow("template",rows[rownum])]
  helpers.writeToFile("bugs.md",lines,args[0])

def toQa(args):
  lines = helpers.readLines("bugs.md")
  startLines = len(lines)
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[1])
  rowGroups = helpers.getRowGroups(rows, lines)
  rowGroups[2].append(rows[rownum])
  helpers.deleteExcept(rows[rownum],rowGroups,[2])

  lines = helpers.constructFile(rowGroups)
  helpers.writeToFile("bugs.md",lines,args[0])

def archive(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[1])
  rowGroups = helpers.getRowGroups(rows, lines)
  row = rows[rownum]
  cardType = helpers.getCardType(row)
  helpers.deleteExcept(row,rowGroups,[])
  row[0][2] = helpers.colourWrap("K"+args[1], colours.completedTable[cardType])
  lineNum = helpers.searchLines("\"cards/",row[0])
  if "template" in row[0][lineNum]:
    del row[0][lineNum]
  else:
    row[0][lineNum] = row[0][lineNum].replace("\"cards","\"../cards")

  lines = helpers.constructFile(rowGroups)
  helpers.writeToFile("bugs.md",lines,args[0])

  archiveFile = helpers.getArchiveFile(args[1])

  archiveLines = helpers.readLines(archiveFile)
  archiveRows = helpers.getRows(archiveLines, template)
  archiveRowGroups = helpers.getRowGroups(archiveRows, archiveLines, fileFlag="archive")
  if cardType == "blocked":
    archiveRowGroups[1].append(row)
  else:
    archiveRowGroups[0].append(row)

  archiveLines = helpers.constructFile(archiveRowGroups,fileFlag="archive")
  helpers.writeToFile(archiveFile,archiveLines,args[0])

  indexLines = helpers.readLines("archive.md")
  helpers.replaceColour(args[1],colours.inProgressTable[cardType],colours.completedTable[cardType],indexLines)
  helpers.writeToFile("archive.md",indexLines,args[1])

  notesFile = "cards/"+args[1]+".md"
  if os.path.exists(notesFile):
    notesLines = helpers.readLines(notesFile)
    notesLines[0] = "[Back to Subarchive](../"+archiveFile+")"
    helpers.writeToFile(notesFile,notesLines,args[0])

def addPR(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[1])
  row = rows[rownum]
  lineNum = helpers.searchInRow("pull/",row)
  lines[lineNum] = lines[lineNum].replace("pull/","pull/"+args[2])

  helpers.writeToFile("bugs.md",lines,args[0])

def addCard(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rowGroups = helpers.getRowGroups(rows, lines)
  newCard = [template[5:-1],0,0]
  helpers.replaceInLines("<cardNum>",args[1],newCard[0])
  if args[2] == "code":
    del newCard[0][26:67]
    rowGroups[0].append(newCard)
  elif args[2] == "review":
    del newCard[0][57:67]
    del newCard[0][6:26]
    rowGroups[1].append(newCard)
  elif args[2] == "investigate":
    del newCard[0][6:57]
    rowGroups[2].append(newCard)
  else:
    print(helpString," [code,review,investigate]")
    return

  colour = colours.inProgressTable[args[2]]

  description = input("Give a description for the card: ")
  helpers.replaceInLines("<description>",description,newCard[0])

  lines = helpers.constructFile(rowGroups)
  helpers.writeToFile("bugs.md",lines,args[0])

  indexLines = helpers.readLines("archive.md")
  lineNum = -1
  for i in range(len(indexLines)):
    match = helpers.getCardNum(indexLines[i])
    if match and int(match) > int(args[1]):
      lineNum = i
      break
  if lineNum < 0:
    lineNum = len(indexLines)
  indexLines.insert(lineNum,helpers.archiveLine(args[1], description, colour))
  helpers.writeToFile("archive.md",indexLines,args[0])

def blockCard(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[1])
  row = rows[rownum]
  rowGroups = helpers.getRowGroups(rows, lines)
  row[0][2] = helpers.colourWrap("K"+args[1], colours.inProgressTable["blocked"])

  helpers.deleteExcept(row,rowGroups,[])
  rowGroups[-1].append(row)

  lines = helpers.constructFile(rowGroups)
  helpers.writeToFile("bugs.md",lines,args[0])

  archiveLines = helpers.readLines("archive.md")
  helpers.setColour(args[1],colours.inProgressTable["blocked"],archiveLines)
  helpers.writeToFile("archive.md",archiveLines,args[0])

def test(args):
  helpers.writeToFile("blorg.txt",["string"],"test")

if __name__ == "__main__":
  import sys, helpers10 as helpers
  helpString = "Usage: python modify.py [deleteNotes,addNotes,toQa] <cardNum>"
  cardTypes = ["code","review","investigate"]
  if len(sys.argv) < 3:
    print(helpString)
  else:
    choice = sys.argv[1]
    args = sys.argv[2:]
    if choice[0] != "-":
      if choice == "test":
        test(args)
      else:
        print(helpString)
    else:
      flag = 0
      if len(choice) > 2 and not "t" in choice:
        print("Can't have multiple choices")
        choice = "-"
      if "t" in choice:
        args.insert(0,"test")
        helpers.writeLines("testOut.md",["[Back to Archive](archive.md)","","## Test result files",""])
      else:
        args.append("real")
      if "q" in choice: 
        toQa(args)
        flag = 1
      if "n" in choice:
        addNotes(args)
        flag = 1
      if "d" in choice:
        deleteNotes(args)
        flag = 1
      if "r" in choice:
        import os
        archive(args)
        flag = 1
      if "p" in choice:
        if len(args) < 3:
          print(helpString+" <prNum>")
        else:
          addPR(args)
          flag = 1
      if "c" in choice:
        if len(args) < 3:
          print(helpString+" ["+",".join(cardTypes)+"]")
        else:
          addCard(args)
          flag = 1
      if "b" in choice:
        blockCard(args)
        flag = 1
      if not flag:
        print(helpString)

