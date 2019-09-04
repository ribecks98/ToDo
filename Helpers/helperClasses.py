## Add a state and a setStatus method for CardInfo
import fileio
import cardInfo

class CardInfo:
  card = -1
  line = ''
  row = []
  rowNum = -1
  partition = -1

  def __init__(self, card, line="", row=[], rowNum=-1, partition=-1):
    self.card = card
    self.line = line
    self.row = row
    self.partition = partition

  def setStatus(self, colourConfig, progressCards=[]):
    if progressCards == []:
      progressLines = fileio.readLines("bugs.md")
      template = fileio.readLines("cardTemplate.md")
      rows = rowHelpers.getRows(progressLines, template)
      for row in rows:
        progressCards.append(fileio.sortKey(row))

    complete = not self.card in progressCards
    self.status = State(complete, cardInfo.getCardType(colourConfig, self.line))

class Config:
  partition = []
  colour = []

  def __init__(self, partition=[], colour=[]):
    self.partition = partition
    self.colour = colour
    self.validate()

  def validate(self):
    self.validatePart()
    self.validateColour()

  def validatePart(self):
    if not self.partition:
      return
    try:
      for i in range(len(self.partition)-1):
        if self.partition[i+1][0] != self.partition[i][1] + 1:
          raise MessageError("Boundaries "+str(i)+" and "+str(i+1)+" are not one apart: "+ \
            str(self.partition[i][1])+", "+str(self.partition[i+1][0]))
      cardNumbers = cardInfo.getCardInfos(fileio.readLines("archive.md")).keys()
      theMin = min(cardNumbers)
      if self.partition[0][0] > theMin:
        raise MessageError("The minimum value in the partition is larger than the smallest ID: " \
          +str(self.partition[0][0])+", "+str(theMin))
      theMax = max(cardNumbers)
      if self.partition[-1][1] < theMax:
        raise MessageError("The maximum value in the partition is smaller than the largest ID: " \
          +str(self.partition[-1][1])+", "+str(theMax))
    except MessageError as err:
      print(err)
      raise

  def validateColour(self):
    cardTypes = sorted(["code","review","investigate","blocked"])
    try:
      for table in self.colour:
        if not sorted(table.keys()) == cardTypes:
          for thing in table.keys():
            if not thing in cardTypes:
              raise MessageError("Unrecognized colour: "+thing)
          raise MessageError("Not all the colours are included in the config file")
    except MessageError as err:
      print(err)
      raise

  def __str__(self):
    print(self.partition)
    print(self.colour)
    return ""

class State:
  complete = False
  status = "code"

  def __init__(self, complete, status):
    if complete:
      self.complete = 1
    else: 
      self.complete = 0
    self.status = status

  def __str__(self):
    if self.complete:
      return "complete "+self.status
    return "incomplete "+self.status

class Error(Exception):
  pass

class MessageError(Error):
  message = ""
  def __init__(self, message=""):
    self.message = message

  def __str__(self):
    return "Error: " + self.message + "\n"
