import discord
from discord.ext import commands
import asyncio
# import schedule  # read more about functionality
import time  # get proper syntax

bot = commands.Bot(command_prefix="!")


def timeName(name):  # converts the unit of time to it's multiple of seconds
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


def is_me(m):
    return m.author == bot.user


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event  # bruh moment
async def on_message(message):
    if message.author == bot.user:
        return
    if 'bruh' in message.content:
        await message.channel.send("look at this bruh moment")
        user = message.author
        role = discord.utils.get(user.guild.roles, name='bruh')
        await user.add_roles(role)
    await bot.process_commands(message)


@bot.command()  # adds the named role to a user
async def addRole(ctx, role):
    user = ctx.author
    role = discord.utils.get(user.guild.roles, name=role)
    await user.add_roles(role)
    await ctx.channel.send((str(user.display_name) + " has role " + str(role)))


@bot.command()  # clears up to 200 messages at once
async def clearMessages(ctx):
    deleted = await ctx.channel.purge(limit=200)
    await ctx.channel.send("Deleted {} message(s)".format(len(deleted)))
    await asyncio.sleep(5)
    await ctx.channel.purge(limit=1, check=is_me)


@bot.command()  # creates a role in the server, cannot create a role with special permissions
async def createRole(ctx, role):
    guild = ctx.Guild
    await guild.create_role(name=role)


@bot.command()  # sends a PM to the user that called the function
async def sendPM(ctx):
    user = ctx.author
    await user.create_dm()
    await user.dm_channel.send("It's me, your bot!")


@bot.command()  # sends a reminder to the user after a set amount of time
async def sendReminder(ctx, arg1, arg2, arg3):
    user = ctx.author
    timeDenominator = timeName(arg2)
    time = int(arg1) * timeDenominator
    message = str(arg3)
    await user.create_dm()
    await asyncio.sleep(time)
    await user.dm_channel.send(message)

@bot.command() #get an SCP article when given a number
async def getSCP(ctx, arg1):
    num = int(arg1)
    if num < 10:
        await ctx.channel.send("http://www.scp-wiki.net/scp-00" + str(num))
    elif num < 100:
        await ctx.channel.send("http://www.scp-wiki.net/scp-0" + str(num))
    else:
        await ctx.channel.send("http://www.scp-wiki.net/scp-" + str(num))


@bot.command()  # sends a messages to all users with a certain role
async def sendMassMessage(ctx, arg1, message):
    role = discord.utils.get(ctx.guild.roles, name=arg1)
    users = role.members
    for user in users:
        await user.create_dm()
        await user.dm_channel.send(message)


@bot.command()  # sends a reminder to all users with a certain role
async def sendMassReminder(ctx, time, unit, role, message):
    role = discord.utils.get(ctx.guild.roles, name=role)
    users = role.members
    unitNumber = timeName(unit)
    time = int(time) * unitNumber
    message = str(message)
    await asyncio.sleep(time)
    for user in users:
        await user.create_dm()
        await user.dm_channel.send(message)


# sets a meeting time, telling users of that role when the meeting is, reminding them 2 units before, and when the
# meeting starts
@bot.command()
async def setMeetingTime(ctx, t, denominator, role, meetingName):
    role = discord.utils.get(ctx.guild.roles, name=role)
    users = role.members
    host = ctx.author
    await host.create_dm()
    timeDenominator = timeName(denominator)
    time = int(t) * timeDenominator
    meetingName = str(meetingName)
    for user in users:
        await user.create_dm()
        msg = await user.dm_channel.send(str("You are signed up for " + str(meetingName) + " in " + str(t) + " " + str(
            denominator)) + ". Respond with 'not attending' to let the host know you cannont make it.")

        @bot.event
        async def on_message(message):
            if message.author == bot.user:
                return
            if 'not attending' in message.content:
                await user.dm_channel.send("Thank you for your response")
                await host.dm_channel.send(str(user) + " is unable to attend.")

    await asyncio.sleep(time - (2 * timeDenominator))
    for user in users:
        await user.create_dm()
        await user.dm_channel.send(meetingName + " starts in 2 " + denominator)
    await asyncio.sleep(2 * timeDenominator)
    for user in users:
        await user.create_dm()
        await user.dm_channel.send(meetingName + " is starting now")
    # TODO: turn meeting time into a time and date format, allow organizer to set a
    #  custom reminder date (2 hours before, but the meeting is scheduled in days), allow an organizer to use
    #  multiple units (meetings is in 2 hours and 30 minutes

    # TODO: Fix: Known bugs: after a user declines an invite, the bot will send the host their name and not the users
    #  name. If there is another meeting scheduled, you can't schedule a different one until the first is over


@bot.command()
async def react(ctx):
    message = ctx.message
    await message.add_reaction('👍')


bot.run('TOKEN')
# custom bot token, change to TOKEN before pushing

