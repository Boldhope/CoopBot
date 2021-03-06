#--------------------------------------------------------
# executecommands.py
# What it does: Executes the commands for what is called by the user in main.py. Currently, they are encapsulated in generic methods that are defined by the bot dictionary in main.py. They are all asynchronous methods...
# Dependencies: enum, discord, os, commandsupport.py, monitorProcess.py,
#Notes:TO DO: MAKE TASKS OUT OF THE SCHEDULED EVENTS. PASS THEM IN HERE, AND CHECK IF THERE ARE ANY FOR A SPECIFIC GAME AND PREVENT REMOVAL IF THERE IS. For removeGame
#TO DO: USE STEAM STORE PAGE AND TRACK DOWN GAMES ACCORDING TO THEIR TAGS, LIKE "COOP", "ACTION", ETC. for findGames
#--------------------------------------------------------
import discord
import enum
import os
from monitorProcess import *
from commandSupport import *
from bs4 import BeautifulSoup, SoupStrainer
import requests

#Open the games.txt file, and write out the list of coop games available.
async def listGames(discordChannel, discordUser, scheduleInstance, args, gameFile, tempFileName):
  f = open(gameFile)
  #Read each line in f for the game list into a buffer, and write out as one message
  buffer = "The list of games are as follows:\n"
  buffer += "```"
  for line in f:
    buffer += (line)
  buffer += "```"
  f.close()
  await discordChannel.send(buffer)

#Determine whether game exists. If so, let user know it already exists. Else, display confirmation and add to the games.txt file
async def addGame(discordChannel, discordUser, scheduleInstance, args, gameFile, tempFileName):
  
  #Declare/Initialize variables for use.
  gameName = getUserInputtedGameName(args)
  
  #Get list of available games
  gameList = getGameList(gameFile)

  #Check if the game name exists already in our games.txt file array, or our gameList.
  if(gameName in gameList):
    await discordChannel.send("This game is already in the list")
  else:
    e = open(gameFile, "a")
    e.write("\n" + gameName)
    await discordChannel.send(gameName + " has been added to the list.")
    e.close()
  f.close()

#List the schedules available, which were input by discord users.
async def listSchedules(discordChannel, discordUser, scheduleInstance, args, gameFile, tempFileName):
  await discordChannel.send(scheduleInstance.giveInfo())

#If there is not already another process waiting to get deleted, then request deletion for a given asynchronous object.
async def removeSchedule(discordChannel, discordUser, scheduleInstance, args, gameFile, tempFileName):
  scheduleIdentifier = args[0]
  if(scheduleInstance.removeSchedule(scheduleIdentifier)):
    await discordChannel.send("Schedule removal success.")

#Add method for the user to add a game to a particular schedule. Check if the game is valid, then add the game to the scheduleInstance.
async def addGametoSchedule(discordChannel, discordUser, scheduleInstance, args, gameFile, tempFileName):
  scheduleIdentifier = args[len(args)-1]
  args.remove(scheduleIdentifier)
  gameName = getUserInputtedGameName(args)
  gameList = getGameList(gameFile)
  if (gameName in gameList):
    if(scheduleInstance.addGame(scheduleIdentifier, gameName)):
      await discordChannel.send("Game added to the schedule.")
    else:
      await discordChannel.send("Game already exists as a part of the schedule or this schedule does not exist.")
  else:
    await discordChannel.send("This game does not exist.")

#Add method for the user to add themselves to a particular schedule.
async def addMembertoSchedule(discordChannel, discordUser, scheduleInstance, args, gameFile, tempFileName):
  scheduleIdentifier = args[0]
  scheduleInstance.addMember(scheduleIdentifier, discordUser)
  await discordChannel.send(discordUser.display_name + " has successfully joined the schedule.")

#Specify in terms of day (Mon, Tue, etc...), time (and AM/PM), and timezone.
async def scheduleTime(discordChannel, discordUser, scheduleInstance, args, gameFile, tempFileName):
  
  #Place user arguments into day, time, am/pm, and timezone.
  #Note there needs to be method that handles the time zone conversion for pytz. It can only handle UTC right now.
    dayOfWeek = args[0]
    timeOfDay = args[1]
    amOrPM = args[2]
    timeZone = args[3]
    
    #Create a concurrent task to run, which will be awaited.
    scheduleInstance.newSchedule(dayOfWeek, timeOfDay, amOrPM, discordChannel, timeZone)
    await discordChannel.send("Schedule added...")
    # await monitorTime(actualHours, actualMinutes, dayinTermsOfNum, actualTimeZone, scheduleInstance, scheduleIdentifier)


#Print from the help.txt, which is preformatted with information
async def listPossibleCommands(discordChannel, discordUser, scheduleInstance, args, gameFile, tempFileName):
  print("Does Nothing")

#Must be able to prevent removal of a specific game, if there are still scheduler tasks running.
#Take the following format !removecoopgame <GameName>
async def removeGame(discordChannel, discordUser, scheduleInstance, args, gameFile, tempFileName):

  userInput = getUserInputtedGameName(args)
  removalSuccessful = False
  #Open the respective files for read and write
  f = open(gameFile)
  e = open(tempFileName, "w")

  #Check the games.txt line by line to find the game we want to remove.
  linesToAdd = ""
  lineCount = 0
  for line in f:
    lineCount += 1
    tempstr = line.split('\n')
    #Output lines that do not correspond to the game we want to remove (include a newline character at the beginning of the line if it is not initial line). Else, remove that line.
    if(tempstr[0] == userInput):
      removalSuccessful = True
    else:
      if(lineCount == 1):
        e.write(tempstr[0])
      else:
        e.write("\n" + tempstr[0])
  
  #Write to the temp file.
  e.write(linesToAdd)

  #Close the files.
  f.close()
  e.close()
  
  #Delete the previous file, games.txt, and rename temp.txt to games.txt.
  os.remove(gameFile)
  os.rename(tempFileName, gameFile)
  
  if(removalSuccessful):
    await discordChannel.send("Successfully Removed " + userInput)
  else:
    await discordChannel.send("Game does not exist...")
    
#Searches a game store for a list of games. Will only return one page at a time. Needs user input to return more than one page... (not sure how to do this at this time)
#Should make the user choose between different tags, and then go from there. Might want to make this a separate command, by using the command subclass rather than the regular client to truly use this. Would be nice if it can display all the games from a page, then ask the user if they want to continue looking for more games.
#Narrow the query down to the page we want to look at, say: https://store.steampowered.com/tags/en/Co-op/#p=0&tab=TopSellers
#Note issue where the page link for each page is correct, but it does not seem to pull the correct information
async def findGames(discordChannel, discordUser, scheduleInstance, args, gamesFile, tempFileName):
  basePage = "https://store.steampowered.com/"
  pageTag = "tags/en/" + "Co-op" + "/"
  currentPage = 0
  currentTab = "NewReleases"
  pageToGoTo = basePage + pageTag # + "#p=" + str(currentPage) + "&tab=" + currentTab
  numPages = range(5)
  steamGameList = []
  #Request the Webpage information, and store the information in soup object
  for i in numPages:
    pageToGoTo = basePage + pageTag  + "#p=" + str(i) + "&tab=" + currentTab  
    print(pageToGoTo)
    result = requests.get(pageToGoTo)
    steamGameList = returnInfo(result, currentTab)
  print(steamGameList)


  


