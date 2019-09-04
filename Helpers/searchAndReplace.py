def replaceInLines(target, string, lines):
  for i in range(len(lines)):
    lines[i] = lines[i].replace(target,string)

def searchInRow(string, row):
  return row[1] + searchLines(string, row[0])

## Searches a list of strings for an input string. Returns the line number if
## found and -1 if not
def searchLines(string, lines):
  for i in range(len(lines)):
    if string in lines[i]:
      return i
  return -1

def searchLinesHigh(string, lines):
  line = searchLines(string, lines)
  if line < 0:
    return len(lines)
  return line

