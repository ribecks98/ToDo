def filter1(cardInfos):
  newCards = {}
  for card in cardInfos.keys():
    if not cardInfos[card].status.complete:
      newCards[card] = cardInfos[card]
  return newCards

def filter2(cardInfos,config):
  newCards = {}
  for card in cardInfos.keys():
    info = cardInfos[card]
    if info.status.complete and info.card >= config[0] and info.card < config[1]:
      newCards[card] = cardInfos[card]
  return newCards

