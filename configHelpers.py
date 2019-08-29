## Move the config to a separate directory
import helperClasses14 as helperClasses, helpers14 as helpers
import os

def getConfig():
  base = "config"
  return helperClasses.Config(readPartitionConfig(base), readColourConfig(base))

def getUpdateConfig():
  base = "update"
  if os.path.exists(base+"/config_part"):
    part = readPartitionConfig(base)
  else:
    part = None
  if os.path.exists(base+"/config_colour"):
    colour = readColourConfig(base)
  else: 
    colour = None
  return helperClasses.Config(part, colour)

def readPartitionConfig(base):
  configLines = helpers.readLines(base+"/config_part")
  for i in range(len(configLines)):
    configLines[i] = configLines[i].split(" ")
    for j in range(2):
      configLines[i][j] = int(configLines[i][j])
  return configLines

def readColourConfig(base):
  configLines = helpers.readLines(base+"/config_colour")
  configDicts = [{}]
  for line in configLines:
    if line == "":
      configDicts.append({})
      continue
    parts = line.split(" ")
    configDicts[-1][parts[0]] = parts[1]
  return configDicts

def setConfig(updateConfig, flag):
  config = getConfig()
  if updateConfig.partition:
    config.partition = updateConfig.partition
  if updateConfig.colour:
    config.colour = updateConfig.colour
  writeConfig(config, flag)

def writeConfig(config, flag):
  lines = []
  for line in config.partition:
    lines.append(helpers.addZeroes(line[0])+" "+helpers.addZeroes(line[1]))
  helpers.writeToFile("config/config_part", lines, flag)
  lines = []
  for section in config.colour:
    for line in section.keys():
      lines.append(line+" "+section[line])
    lines.append("")
  helpers.writeToFile("config/config_colour", lines[:-1], flag)
