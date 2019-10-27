import discord
from discord.ext import commands
import asyncio
import schedule #read more about functionality
import time #get proper syntax

bot = commands.Bot(command_prefix = "!")

def timeName(name): #converts the unit of time to it's multiple of seconds
  if name == 'hour' or name == 'hours':
    return 3600
  if name == 'minute' or name == 'minutes':
    return 60
  if name == 'day' or name == 'days':
    return 86400
  if name == 'week' or name == 'weeks':
    return 604800
  if name == 'month' or name == 'months':
    return 18144000
  if name == 'second' or name == 'seconds':
    return 1

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.command() #adds the named role to a user
async def addrole(ctx, role):
  user = ctx.author
  role = discord.utils.get(user.guild.roles, name = role)
  await user.add_roles(role)
  await ctx.channel.send((str(user.display_name) + " has role " + str(role)))

@bot.command() #clears up to 2000 messages at once, takes a while however
async def clearMessages(ctx): #TODO: optimize to speed up message cleanup
  messages = await ctx.channel.history(limit = 2000).flatten()
  for i in messages:
    await i.delete()

@bot.command() #creates a role in the server, cannot create a role with special permisions
async def createRole(ctx, role):
  guild = ctx.Guild
  await guild.create_role(name = role)


@bot.command() #sends a PM to the user that called the function
async def sendPM(ctx):
  user = ctx.author
  await user.create_dm()
  await user.dm_channel.send("It's me, Matt!")

@bot.command() #sends a reminder to the user after a set amount of time
async def sendReminder(ctx, arg1, arg2, arg3):
  user = ctx.author
  timeDenominator = timeName(arg2)
  time = int(arg1)*timeDenominator
  message = str(arg3)
  await user.create_dm()
  await asyncio.sleep(time)
  await user.dm_channel.send(message)

@bot.command() #sends a messaget to all users with a certain role 
async def sendMassMessage(ctx, arg1, message):
  role = discord.utils.get(ctx.guild.roles, name = arg1)
  users = role.members
  for user in users:
    await user.create_dm()
    await user.dm_channel.send(message)

@bot.command() #sends a reminder to all users with a certain role
async def sendMassReminder(ctx, time, unit, role, message):
  role = discord.utils.get(ctx.guild.roles, name = role)
  users = role.members
  unitNumber = timeName(unit)
  time = int(time)*unitNumber
  message = str(message)
  await asyncio.sleep(time)
  for user in users:
    await user.create_dm()
    await user.dm_channel.send(message)

@bot.command() #sets a meeting time, telling users of that role when the meeting is, reminding them 2 units before, and when the meeting starts
async def setMeetingTime(ctx, t, denominator, role, meetingName):
  role = discord.utils.get(ctx.guild.roles, name = role)
  users = role.members
  timeDenominator = timeName(denominator)
  time = int(t)*timeDenominator
  meetingName = str(meetingName)
  for user in users:
    await user.create_dm()
    await user.dm_channel.send(str("You are signed up for " + str(meetingName) + " in " + str(t) + " " + str(denominator)))
  await asyncio.sleep(time-(2*timeDenominator))
  for user in users:
    await user.create_dm()
    await user.dm_channel.send(meetingName + " starts in 2 " + denominator)
  await asyncio.sleep(2*timeDenominator)
  for user in users:
    await user.create_dm()
    await user.dm_channel.send(meetingName + " is starting now")
  #TODO: turn meeting time into a time and date format, allow users to decline a meeting, allow organizer to set a custom reminder date (2 hours before, but the meeting is scheduled in days), allow an organizer to use multiple units (meetings is in 2 hours and 30 minutes) 


bot.run('TOKEN')
