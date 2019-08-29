## Add the ability to change the colour scheme using an update config

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
  rowGroups[-2].append(rows[rownum])
  helpers.deleteExcept(rows[rownum],rowGroups,[-2])

  lines = helpers.constructFile(rowGroups)
  helpers.writeToFile("bugs.md",lines,args[0])

def archive(args):
  config = load.getConfig()
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[1])
  rowGroups = helpers.getRowGroups(rows, lines)
  row = rows[rownum]

  indexLines = helpers.readLines("archive.md")
  lineNum = helpers.searchLines(args[1],indexLines)
  cardType = helpers.getCardType(config.colour, indexLines[lineNum])
  helpers.deleteExcept(row,rowGroups,[])
  row[0][2] = helpers.colourWrap("K"+args[1], config.colour[1][cardType])
  lineNum = helpers.searchLines("\"cards/",row[0])
  if "template" in row[0][lineNum]:
    del row[0][lineNum]
  else:
    row[0][lineNum] = row[0][lineNum].replace("\"cards","\"../cards")

  lines = helpers.constructFile(rowGroups)
  helpers.writeToFile("bugs.md",lines,args[0])

  archiveFile = helpers.getArchiveFile(args[1], config.partition)
  archiveLines = helpers.readLines(archiveFile)
  archiveRows = helpers.getRows(archiveLines, template)
  archiveRowGroups = helpers.getRowGroups(archiveRows, archiveLines, fileFlag="archive")
  if cardType == "blocked":
    archiveRowGroups[1].append(row)
  else:
    archiveRowGroups[0].append(row)

  archiveLines = helpers.constructFile(archiveRowGroups,fileFlag="archive")
  helpers.writeToFile(archiveFile,archiveLines,args[0])

  helpers.replaceColour(args[1],config.colour[0][cardType],config.colour[1][cardType],indexLines)
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
  config = load.getConfig()
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

  colour = config.colour[0][args[2]]

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
  config = load.getConfig()
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[1])
  row = rows[rownum]
  rowGroups = helpers.getRowGroups(rows, lines)
  row[0][2] = helpers.colourWrap("K"+args[1], config.colour[0]["blocked"])

  helpers.deleteExcept(row,rowGroups,[])
  rowGroups[-1].append(row)

  lines = helpers.constructFile(rowGroups)
  helpers.writeToFile("bugs.md",lines,args[0])

  archiveLines = helpers.readLines("archive.md")
  helpers.setColour(args[1],config.colour[0]["blocked"],archiveLines,config.colour)
  helpers.writeToFile("archive.md",archiveLines,args[0])

def updateConfig(args):
  config = load.getUpdateConfig()
  if not config.partition and not config.colour:
    return

  files = sorted(os.listdir("archive"))
  template = helpers.readLines("cardTemplate.md")
  archiveLines = helpers.readLines("archive.md")
  cardInfos = helpers.getCardInfos(archiveLines)
  archiveFileRowGroups = []
  for f in files:
    lines = helpers.readLines("archive/"+f)
    rows = helpers.getRows(lines, template)
    rowGroups = helpers.getRowGroups(rows, lines, fileFlag="archive")
    archiveFileRowGroups.append(rowGroups)
    for i in range(2):
      for j in range(len(rowGroups[i])):
        cardNum = helpers.sortKey(rowGroups[i][j])
        cardInfos[cardNum].row = rowGroups[i][j] 
        cardInfos[cardNum].rowNum = j
        cardInfos[cardNum].rowGroup = i

  if config.colour:
    oldConfig = load.getConfig()
    progressLines = helpers.readLines("bugs.md")
    rows = helpers.getRows(progressLines, template)
    rowGroups = helpers.getRowGroups(rows, progressLines)
    progressCards = []
    for i in range(len(rowGroups)):
      for j in range(len(rowGroups[i])):
        cardNum = helpers.sortKey(rowGroups[i][j])
        cardInfos[cardNum].row = rowGroups[i][j] 
        cardInfos[cardNum].rowNum = j
        cardInfos[cardNum].rowGroup = i
        progressCards.append(cardNum)

    for card in cardInfos.keys():
      cardInfos[card].setStatus(oldConfig.colour, progressCards)

    helpers.getPartition(cardInfos, oldConfig.partition, exclude=True)

    newArchiveRowGroups = [[[],[]] for f in files]

    for card in cardInfos.keys():
