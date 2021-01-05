import discord 
import os

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

  #Schedule coop game time for reminder
  #Take in people of group/time to alert
  elif(command == "schedule"):
    scheduleTime()

  elif(command == ""):
    print("...")

#Print from the help.txt, which is preformatted with information
def listPossibleCommands():
  print("Does nothing")

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
  
#Searches a game store for a list of games. Will only return one page at a time. Needs user input to return more than one page... (not sure how to do this at this time)
async def findGames():
  print("Does Nothing")

async def scheduleTime():
    print("Does nothing")

bot.run(os.getenv('TOKEN'))