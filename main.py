#--------------------------------------------------------
# main.py
# What it does: Some other functions which are used from time to time. To support commands.
# Dependencies: discord, os, executecommands.py, monitorProcess.py, commandsupport.py
#TO DO: New command that takes in argument membersin # to get which members are part of a specific schedule.
#--------------------------------------------------------
import discord 
import os
from executeCommands import *
from monitorProcess import *
from commandSupport import getUserInputtedGameName
bot = discord.Client()

botDict = {
  "help": listPossibleCommands,
  "listcoopgames": listGames,
  "addcoopgame": addGame,
  "removecoopgame": removeGame,
  "schedule": scheduleTime,
  "joinschedule": addMembertoSchedule,
  "addgametoschedule": addGametoSchedule,
  "listschedule": listSchedules,
  "removeschedule": removeSchedule,
}

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

  botFunction = botDict[discordCommand]

  await botFunction(discordChannel, discordUser, scheduleInstance, args, gamesFile, tempFileName)

bot.run(os.getenv('TOKEN'))