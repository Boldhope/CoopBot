#--------------------------------------------------------
# dataStructs.py
# What it does: Some data structures for the bot to use to interpret data like that for schedules.
# Dependencies: enums
#--------------------------------------------------------
import enum

#Days Enumeration for scheduler. I put it here since it's technically a "class"
class Days(enum.Enum):
  monday = 0
  tuesday = 1
  wednesday = 2
  thursday = 3
  friday = 4
  saturday = 5
  sunday = 6

#Class which is essentially a struct that carries information
class scheduleContainer:
    scheduledDate = ""
    gameTitle = "_"
    memberList = []
    #processID = 0
