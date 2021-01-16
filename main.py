#--------------------------------------------------------
# main.py
# What it does: Some other functions which are used from time to time. To support commands.
# Dependencies: discord, os, executecommands.py, monitorProcess.py, commandsupport.py
#--------------------------------------------------------
import discord 
import os
from executeCommands import *
from monitorProcess import *
from commandSupport import getUserInputtedGameName
bot = discord.Client()
possibleCommands = ["listcoopgames", "addcoopgame", "schedule"]
possibleCommandDescriptions = ["", "", ""]

@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(command):
  if command.content.startswith('!'):
    #Split to get rid of the ! in front of our discord command
    commandStr = command.content.split('!')
    
    #Split command into various words
    args = commandStr[1].split(' ')
    
    #Grab the key discord command for the bot, and remove it from the list of arguments
    discordCommand = args[0]
    args.remove(discordCommand)
    
    #Check and perform a specific command.
    await checkCommand(discordCommand, command, args)

#Function will check the command to see which one was chosen (only checks simple commands)
async def checkCommand(discordCommand, commandProperties, args):
  #Grab the channel & user for the bot to send a message through
  discordChannel = commandProperties.channel
  discordUser = commandProperties.author

  #File names...
  tempFileName = "etc/temp.txt"
  gamesFile = "etc/games.txt"
    
  #For now, this class is a singleton, which I don't really fancy...it will be passed down from here to reduce its usage elsewhere (for easy removal).
  scheduleInstance = processMonitor.getInstance()

  #List all the possible commands we are able toi
  if(discordCommand == "help"):
    await listPossibleCommands()

  #List all coop games which are part of the coop game list. Can be added to.
  elif(discordCommand == "listcoopgames"):
    await listGames(discordChannel, gamesFile)

  #Allow user to add a coop game to the list
  elif(discordCommand == "addcoopgame"):
    gameName = getUserInputtedGameName(args)
    await addGame(discordChannel, gameName, gamesFile)

  #Remove a coop game from the list.
  elif (discordCommand == "removecoopgame"):
    gameName = getUserInputtedGameName(args)
    await removeGame(discordChannel, gameName, gamesFile, tempFileName)
  
  #Schedule coop game time for reminder
  #Take in people of group/time to alert
  elif(discordCommand == "schedule"):
    await scheduleTime(discordChannel, args, scheduleInstance)
  
  #Allow a user to join a particular schedule
  elif(discordCommand == "joinschedule"):
    await addMembertoSchedule(discordChannel,scheduleInstance, args[0], discordUser)

  #Allow a user to add a particular game to a schedule.
  elif(discordCommand == "addgametoschedule"):
    #Extract schedule ID and remove it from the list of earlier extracted arguments.
    scheduleID = args[len(args)-1]
    args.remove(scheduleID)
    
    #get full string of user input for the game name.
    gameName = getUserInputtedGameName(args)

    await addGametoSchedule(discordChannel, scheduleInstance, scheduleID, gameName)

  #List ongoing plans (schedules)
  elif(discordCommand == "listschedule"):
    await listSchedules(discordChannel, scheduleInstance)
  
  #Remove a schedule from the list
  elif(discordCommand == "removeschedule"):

    await removeSchedule(discordChannel, scheduleInstance, args[0])

  #Incorrect command was entered. Instruct the user to type !help for more information.
  else:
    await channel.send("Incorrect command, try entering !help for a list of commands")

bot.run(os.getenv('TOKEN'))