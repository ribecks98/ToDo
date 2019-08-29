devTable = { \
  "Dev To-Do": "#3dd49d", \
  "Design/Code Review": "#2979ff", \
  "QA Review": "#8f44ad" , \
}

reviewTable={ \
  "Design Review": "#ffab0f", \
  "Code Review": "#db4083" \
}

inProgressTable = { \
  "code" : "fuchsia", \
  "review" : "#ffab0f", \
  "investigate" : "#241ab8", \
  "blocked" : "#d91e31" \
}

completedTable={ \
  "code" : "#32a852", \
  "review" : "#0c7528", \
  "investigate" : "#85a900", \
  "blocked" : "#d91e31" \
}

def printDict(aDict):
  for key in aDict.keys():
    print(key,":",aDict[key])
  print("")

if __name__ == "__main__":
  print("Development colours:","\n")
  printDict(devTable)
  print("Review colours:","\n")
  printDict(reviewTable)
  print("In Progress colours:", "\n")
  printDict(inProgressTable)
  print("Completed colours:","\n")
  printDict(completedTable)
