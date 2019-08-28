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
  qaLineNum = helpers.searchLines("In QA", lines)
  rows = helpers.getRows(lines, template)
  rownum = helpers.getRowNum(rows,args[0])
  rowGroups = helpers.getRowGroups(rows, lines)
  rowGroups[2].append(rows[rownum])
  helpers.deleteExcept(rows[rownum],rowGroups,[2])

  lines = helpers.constructFile(rowGroups)
  helpers.writeLines(helpers.outputFileName(args[1]), lines)

if __name__ == "__main__":
  import sys, helpers1 as helpers
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
      if "a" in choice:
        import subprocess
        addNotes(args)
        flag = 1
      if "d" in choice:
        deleteNotes(args)
        flag = 1
      if not flag:
        print(helpString)

