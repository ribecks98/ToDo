## Add the ability to change the colour scheme using an update config

def addNotes(args):
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  rows = rowHelpers.getRows(lines, template)
  rownum = rowHelpers.getRowNum(rows,args[1])
  lineNum = sar.searchInRow("cards/template.md",rows[rownum])
  lines[lineNum] = lines[lineNum].replace("template",args[1])
  fileio.writeToFile("bugs.md",lines,args[0])
  fileio.writeToFile("cards/"+args[1]+".md",["[Back to Cards](../bugs.md)",""],args[0])

def deleteNotes(args):
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  startLines = len(lines)
  rows = rowHelpers.getRows(lines,template)
  rownum = rowHelpers.getRowNum(rows,args[1])
  del lines[sar.searchInRow("template",rows[rownum])]
  fileio.writeToFile("bugs.md",lines,args[0])

def toQa(args):
  lines = fileio.readLines("bugs.md")
  startLines = len(lines)
  template = fileio.readLines("cardTemplate.md")
  rows = rowHelpers.getRows(lines, template)
  rownum = rowHelpers.getRowNum(rows,args[1])
  rowGroups = rowHelpers.getRowGroups(rows, lines)
  rowGroups[-2].append(rows[rownum])
  general.deleteExcept(rows[rownum],rowGroups,[-2])

  lines = construct.constructFile(rowGroups)
  fileio.writeToFile("bugs.md",lines,args[0])

def archive(args):
  config = load.getConfig()
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  rows = rowHelpers.getRows(lines, template)
  rownum = rowHelpers.getRowNum(rows,args[1])
  rowGroups = rowHelpers.getRowGroups(rows, lines)
  row = rows[rownum]

  indexLines = fileio.readLines("archive.md")
  lineNum = sar.searchLines(args[1],indexLines)
  cardType = cardHelp.getCardType(config.colour, indexLines[lineNum])
  general.deleteExcept(row,rowGroups,[])
  row[0][2] = general.colourWrap("ID"+args[1], config.colour[1][cardType])
  lineNum = sar.searchLines("\"cards/",row[0])
  if "template" in row[0][lineNum]:
    del row[0][lineNum]
  else:
    row[0][lineNum] = row[0][lineNum].replace("\"cards","\"../cards")

  lines = construct.constructFile(rowGroups)
  fileio.writeToFile("bugs.md",lines,args[0])

  archiveFile = general.getArchiveFile(args[1], config.partition)
  archiveLines = fileio.readLines(archiveFile)
  archiveRows = rowHelpers.getRows(archiveLines, template)
  archiveRowGroups = rowHelpers.getRowGroups(archiveRows, archiveLines, fileFlag="archive")
  if cardType == "blocked":
    archiveRowGroups[1].append(row)
  else:
    archiveRowGroups[0].append(row)

  archiveLines = construct.constructFile(archiveRowGroups,fileFlag="archive")
  fileio.writeToFile(archiveFile,archiveLines,args[0])

  colouring.replaceColour(args[1],config.colour[0][cardType],config.colour[1][cardType],indexLines)
  fileio.writeToFile("archive.md",indexLines,args[0])

  notesFile = "cards/"+args[1]+".md"
  if os.path.exists(notesFile):
    notesLines = fileio.readLines(notesFile)
    notesLines[0] = "[Back to Subarchive](../"+archiveFile+")"
    fileio.writeToFile(notesFile,notesLines,args[0])

def addPR(args):
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  rows = rowHelpers.getRows(lines, template)
  rownum = rowHelpers.getRowNum(rows,args[1])
  row = rows[rownum]
  lineNum = sar.searchInRow("pull/",row)
  lines[lineNum] = lines[lineNum].replace("pull/","pull/"+args[2])

  fileio.writeToFile("bugs.md",lines,args[0])

