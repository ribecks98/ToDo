## Add a function to add cards

def addNotes(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[0])
  lineNum = helpers.searchInRow("cards/template.md",rows[rownum])
  lines[lineNum] = lines[lineNum].replace("template",args[0])
  helpers.writeLines(helpers.outputFileName("bugs.md",args[1]), lines)
  if args[1] != "test":
    helpers.writeLines("cards/"+args[0]+".md",["[Back to Cards](../bugs.md)",""])

def deleteNotes(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  startLines = len(lines)
  rows = helpers.getRows(lines,template)
  rownum = helpers.getRowNum(rows,args[0])
  del lines[helpers.getTemplateLine(rows[rownum])]
  
  if args[1] == "test":
    fileName = "testOut.md"
  else: 
    fileName = "bugs.md"
  helpers.writeLines(fileName, lines)

def toQa(args):
  lines = helpers.readLines("bugs.md")
  startLines = len(lines)
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[0])
  rowGroups = helpers.getRowGroups(rows, lines)
  rowGroups[2].append(rows[rownum])
  helpers.deleteExcept(rows[rownum],rowGroups,[2])

  lines = helpers.constructFile(rowGroups)
  helpers.writeLines(helpers.outputFileName("bugs.md",args[1]), lines)

def archive(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[0])
  rowGroups = helpers.getRowGroups(rows, lines)
  row = rows[rownum]
  helpers.deleteExcept(row,rowGroups,[])
  row[0][2] = helpers.colourWrap(row[0][2], "green")

  lines = helpers.constructFile(rowGroups)
  helpers.writeLines(helpers.outputFileName("bugs.md",args[1]), lines)

  archiveFile = helpers.getArchiveFile(args[0])

  archiveLines = helpers.readLines(archiveFile)
  archiveRows = helpers.getRows(archiveLines, template)
  archiveRowGroups = helpers.getRowGroups(archiveRows, archiveLines, fileFlag="archive")
  archiveRowGroups[0].append(row)

  archiveLines = helpers.constructFile(archiveRowGroups,fileFlag="archive")
  helpers.writeLines(helpers.outputFileName(archiveFile,args[1]), archiveLines)

  indexLines = helpers.readLines("archive.md")
  line = helpers.searchLines(args[0], indexLines)
  indexLines[line] = indexLines[line].replace("fuchsia","#32a852")
  indexLines[line] = indexLines[line].replace("#ffab0f","#0c7528")
  helpers.writeLines(helpers.outputFileName("archive.md",args[1]), indexLines)

  notesFile = "cards/"+args[0]+".md"
  if os.path.exists(notesFile):
    notesLines = helpers.readLines(notesFile)
    notesLines[0] = "[Back to Subarchive](../"+archiveFile+")"
    helpers.writeLines(helpers.outputFileName(notesFile,args[1]), notesLines)

def addPR(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[0])
  row = rows[rownum]
  lineNum = helpers.searchInRow("pull/",row)
  lines[lineNum] = lines[lineNum].replace("pull/","pull/"+args[1])

  helpers.writeLines(helpers.outputFileName("bugs.md",args[2]), lines)

def addCard(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rowGroups = helpers.getRowGroups(rows, lines)
  newCard = [template[5:-2],0,0]
  helpers.replaceInLines("<cardNum>",args[0],newCard[0])
  if args[1] == 'code':
    del newCard[0][26:56]
    rowGroups[0].append(newCard)
    colour = "fuchsia"
  elif args[1] == "review":
    del newCard[0][6:26]
    rowGroups[1].append(newCard)
    colour = "#ffab0f"
  else:
    print(helpstring," [code,review]")

  description = input("Give a description for the card: ")
  helpers.replaceInLines("<description>",description,newCard[0])

  lines = helpers.constructFile(rowGroups)
  helpers.writeLines(helpers.outputFileName("bugs.md",args[2]), lines)

  indexLines = helpers.readLines("archive.md")
  lineNum = -1
  for i in range(len(indexLines)):
    match = helpers.getCardNum(indexLines[i])
    if match and int(match) > int(args[0]):
      lineNum = i
      break
  if lineNum < 0:
    lineNum = len(indexLines)
  indexLines.insert(lineNum,helpers.archiveLine(args[0], description, colour))
# helpers.writeLines(helpers.outputFileName("archive.md",args[2]), indexLines)

def test(args):
  print(helpers.getCardNum(">K12345<"))

if __name__ == "__main__":
  import sys, helpers4 as helpers
  helpString = "Usage: python modify.py [deleteNotes,addNotes,toQa] <cardNum>"
  if len(sys.argv) < 3:
    print(helpString)
  else:
    choice = sys.argv[1]
    args = sys.argv[2:]
    if choice[0] != "-":
      if choice == "toQa":
        toQa(args)
      elif choice == "addNotes":
        import subprocess
        addNotes(args)
      elif choice == "deleteNotes":
        deleteNotes(args)
      elif choice == "test":
        test(args)
      else:
        print(helpString)
    else:
      flag = 0
      if len(choice) > 2 and not "t" in choice:
        print("Can't have multiple choices")
        choice = "-"
      if "t" in choice:
        args.append("test")
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
          print(helpstring+" [code,review]")
        else:
          addCard(args)
          flag = 1
      if not flag:
        print(helpString)

