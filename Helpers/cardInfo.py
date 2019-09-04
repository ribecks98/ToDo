import helperClasses as helpers
import re

def getCardInfos(archiveLines):
  cardInfos = {}
  for line in archiveLines:
    card = getCardNum(line)
    if card and not "#####" in line:
      cardInfos[int(card)] = (helpers.CardInfo(int(card),line=line))
  return cardInfos

def getCardNum(line):
  match = re.search(">.*<", line)
  if match:
    return match.group(0)[2:-1]
  match = re.search("K[0-9]*", line)
  if match:
    return match.group(0)[1:]

def getCardType(colours, archiveLine):
  for key in colours[0].keys():
    for i in range(len(colours)):
      if colours[i][key] in archiveLine:
        return key

def getCardTypeFromRow(colours, row):
  for key in colours[0].keys():
    for i in range(len(colours)):
      if colours[i][key] in row[0][9]:
        return key
  

def getPartition(cardLines, config, exclude=False):
  count = 0
  partition = [[]]
  for card in sorted(cardLines.keys()):
    if not cardLines[card].status.complete and exclude:
      continue
    if card > config[count][1]:
      partition.append([])
      count = count + 1
    partition[-1].append(cardLines[card].line)
    cardLines[card].partition = count
  return partition

