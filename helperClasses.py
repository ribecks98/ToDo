## Improve the CardLine class to make it a CardInfo class, and create a
## Config class for storing the whole config
import helpers14 as helpers

class CardInfo:
  line = ''
  row = []
  partition = -1

  def __init__(self, line="", row=[], partition=-1):
    self.line = line
    self.row = row
    self.partition = partition

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
