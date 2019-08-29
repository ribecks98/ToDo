## Make the CardLine class for easy look-ups

class CardLine:
  card = -1
  line = ''
  partition = -1

  def __init__(self, card=-1, line="", partition=-1):
    self.card = card
    self.line = line
    self.partition = partition
