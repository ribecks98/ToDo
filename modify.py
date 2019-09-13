import os

def addNotes(args): ## -n 
  config = load.getConfig()
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  cardInfos = rowHelpers.getRowsByCard(lines, template, config, {})
  lineNum = sar.searchInRow("cards/template.md",cardInfos[args[1]].row)
  lines[lineNum] = lines[lineNum].replace("template",args[1])
  fileio.writeToFile("bugs.md",lines,args[0])
  fileio.writeToFile("cards/"+args[1]+".md",["[Back to Cards](../bugs.md)",""],args[0])

def deleteNotes(args): ## -d
  config = load.getConfig()
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  cardInfos = rowHelpers.getRowsByCard(lines, template, config, {})
  del lines[sar.searchInRow("cards/"+args[1],cardInfos[args[1]].row)]
  fileio.writeToFile("bugs.md",lines,args[0])

def archive(args): ## -r
  config = load.getConfig()
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  cardInfos = rowHelpers.getRowsByCard(lines, template, config, {})

  indexLines = fileio.readLines("archive.md")
  lineNum = sar.searchLines(args[1]+"<",indexLines)
  cardInfos[args[1]].status.complete = True ## We've completed the thing
  cardType = cardInfos[args[1]].status.convertToStatus()
  cardInfos[args[1]].row[0][2] = general.colourWrap("ID"+args[1], config.colour[1][cardType])
  lineNum = sar.searchLines("\"cards/",cardInfos[args[1]].row[0])
  if "template" in cardInfos[args[1]].row[0][lineNum]:
    del cardInfos[args[1]].row[0][lineNum]
  else:
    cardInfos[args[1]].row[0][lineNum] = cardInfos[args[1]].row[0][lineNum].replace("\"cards","\"../cards")

  lines = construct.constructFileByCard( \
    rowHelpers.getRowGroupsByCard( \
      filters.filter1(cardInfos),config \
    ), \
    config \
  )
  fileio.writeToFile("bugs.md",lines,args[0])

  archiveFile = general.getArchiveFile(args[1], config.partition)
  archiveLines = fileio.readLines(archiveFile)
  archiveRows = rowHelpers.getRowsByCard(archiveLines, template, config, cardInfos)

  part = -1
  for i in range(len(config.partition)):
    if int(args[1]) >= config.partition[i][0] and int(args[1]) <= config.partition[i][1]:
      part = i
      break

  archiveLines = construct.constructFileByCard( \
    rowHelpers.getRowGroupsByCard( \
      filters.filter2(cardInfos,config.partition[part]),config \
    ), \
    config, \
    fileFlag="archive" \
  )
  fileio.writeToFile(archiveFile,archiveLines,args[0])

  colouring.replaceColour(args[1],config.colour[0][cardType],config.colour[1][cardType],indexLines)
  fileio.writeToFile("archive.md",indexLines,args[0])

  notesFile = "cards/"+args[1]+".md"
  if os.path.exists(notesFile):
    notesLines = fileio.readLines(notesFile)
    notesLines[0] = "[Back to Subarchive](../"+archiveFile+")"
    fileio.writeToFile(notesFile,notesLines,args[0])

def addPR(args): ## -p
  config = load.getConfig()
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  cardInfos = rowHelpers.getRowsByCard(lines, template, config, {})
  lineNum = sar.searchInRow("pull/",cardInfos[args[1]].row)
  lines[lineNum] = lines[lineNum].replace("pull/","pull/"+args[2])

  fileio.writeToFile("bugs.md",lines,args[0])

def addCard(args): ## -c
  config = load.getConfig()
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  cardInfos = rowHelpers.getRowsByCard(lines, template, config, {})
  colour = config.colour[0][args[2]]
  newCard = [rowHelpers.constructNewChecklist(template,args[2],args[1],colour),0,0]
  cardInfos[args[1]] = classes.CardInfo(int(args[1]),row=newCard)
  cardInfos[args[1]].status = classes.State(False,args[2],False)

  description = input("Give a description for the card: ")
  sar.replaceInLines("<description>",description,cardInfos[args[1]].row[0])

  lines = construct.constructFileByCard( \
    rowHelpers.getRowGroupsByCard( \
      filters.filter1(cardInfos),config \
    ), \
    config \
  )
  fileio.writeToFile("bugs.md",lines,args[0])

  indexLines = fileio.readLines("archive.md")
  lineNum = -1
  for i in range(len(indexLines)):
    match = cardHelp.getCardNum(indexLines[i])
    if match and int(match) > int(args[1]):
      if "#####" in indexLines[i]:
        lineNum = i-1
      else:
        lineNum = i
      break
  if lineNum < 0:
    lineNum = len(indexLines)
  indexLines.insert(lineNum,general.archiveLine(args[1], description, colour))
  fileio.writeToFile("archive.md",indexLines,args[0])

