from commandsupport import *
import discord
import enum
import os

#Days Enumeration for scheduler.
class Days(enum.Enum):
  monday = 0
  tuesday = 1
  wednesday = 2
  thursday = 3
  friday = 4
  saturday = 5
  sunday = 6

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
  
#Specify in terms of day (Mon, Tue, etc...), time (and AM/PM), and timezone.
#TO DO: MAKE IT PART OF TASKS, AS IT IS HARD TO KEEP TRACK OF THEM THE WAY THEY ARE CURRENTLY IMPLEMENTED.
async def scheduleTime(channel, args):

  #Place user arguments into day, time, am/pm, and timezone.
    dayOfWeek = args[0]
    timeOfDay = args[1]
    amOrPM = args[2]
    #Note there needs to be method that handles the time zone conversion for pytz. It can only handle UTC right now.
    timeZone = args[3]
    
    #Find out what day it is, for reference. Make this a separate function when done. Returns dayinTermsofNum for use later to find the day.
    dayinTermsOfNum = 0
    for day in Days:
      if(day.name == dayOfWeek.lower()):
        dayinTermsOfNum = day.value

    #Separate timeOfDay into hour and minutes
    actualTime = timeOfDay.split(':')
    actualMinutes = int(actualTime[1])
    actualTimeZone = timeZone.lower()
    
    #Figure out the actual hour offset, based on whether we are in PM or AM.
    timeOfDay = amOrPM.lower()
    if(timeOfDay == "am"):
      actualHours = int(actualTime[0])
    else:
      actualHours = int(actualTime[0]) + 12

    #Create a concurrent task to run, which will be awaited.
    await monitorTime(actualHours, actualMinutes, dayinTermsOfNum, actualTimeZone)


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
