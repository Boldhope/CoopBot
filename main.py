import discord 
import os
from executecommands import *

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
    
    #Grab the channel for the bot to send a message through
    channel = command.channel
    
    #Check and perform a specific command.
    await checkCommand(discordCommand, channel, args)

#Function will check the command to see which one was chosen (only checks simple commands)
async def checkCommand(command, channel, args):
  
  #List all the possible commands we are able toi
  if(command == "help"):
    listPossibleCommands()

  #List all coop games which are part of the coop game list. Can be added to.
  elif(command == "listcoopgames"):
    await listGames(channel)

  #Allow user to add a coop game to the list
  elif(command == "addcoopgame"):
    await addGame(channel, args)

  #Remove a coop game from the list. Requires you to have scheduled information removed, if it exists for the game, for it to be removed. TO DO.
  elif (command == "removecoopgame"):
    await removeGame(channel, args)
  
  #Schedule coop game time for reminder
  #Take in people of group/time to alert
  elif(command == "schedule"):
    await scheduleTime(channel, args)

  #Incorrect command was entered. Instruct the user to type !help for more information.
  else:
    await channel.send("Incorrect command, try entering !help for a list of commands")

bot.run(os.getenv('TOKEN'))