##    print(card,cardInfos[card].partition)
      helpers.updateColourByConfig(oldConfig.colour, config.colour, cardInfos[card])
      if cardInfos[card].partition >= 0:
        newArchiveRowGroups[cardInfos[card].partition][cardInfos[card].rowGroup].append(cardInfos[card].row)
      else:
        rowGroups[cardInfos[card].rowGroup][cardInfos[card].rowNum] = cardInfos[card].row

    helpers.getPartition(cardInfos, oldConfig.partition)
    archiveOut = helpers.constructArchiveFromInfos(archiveLines, cardInfos, oldConfig.partition)
    helpers.writeToFile("archive.md",archiveOut,args[0])
    for i in range(len(files)):
      lines = helpers.constructFile(newArchiveRowGroups[i], fileFlag="archive")
      helpers.writeToFile("archive/"+files[i], lines, args[0])

    lines = helpers.constructFile(rowGroups)
    helpers.writeToFile("bugs.md", lines, args[0])

  if config.partition:
    partition = helpers.getPartition(cardInfos, config.partition)
    archiveOut = helpers.constructArchiveFromPartition(archiveLines, partition, config.partition)
    helpers.writeToFile("archive.md",archiveOut,args[0])

    newArchives = [[[],[]] for part in range(len(config.partition))]
    for f in files:
      lines = helpers.readLines("archive/"+f)
      rows = helpers.getRows(lines, template)
      rowGroups = helpers.getRowGroups(rows, lines, fileFlag="archive")
      for i in range(2):
        for row in rowGroups[i]:
          cardNum = helpers.sortKey(row)
          newArchives[helpers.getArchiveIndex(cardNum, config.partition)][i].append(row)
      helpers.writeToFile("archiveOld/"+f, lines, args[0])
      if args[0] == "real":
        os.remove("archive/"+f)

    for i in range(len(config.partition)):
      lines = helpers.constructFile(newArchives[i],fileFlag="archive")
      helpers.writeToFile("archive/"+helpers.constructFileName(config.partition[i]),lines,args[0])

    for card in cardInfos.keys():
      if not os.path.exists("cards/" + str(card) + ".md"):
        continue
      lines = helpers.readLines("cards/" + str(card) + ".md")
      lines[0] = "[Back to Subarchive](../" + helpers.getArchiveFile(card, config.partition) +")"
      helpers.writeToFile("cards/" + str(card) + ".md", lines, args[0])

  load.setConfig(config, args[0])

def unblockCard(args):
  config = load.getConfig()
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[1])
  row = rows[rownum]
  rowGroups = helpers.getRowGroups(rows, lines)

  archiveLines = helpers.readLines("archive.md")
  lineNum = helpers.searchLines(args[1], archiveLines)
  cardInfo = helperClasses.CardInfo(int(args[1]), line=archiveLines[lineNum], row=row)
  cardType = helpers.getCardTypeFromRow(config.colour, row)
  helpers.updateColour(config.colour[0]["blocked"],config.colour[0][cardType],cardInfo)
  helpers.deleteExcept(row, rowGroups, [])
  cardInfo.row[0][2] = "  K"+args[1]
  if cardType == "code":
    rowGroups[0].append(cardInfo.row)
  elif cardType == "review":
    rowGroups[1].append(cardInfo.row)
  elif cardType == "investigate":
    rowGroups[2].append(cardInfo.row)

  lines = helpers.constructFile(rowGroups)
  helpers.writeToFile("bugs.md", lines, args[0])

  archiveLines[lineNum] = cardInfo.line
  helpers.writeToFile("archive.md", archiveLines, args[0])

def test(args):
  config = load.getUpdateConfig()
  print(config)

if __name__ == "__main__":
  import sys
  import helpers
  import configHelpers as load
  import helperClasses
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
      if "z" in choice:
        unblockCard(args)
        flag = 1
      if not flag:
        helpers.printHelp()

