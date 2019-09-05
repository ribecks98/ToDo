import searchAndReplace as sar

def replaceColour3(line,colour1,colour2):
  return line.replace("color:"+colour1,"color:"+colour2)

def replaceColour(card,colour1,colour2,lines):
  line = sar.searchLines(card+"<", lines)
  lines[line] = replaceColour3(lines[line],colour1,colour2)

def setColour(card,colour,lines,colours):
  for table in colours:
    for key in table.keys():
      replaceColour(card,table[key],colour,lines)

def updateColourByConfig(config, updateConfig, cardInfo):
  for key in config[0].keys():
    for i in range(len(config)):
      updateColour(config[i][key], updateConfig[i][key], cardInfo)

def updateColour(colour1, colour2, cardInfo):
  cardInfo.line = replaceColour3(cardInfo.line,colour1,colour2)
  for i in range(len(cardInfo.row[0])):
    cardInfo.row[0][i] = replaceColour3(cardInfo.row[0][i],colour1,colour2)

