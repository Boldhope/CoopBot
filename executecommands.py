from commandsupport import *
import discord
import enum

class Days(enum.Enum):
  monday = 0
  tuesday = 1
  wednesday = 2
  thursday = 3
  friday = 4
  saturday = 5
  sunday = 6
#Open the games.txt file, and write out the list of coop games available.
async def listGames(channel):
  f = open("games.txt")
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
async def addGame(channel, args):
  
  #Declare/Initialize variables for use.
  buffer = ""
  gameList = []

  #Piece together the arguments into one cohesive string
  for arg in args:
    buffer += (arg + " ")

  #Open the file and check if it is already in the list
  buffer = buffer.rstrip()

  #Fill out our game list
  f = open("games.txt")
  for line in f:
    tempstr = line.split('\n')
    gameList.append(tempstr[0])
  

  #Check if the buffer exists already in our games.txt file array, or our gameList.
  if(buffer in gameList):
    await channel.send("This game is already in the list")
  else:
    e = open("games.txt", "a")
    e.write("\n" + buffer)
    await channel.send(buffer + " has been added to the list.")
    e.close()
  f.close()
  
#Specify in terms of day (Mon, Tue, etc...), time (and AM/PM), and timezone.
async def scheduleTime(channel, args):

  #Place user arguments into day, time, am/pm, and timezone.
    dayOfWeek = args[0]
    timeOfDay = args[1]
    amOrPM = args[2]
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
def listPossibleCommands():
  print("Does nothing")

#Searches a game store for a list of games. Will only return one page at a time. Needs user input to return more than one page... (not sure how to do this at this time)
async def findGames():
  print("Does Nothing")