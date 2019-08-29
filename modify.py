## Added the ability to archive a card and made some changes to accommodate
## the changes in helpers

def addNotes(args):
  lines = helpers.readLines("bugs.md")
  template = helpers.readLines("cardTemplate.md")
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[0])
  if args[1] != "test":
    subprocess.run(["sed","-i",str(helpers.getTemplateLine(rows[rownum])+1)+"s/template/"+args[0]+"/","bugs.md"])
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

if __name__ == "__main__":
  import sys, helpers2 as helpers
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
        import subprocess
        addNotes(args)
        flag = 1
      if "d" in choice:
        deleteNotes(args)
        flag = 1
      if "r" in choice:
        archive(args)
        flag = 1
      if not flag:
        print(helpString)

