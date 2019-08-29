## Add a state and a setStatus method for CardInfo
import helpers15 as helpers

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
      progressLines = helpers.readLines("bugs.md")
      template = helpers.readLines("cardTemplate.md")
      rows = helpers.getRows(progressLines, template)
      for row in rows:
        progressCards.append(helpers.sortKey(row))

    complete = not self.card in progressCards
    self.status = State(complete, helpers.getCardType(colourConfig, self.line))

class Config:
  partition = []
  colour = []

  def __init__(self, partition=[], colour={}):
    self.partition = partition
    self.colour = colour

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
