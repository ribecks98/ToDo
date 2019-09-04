import re
import fileConstruct as construct

def archiveLine(cardNum, description, colour):
  return "- "+colourWrap("K"+cardNum, colour).strip()+" "+description

def colourWrap(string, colour):
  return "  <span style=\"color:" + colour + "\">" + string.strip() + "</span>"

def deleteExcept(row, rowGroups, toExclude):
  for i in range(len(toExclude)):
    toExclude[i] = toExclude[i] % len(rowGroups)
  for i in range(len(rowGroups)):
    if i in toExclude:
      continue
    if row in rowGroups[i]:
      rowGroups[i].remove(row)

def getArchiveFile(card, partitionConfig):
  for i in range(len(partitionConfig)):
    if int(card) >= partitionConfig[i][0] and int(card) <= partitionConfig[i][1]:
      archiveFile = "archive/" + construct.addZeroes(partitionConfig[i][0]) + "-" + construct.addZeroes(partitionConfig[i][1]) + ".md"
      break
  return archiveFile

def getArchiveIndex(card, partitionConfig):
  for i in range(len(partitionConfig)):
    if int(card) >= partitionConfig[i][0] and int(card) <= partitionConfig[i][1]:
      return i
  return -1