def blockCard(args): ## -b
  config = load.getConfig()
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  cardInfos = rowHelpers.getRowsByCard(lines, template, config, {})
  cardInfos[args[1]].row[0][2] = general.colourWrap("ID"+args[1], config.colour[0]["blocked"])
  cardInfos[args[1]].status.blocked = True

  lines = construct.constructFileByCard( \
    rowHelpers.getRowGroupsByCard( \
      filters.filter1(cardInfos), config
    ), \
    config \
  )
  fileio.writeToFile("bugs.md",lines,args[0])

  archiveLines = fileio.readLines("archive.md")
  colouring.setColour(args[1],config.colour[0]["blocked"],archiveLines,config.colour)
  fileio.writeToFile("archive.md",archiveLines,args[0])

def updateConfig(args): ## -u
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

def unblockCard(args): ## -z
  config = load.getConfig()
  lines = fileio.readLines("bugs.md")
  template = fileio.readLines("cardTemplate.md")
  cardInfos = rowHelpers.getRowsByCard(lines, template, config, {})
  if not cardInfos[args[1]].status.blocked or cardInfos[args[1]].status.complete:
    return

  cardInfos[args[1]].row[0][2] = "  ID"+args[1]
  cardInfos[args[1]].status.blocked = False
  archiveLines = fileio.readLines("archive.md")
  lineNum = sar.searchLines(args[1], archiveLines)
  cardInfos[args[1]].line = archiveLines[lineNum]
  cardType = cardInfos[args[1]].status.status
  colouring.updateColour(config.colour[0]["blocked"],config.colour[0][cardType],cardInfos[args[1]])

  lines = construct.constructFileByCard( \
    rowHelpers.getRowGroupsByCard( \
      filters.filter1(cardInfos), config \
    ), \
    config \
  )
  fileio.writeToFile("bugs.md", lines, args[0])

  archiveLines[lineNum] = cardInfos[args[1]].line
  fileio.writeToFile("archive.md", archiveLines, args[0])

def cleanTests(args):
  fileio.writeLines("testOut.md",["[Back to Archive](archive.md)"])
  files = filter(lambda x: "Test" in x,os.listdir())
  for f in files:
    if os.path.isfile(f):
      os.remove(f)
    else:
      sub = os.listdir(f)
      for g in sub:
        os.remove(f+"/"+g)
      os.rmdir(f)

def test(args):
  nums = [1,2,3,4,5,656,76,7,8,899,8,7,6]

def isValid(args, minVal):
  return len(args) >= minVal

def chooseScript(choice, args):
  import os
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
      cleanTests(args)
      files = os.listdir()
      toexclude = [".git","Templates","Helpers","update"]
      for f in files:
        if os.path.isdir(f) and not f in toexclude:
          os.mkdir(f+"Test")
    else:
      args.insert(0,"real")
    if "q" in choice: 
      cont = input("This function is not being actively maintained. Continue? [y/n]")
      if cont == "y" and isValid(args,2):
        toQa(args)
        flag = 1
    if "n" in choice:
      if isValid(args,2):
        addNotes(args)
        flag = 1
    if "d" in choice:
      if isValid(args,2):
        deleteNotes(args)
        flag = 1
    if "r" in choice:
      if isValid(args,2):
        archive(args)
        flag = 1
    if "p" in choice:
      if isValid(args,3):
        addPR(args)
        flag = 1
    if "c" in choice and len(args) >= 3:
      if isValid(args,3):
        addCard(args)
        flag = 1
    if "b" in choice:
      if isValid(args,2):
        blockCard(args)
        flag = 1
    if "u" in choice:
      if isValid(args,1):
        import os
        updateConfig(args)
        flag = 1
    if "v" in choice:
      if isValid(args,1):
        cleanTests(args)
        flag = 1
    if "z" in choice:
      if isValid(args,2):
        unblockCard(args)
        flag = 1
    if not flag:
      printing.printHelp()

if __name__ == "__main__":
  import sys
  import os
  sys.path.append("Helpers")
  import cardInfo as cardHelp
  import colouring
  import fileConstruct as construct
  import fileio
  import general
  import helperClasses as classes
  import printing
  import rowHelpers
  import searchAndReplace as sar
  import configHelpers as load
  import helperClasses
  import filters
  n = len(sys.argv)
  if n >= 2:
    choice = sys.argv[1]
  else:
    printing.printHelp()
  if n >= 3:
    args = sys.argv[2:]
  else:
    args = []
  if choice:
    chooseScript(choice, args)