def addCard(args):
  config = load.getConfig()
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  rows = rowHelpers.getRows(lines, template)
  rowGroups = rowHelpers.getRowGroups(rows, lines)
  colour = config.colour[0][args[2]]
  newCard = [rowHelpers.constructNewChecklist(template,args[2],args[1],colour),0,0]

  if args[2] == "code":
    rowGroups[0].append(newCard)
  elif args[2] == "review":
    rowGroups[1].append(newCard)
  else:
    rowGroups[2].append(newCard)

  description = input("Give a description for the card: ")
  sar.replaceInLines("<description>",description,newCard[0])

  lines = construct.constructFile(rowGroups)
  fileio.writeToFile("bugs.md",lines,args[0])

  indexLines = fileio.readLines("archive.md")
  lineNum = -1
  for i in range(len(indexLines)):
    match = cardHelp.getCardNum(indexLines[i])
    if match and int(match) > int(args[1]):
      lineNum = i
      break
  if lineNum < 0:
    lineNum = len(indexLines)
  indexLines.insert(lineNum,general.archiveLine(args[1], description, colour))
  fileio.writeToFile("archive.md",indexLines,args[0])

def blockCard(args):
  config = load.getConfig()
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  rows = rowHelpers.getRows(lines, template)
  rownum = rowHelpers.getRowNum(rows,args[1])
  row = rows[rownum]
  rowGroups = rowHelpers.getRowGroups(rows, lines)
  row[0][2] = general.colourWrap("ID"+args[1], config.colour[0]["blocked"])

  general.deleteExcept(row,rowGroups,[])
  rowGroups[-1].append(row)

  lines = construct.constructFile(rowGroups)
  fileio.writeToFile("bugs.md",lines,args[0])

  archiveLines = fileio.readLines("archive.md")
  colouring.setColour(args[1],config.colour[0]["blocked"],archiveLines,config.colour)
  fileio.writeToFile("archive.md",archiveLines,args[0])

def updateConfig(args):
  config = load.getUpdateConfig()
  if not config.partition and not config.colour:
    return

  files = sorted(os.listdir("archive"))
  template = fileio.readLines("cardTemplate.md")
  archiveLines = fileio.readLines("archive.md")
  cardInfos = cardHelp.getCardInfos(archiveLines)
  archiveFileRowGroups = []
  for f in files:
    lines = fileio.readLines("archive/"+f)
    rows = rowHelpers.getRows(lines, template)
    rowGroups = rowHelpers.getRowGroups(rows, lines, fileFlag="archive")
    archiveFileRowGroups.append(rowGroups)
    for i in range(2):
      for j in range(len(rowGroups[i])):
        cardNum = fileio.sortKey(rowGroups[i][j])
        cardInfos[cardNum].row = rowGroups[i][j] 
        cardInfos[cardNum].rowNum = j
        cardInfos[cardNum].rowGroup = i

  if config.colour:
    oldConfig = load.getConfig()
    progressLines = fileio.readLines("bugs.md")
    rows = rowHelpers.getRows(progressLines, template)
    rowGroups = rowHelpers.getRowGroups(rows, progressLines)
    progressCards = []
    for i in range(len(rowGroups)):
      for j in range(len(rowGroups[i])):
        cardNum = fileio.sortKey(rowGroups[i][j])
        cardInfos[cardNum].row = rowGroups[i][j] 
        cardInfos[cardNum].rowNum = j
        cardInfos[cardNum].rowGroup = i
        progressCards.append(cardNum)

    for card in cardInfos.keys():
      cardInfos[card].setStatus(oldConfig.colour, progressCards)

    cardHelp.getPartition(cardInfos, oldConfig.partition, exclude=True)

    newArchiveRowGroups = [[[],[]] for f in files]

    for card in cardInfos.keys():
