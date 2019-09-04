import fileio

def addZeroes(num):
  string = str(num)
  while len(string) < 5:
    string = "0"+string
  return string

def constructArchiveFromInfos(archiveLines, cardInfos, config):
  partition = [[] for thing in config]
  for card in sorted(cardInfos.keys()):
    partition[cardInfos[card].partition].append(cardInfos[card].line)
  return constructArchiveFromPartition(archiveLines, partition, config)

def constructArchiveFromPartition(archiveLines, partition, config):
  archiveOut = archiveLines[:9]
  for i in range(len(config)):
    archiveOut.extend([constructArchiveLink(config[i]),""])
    archiveOut.extend(partition[i])
    archiveOut.append("")
  return archiveOut

def constructArchiveLink(configLine):
  start = addZeroes(configLine[0])
  end = addZeroes(configLine[1])
  return "##### [K" + start + "-K" + end + \
  "](archive/" + start + "-" + end + ".md)"

## Constructs the MarkDown file based from the row groups
def constructFile(rowGroups, fileFlag="bugs"):
  lines = getStartLines(fileFlag)
  titles = getTitles(fileFlag)
  for i in range(len(titles)):
    if rowGroups[i] != []:
      lines.extend(constructTable(rowGroups[i],titles[i]))
  return lines

def constructFileName(configLine):
  return addZeroes(configLine[0]) + "-" + addZeroes(configLine[1]) + ".md"

## Constructs a single table from the rows in it
def constructTable(rows, title):
  lines = ["", "## "+ title, "", "<table>", "  <tr><th>Bug</th><th>Checklist</th><th>Links</th>"]
  for row in sorted(rows,key=fileio.sortKey):
    lines.extend(row[0])
  lines.append("</table>")
  return lines

def getStartLines(fileFlag):
  if fileFlag == "bugs":
    return ["<title>Bug Checklists</title>","","[Back to Archive](archive.md)"]
  return ["<title>Bug Checklists</title>","","[Back to Archive](../archive.md)"]

def getTitles(fileFlag):
  bugTitles = ["In Progress", "Code Reviews", "Investigations", "In QA", "Blocked"]
  archiveTitles = ["Completed", "No Action Required"]
  if fileFlag == "bugs":
    return bugTitles
  else:
    return archiveTitles

