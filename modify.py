## Add the ability to rearrange the structure and group different cards
## together in the archive
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
  rowGroups[3].append(rows[rownum])
  helpers.deleteExcept(rows[rownum],rowGroups,[3])

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

  config = helpers.readLines("config")
  archiveFile = helpers.getArchiveFile(args[1], config)

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
  helpers.writeToFile("archive.md",indexLines,args[0])

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
    helpers.printHelp()
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

def updateConfig(args):
  archiveLines = helpers.readLines("archive.md")
  cardLines = helpers.getCardLines(archiveLines)
  config = helpers.readConfig("update")
  partition = helpers.getPartition(cardLines, config)
  archiveOut = helpers.constructArchiveFromPartition(archiveLines, partition, config)
  helpers.writeToFile("archive.md",archiveOut,args[0])

  newArchives = [[[],[]] for part in range(len(config))]
  files = os.listdir("archive")
  template = helpers.readLines("cardTemplate.md")
  for f in files:
    lines = helpers.readLines("archive/"+f)
    rows = helpers.getRows(lines, template)
    rowGroups = helpers.getRowGroups(rows, lines, fileFlag="archive")
    for i in range(2):
      for row in rowGroups[i]:
        cardNum = helpers.sortKey(row)
        newArchives[helpers.getArchiveIndex(cardNum, flag="update")][i].append(row)

  for i in range(len(config)):
    lines = helpers.constructFile(newArchives[i],fileFlag="archive")
    helpers.writeToFile("archive/"+helpers.constructFileName(config[i]),lines,args[0])

  for line in cardLines:
    if not os.path.exists("cards/" + str(line.card) + ".md"):
      continue
    lines = helpers.readLines("cards/" + str(line.card) + ".md")
    lines[0] = "[Back to Subarchive](../" + helpers.getArchiveFile(line.card, flag="update") +")"
    helpers.writeToFile("cards/" + str(line.card) + ".md", lines, args[0])

def test(args):
  helpers.writeToFile("blorg.txt",["string"],"test")

if __name__ == "__main__":
  import sys, helpers13 as helpers
  cardTypes = ["code","review","investigate"]
  if len(sys.argv) < 3:
    helpers.printHelp()
  else:
    choice = sys.argv[1]
    args = sys.argv[2:]
    if choice[0] != "-":
      if choice == "test":
        test(args)
      else:
        helpers.printHelp()
    else:
      flag = 0
      if len(choice) > 2 and not "t" in choice:
        print("Can't have multiple choices")
        choice = "-"
      if "t" in choice:
        args.insert(0,"test")
        helpers.writeLines("testOut.md",["[Back to Archive](archive.md)","","## Test result files",""])
      else:
        args.insert(0,"real")
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
      if "p" in choice and len(args) >= 3:
        addPR(args)
        flag = 1
      if "c" in choice and len(args) >= 3:
        addCard(args)
        flag = 1
      if "b" in choice:
        blockCard(args)
        flag = 1
      if "u" in choice:
        import os
        updateConfig(args)
        flag = 1
      if not flag:
        helpers.printHelp()