##    print(card,cardInfos[card].partition)
      colouring.updateColourByConfig(oldConfig.colour, config.colour, cardInfos[card])
      if cardInfos[card].partition >= 0:
        newArchiveRowGroups[cardInfos[card].partition][cardInfos[card].rowGroup].append(cardInfos[card].row)
      else:
        rowGroups[cardInfos[card].rowGroup][cardInfos[card].rowNum] = cardInfos[card].row

    cardHelp.getPartition(cardInfos, oldConfig.partition)
    archiveOut = construct.constructArchiveFromInfos(archiveLines, cardInfos, oldConfig.partition)
    fileio.writeToFile("archive.md",archiveOut,args[0])
    for i in range(len(files)):
      lines = construct.constructFile(newArchiveRowGroups[i], fileFlag="archive")
      fileio.writeToFile("archive/"+files[i], lines, args[0])

    lines = construct.constructFile(rowGroups)
    fileio.writeToFile("bugs.md", lines, args[0])

  if config.partition:
    partition = cardHelp.getPartition(cardInfos, config.partition)
    archiveOut = construct.constructArchiveFromPartition(archiveLines, partition, config.partition)
    fileio.writeToFile("archive.md",archiveOut,args[0])

    newArchives = [[[],[]] for part in range(len(config.partition))]
    for f in files:
      lines = fileio.readLines("archive/"+f)
      rows = rowHelpers.getRows(lines, template)
      rowGroups = rowHelpers.getRowGroups(rows, lines, fileFlag="archive")
      for i in range(2):
        for row in rowGroups[i]:
          cardNum = fileio.sortKey(row)
          newArchives[general.getArchiveIndex(cardNum, config.partition)][i].append(row)
      fileio.writeToFile("archiveOld/"+f, lines, args[0])
      if args[0] == "real":
        os.remove("archive/"+f)

    for i in range(len(config.partition)):
      lines = construct.constructFile(newArchives[i],fileFlag="archive")
      fileio.writeToFile("archive/"+construct.constructFileName(config.partition[i]),lines,args[0])

    for card in cardInfos.keys():
      if not os.path.exists("cards/" + str(card) + ".md"):
        continue
      lines = fileio.readLines("cards/" + str(card) + ".md")
      lines[0] = "[Back to Subarchive](../" + general.getArchiveFile(card, config.partition) +")"
      fileio.writeToFile("cards/" + str(card) + ".md", lines, args[0])

  load.setConfig(config, args[0])

def unblockCard(args):
  config = load.getConfig()
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  rows = rowHelpers.getRows(lines, template)
  rownum = rowHelpers.getRowNum(rows,args[1])
  row = rows[rownum]
  rowGroups = rowHelpers.getRowGroups(rows, lines)

  archiveLines = fileio.readLines("archive.md")
  lineNum = sar.searchLines(args[1], archiveLines)
  cardInfo = helperClasses.CardInfo(int(args[1]), line=archiveLines[lineNum], row=row)
  cardType = cardHelp.getCardTypeFromRow(config.colour, row)
  colouring.updateColour(config.colour[0]["blocked"],config.colour[0][cardType],cardInfo)
  general.deleteExcept(row, rowGroups, [])
  cardInfo.row[0][2] = "  ID"+args[1]
  if cardType == "code":
    rowGroups[0].append(cardInfo.row)
  elif cardType == "review":
    rowGroups[1].append(cardInfo.row)
  elif cardType == "investigate":
    rowGroups[2].append(cardInfo.row)

  lines = construct.constructFile(rowGroups)
  fileio.writeToFile("bugs.md", lines, args[0])

  archiveLines[lineNum] = cardInfo.line
  fileio.writeToFile("archive.md", archiveLines, args[0])

def test(args):
  lines = ["","","","","","",""]
  new = ["These","are","new","lines"]
  general.insertLines(lines,new,2)
  printing.printLines(lines)

if __name__ == "__main__":
  import sys
  sys.path.append("Helpers")
  import cardInfo as cardHelp
  import colouring
  import fileConstruct as construct
  import fileio
  import general
  import printing
  import rowHelpers
  import searchAndReplace as sar
  import configHelpers as load
  import helperClasses
  cardTypes = ["code","review","investigate"]
  if len(sys.argv) < 3:
    printing.printHelp()
  else:
    choice = sys.argv[1]
    args = sys.argv[2:]
    if choice[0] != "-":
      if choice == "test":
        test(args)
      else:
        printing.printHelp()
    else:
      flag = 0
      if len(choice) > 2 and not "t" in choice:
        print("Can't have multiple choices")
        choice = "-"
      if "t" in choice:
        args.insert(0,"test")
        fileio.writeLines("testOut.md",["[Back to Archive](archive.md)","","## Test result files",""])
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
      if "z" in choice:
        unblockCard(args)
        flag = 1
      if not flag:
        printing.printHelp()

