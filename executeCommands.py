#--------------------------------------------------------
# executecommands.py
# What it does: executes the commands for what is called by the user in main.py
# Dependencies: enum, discord, os, commandsupport.py, monitorProcess.py,
#Notes:TO DO: MAKE TASKS OUT OF THE SCHEDULED EVENTS. PASS THEM IN HERE, AND CHECK IF THERE ARE ANY FOR A SPECIFIC GAME AND PREVENT   #REMOVAL IF THERE IS. For removeGame
#TO DO: USE STEAM STORE PAGE AND TRACK DOWN GAMES ACCORDING TO THEIR TAGS, LIKE "COOP", "ACTION", ETC. for findGames
#--------------------------------------------------------
from commandSupport import *
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

#Determine whether game exists. If so, let user know it already exists. Else, display confirmation and add to the games.txt file
async def addGame(channel, gameName, fileName):
  
  #Declare/Initialize variables for use.
  gameList = []
  #Fill out our game list
  f = open(fileName)
  for line in f:
    tempstr = line.split('\n')
    gameList.append(tempstr[0])
  

  #Check if the game name exists already in our games.txt file array, or our gameList.
  if(gameName in gameList):
    await channel.send("This game is already in the list")
  else:
    e = open(fileName, "a")
    e.write("\n" + gameName)
    await channel.send(gameName + " has been added to the list.")
    e.close()
  f.close()

#List the schedules available, which were input by discord users.
async def listSchedules(channel, scheduleInstance):
  await channel.send(scheduleInstance.giveInfo())

#If there is not already another process waiting to get deleted, then request deletion for a given asynchronous object.
async def removeSchedule(channel, scheduleInstance, scheduleIdentifier):
  if(scheduleInstance.removeSchedule(scheduleIdentifier)):
    await channel.send("Schedule removal success.")

#Add method for the user to add a game to a particular schedule.
async def addGametoSchedule(channel, scheduleInstance, scheduleIdentifier, gameName):
  if(scheduleInstance.addGame(scheduleIdentifier, gameName)):
    await channel.send("Game added to the schedule.")
  else:
    await channel.send("Game already exists as a part of the schedule.")

#Add method for the user to add themselves to a particular schedule.
async def addMembertoSchedule(channel, scheduleInstance, scheduleIdentifier, memberName):
  scheduleInstance.addMember(scheduleIdentifier, memberName)

#Specify in terms of day (Mon, Tue, etc...), time (and AM/PM), and timezone.
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
async def removeGame(channel, userInput, fileName, tempfileName):

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
async def findGames():
  print("Does Nothing")
