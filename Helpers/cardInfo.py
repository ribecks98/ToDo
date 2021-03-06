import helperClasses as helpers
import re

def filterCards(cardInfos, cards):
  count = 0
  while count < len(cards):
    if not cardInfos[card].status.complete:
      del cards[count]
    else:
      count = count + 1

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
    return match.group(0)[3:-1]
  match = re.search("ID[0-9]*", line)
  if match:
    return match.group(0)[2:]

def getCardsInPartition(cardKeys, bounds):
  cards = []
  for card in cardKeys:
    if int(card) < bounds[0]:
      continue
    elif int(card) > bounds[1]:
      return cards
    cards.append(card)
  return cards

def getCardStatus(colours, archiveLine):
  for key in colours[0].keys():
    for i in range(len(colours)):
      if colours[i][key] in archiveLine:
        flag = i == 1
        flag2 = key == "blocked"
        return helpers.State(status=key,complete=flag,blocked=flag2)

def getCardStatusFromRow(colours, row):
  flag = False
  flag2 = False
  for key in colours[0].keys():
    for i in range(len(colours)-1,-1,-1):
      if colours[i][key] in row[0][2]:
        flag = i == 1
        flag2 = key == "blocked"
      if colours[i][key] in row[0][9]:
        status = key
  return helpers.State(status=status,complete=flag,blocked=flag2)
  
def getPartition(cardLines, config, exclude=False):
  count = 0
  partition = [[]]
  cardKeys = sorted([cardLines[card].card for card in cardLines.keys()])
  for bounds in config:
    cards = getCardsInPartition(cardKeys, bounds)
    if exclude:
      filterCards(cardLines,cards)
    partition.append([cardLines[card].line for card in cards])
    for card in cards:
      cardLines[card].partition = count
  return partition

