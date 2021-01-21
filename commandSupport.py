#--------------------------------------------------------
# commandSupport.py
# What it does: Some other functions which are used from time to time. To support commands.
# Dependencies: asyncio, datetime, pytz, dataStructs
#--------------------------------------------------------
import asyncio
import datetime
import pytz
from dataStructs import scheduleContainer

#Will occasionally sleep and let other processes take over, while it tries to wait for the designated time. May have problems that should be looked at later.
async def monitorTime(actualHours, actualMinutes,dayinTermsOfNum, timeZone, scheduleInfo, discordChannel):
  #Grab initial values of the time.
  t1 = datetime.datetime.now(pytz.timezone(timeZone))

  todayDay = t1.weekday()
  currentHour = t1.hour
  currentMinute = t1.minute

  #loop continuously until we reach the hour and minutes we are looking for.
  while((todayDay != dayinTermsOfNum) or (currentHour != actualHours) or (currentMinute != actualMinutes)):
    #Sleep for one second, before checking the current time again.
    await asyncio.sleep(1)

    t1 = datetime.datetime.now(pytz.timezone(timeZone))
    todayDay = t1.weekday()
    currentHour = t1.hour
    currentMinute = t1.minute

    
  print("Alarm Ended")
  print(scheduleInfo.gameTitle)
  #Alert the following discord users...
  discordMentionStr = ""
  primaryInfoStr = "\nTime for " + scheduleInfo.gameTitle
  for discordUser in scheduleInfo.memberList:
    discordMentionStr += discordUser.mention
  await discordChannel.send(discordMentionStr + primaryInfoStr)

  #Obtain user input on the game name in a single string.
def getUserInputtedGameName(args):
  buffer = ""
  #Piece together the arguments into one cohesive string
  for arg in args:
    buffer += (arg + " ")

  #Open the file and check if it is already in the list
  buffer = buffer.rstrip()
    
  return buffer
  
#Fill out a game list by reading a file. Removes new lines at the end of the line before doing so.
def getGameList(gameFile):
  gameList = []
  f = open(gameFile, "r")
  for line in f:
    tempstr = line.split('\n')
    gameList.append(tempstr[0])
  return gameList