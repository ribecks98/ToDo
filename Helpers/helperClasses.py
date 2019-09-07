## Add a state and a setStatus method for CardInfo
import fileio
import cardInfo

class CardInfo:
  card = -1
  line = ''
  row = []
  rowNum = -1
  partition = -1
  status = ""

  def __init__(self, card, line="", row=[], rowNum=-1, partition=-1):
    self.card = card
    self.line = line
    self.row = row
    self.partition = partition

  def __str__(self):
    string = "ID: "+ str(self.card) + "\n" \
    + "Line: " + self.line + "\n" \
    + "Status: " + self.status.__str__() + "\n"
    return string

  def setStatus(self, colourConfig):
    if self.row:
      self.status = cardInfo.getCardStatusFromRow(colourConfig,self.row)
    else:
      self.status = cardInfo.getCardStatus(colourConfig,self.line)

class State:
  complete = False
  status = "code"
  blocked = False

  def __init__(self, complete, status, blocked):
    if complete:
      self.complete = 1
    else: 
      self.complete = 0
    self.status = status
    self.blocked = blocked

  def convertToStatus(self):
    if self.blocked:
      return "blocked"
    else:
      return self.status

  def __str__(self):
    if self.complete:
      return "complete "+self.status
    return "incomplete "+self.status

class Config:
  partition = []
  colour = []
  templates = {}

  def __init__(self, partition=[], colour=[], templates={}):
    self.partition = partition
    self.colour = colour
    self.templates = templates
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
      if cardNumbers:
        theMax = max(cardNumbers)
        theMin = min(cardNumbers)
      else:
        theMin = 100000000
        theMax = 0
      if self.partition[0][0] > theMin:
        raise MessageError("The minimum value in the partition is larger than the smallest ID: " \
          +str(self.partition[0][0])+", "+str(theMin))
      if self.partition[-1][1] < theMax:
        raise MessageError("The maximum value in the partition is smaller than the largest ID: " \
          +str(self.partition[-1][1])+", "+str(theMax))
    except MessageError as err:
      print(err)
      raise

  def validateColour(self):
    cardTypes = sorted(self.templates.theList)
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

class Template:
  theList = []
  titleMap = {}
  archiveMap = {}

  def __init__(self, theList, titleMap, archiveMap):
    self.theList = theList
    self.titleMap = titleMap
    self.archiveMap = archiveMap

  def getList(self,complete):
    if complete:
      return ["done", "blocked"]
    else:
      return self.theList

  def getTitles(self,complete):
    if complete:
      return self.archiveMap
    else:
      return self.titleMap

  def __str__(self):
    return self.theList.__str__() + "\n" + self.titleMap.__str__() + "\n" + self.archiveMap.__str__()

class Error(Exception):
  pass

class MessageError(Error):
  message = ""
  def __init__(self, message=""):
    self.message = message

  def __str__(self):
    return "Error: " + self.message + "\n"
