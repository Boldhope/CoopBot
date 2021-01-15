from commandsupport import *
import discord
import enum
import os
from monitorProcess import *


#Open the games.txt file, and write out the list of coop games available.
async def listGames(channel, fileName):
  f = open(fileName)
  #Read each line in f for the game list into a buffer, and write out as one message
  buffer = "The list of games are as follows:\n"
  buffer += "```"
  for line in f:
    buffer += (line)
  buffer += "```"
  f.close()
  await channel.send(buffer)

#Take in args + channel to send to.
#Grab the list of games from games.txt first
#Then, create a single string for everything in *args
#Compare the string to what is available in the games.txt.
#If not part of that list, send updated list and confirmation that said game was added.
async def addGame(channel, args, fileName):
  
  #Declare/Initialize variables for use.
  buffer = getUserInputtedGameName(args)
  gameList = []
  #Fill out our game list
  f = open(fileName)
  for line in f:
    tempstr = line.split('\n')
    gameList.append(tempstr[0])
  

  #Check if the buffer exists already in our games.txt file array, or our gameList.
  if(buffer in gameList):
    await channel.send("This game is already in the list")
  else:
    e = open(fileName, "a")
    e.write("\n" + buffer)
    await channel.send(buffer + " has been added to the list.")
    e.close()
  f.close()

#List the schedules available, which were input by discord users.
async def listSchedules(channel, scheduleInstance):
  #Lists the schedules currently available.
  await channel.send(scheduleInstance.giveInfo())

#If there is not already another process waiting to get deleted, then request deletion for a given asynchronous object.
async def removeSchedule(channel, scheduleInstance, scheduleIdentifier):
  removalQueueSuccess = scheduleInstance.alertSchedule(scheduleIdentifier)
  if(removalQueueSuccess == True):
    await channel.send("Removal Request Success, removal is now pending...")
  else:
    await channel.send("Removal not possible at this time. Currently held by another process.")

#Specify in terms of day (Mon, Tue, etc...), time (and AM/PM), and timezone.
#TO DO: MAKE IT PART OF TASKS, AS IT IS HARD TO KEEP TRACK OF THEM THE WAY THEY ARE CURRENTLY IMPLEMENTED.
async def scheduleTime(channel, args, scheduleInstance):
  
  #Place user arguments into day, time, am/pm, and timezone.
  #Note there needs to be method that handles the time zone conversion for pytz. It can only handle UTC right now.
    dayOfWeek = args[0]
    timeOfDay = args[1]
    amOrPM = args[2]
    timeZone = args[3]
    
    #Create a concurrent task to run, which will be awaited.
    scheduleInstance.newSchedule(dayOfWeek, timeOfDay, amOrPM, timeZone)
    await channel.send("Schedule added...")
    # await monitorTime(actualHours, actualMinutes, dayinTermsOfNum, actualTimeZone, scheduleInstance, scheduleIdentifier)


#Print from the help.txt, which is preformatted with information
async def listPossibleCommands():
  print("Does Nothing")

#Must be able to prevent removal of a specific game, if there are still scheduler tasks running.
#Take the following format !removecoopgame <GameName>
#TO DO: MAKE TASKS OUT OF THE SCHEDULED EVENTS. PASS THEM IN HERE, AND CHECK IF THERE ARE ANY FOR A SPECIFIC GAME AND PREVENT REMOVAL IF THERE IS.
async def removeGame(channel, args, fileName, tempfileName):
  #Get user input
  userInput = getUserInputtedGameName(args)
  removalSuccessful = False
  #Open the respective files for read and write
  f = open(fileName)
  e = open(tempfileName, "w")

  #Check the games.txt line by line to find the game we want to remove.
  for line in f:
    tempstr = line.split('\n')
    #Output lines that do not correspond to the game we want to remove. Else, remove that line.
    if(tempstr[0] == userInput):
      removalSuccessful = True
    else:
      e.write(line)
  #Close the files.
  f.close()
  e.close()
  
  #Delete the previous file, games.txt, and rename temp.txt to games.txt.
  os.remove(fileName)
  os.rename(tempfileName, fileName)
  
  if(removalSuccessful):
    await channel.send("Successfully Removed " + userInput)
  else:
    await channel.send("Game does not exist...")
#Searches a game store for a list of games. Will only return one page at a time. Needs user input to return more than one page... (not sure how to do this at this time)
#TO DO: USE STEAM STORE PAGE AND TRACK DOWN GAMES ACCORDING TO THEIR TAGS, LIKE "COOP", "ACTION", ETC.
async def findGames():
  print("Does Nothing")
