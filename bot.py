import discord
import asyncio
import configparser
import random
import os.path

#variables ================================================
client = discord.Client()
EMOJI = "📌"

#functions ================================================
def locate_channel(guild, channelName):
    for chan in guild.channels:
        if chan.name == channelName:
            return chan
    return None

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def verify_dir(guild_id):
    dirname = "./guilds/" + str(guild_id)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    return dirname

def get_guild_emoji(guild_id):
    filename = "./guilds/" + str(guild_id)
    if os.path.exists(filename):
        file = open(filename, "r")
        
        emoji = file.read()
        print("retrieved emoji for server: " + emoji)
        return emoji
    else:
        print("No entry for this server")

    global EMOJI
    return EMOJI


#events ===================================================
@client.event
async def on_ready():
    global EMOJI
    print('logged in'.format(client))
    act = discord.Activity(type=discord.ActivityType.custom, name=EMOJI+"subscribe")
    await client.change_presence(activity=act)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global EMOJI

    # the mention string doesn't handle nickname mentions
    if message.content.startswith(client.user.mention) or message.content.startswith("<@!" + str(client.user.id) + ">"):
        if isinstance(message.channel, discord.DMChannel):
            await message.channel.send("I think this is a DM. You can't use this feature in DMs.")
        else:
            perms = message.author.permissions_in(message.channel)
            if perms.manage_guild:
                command = remove_prefix(remove_prefix(message.content, client.user.mention), "<@!" + str(client.user.id) + ">").strip()
                filename = "./guilds/" + str(message.channel.guild.id)

                if command.lower() == "reset":
                    if os.path.exists(filename):
                        os.remove(filename)
                        await message.channel.send("Reset emoji for this server.")
                    else:
                        await message.channel.send("There is nothing to reset!")
                elif len(command) > 0:
                    file = open(filename, "w")
                    file.write(command)
                    file.close
                    await message.channel.send("Set emoji on this server to " + command)
                    print("Set emoji on " + str(message.channel.guild.id) + " to " + command)

                else:
                    await message.channel.send("I can't do anything with empty commands.")
            else:
                await message.channel.send("You need Manage Server permission to do that.")

@client.event
async def on_raw_reaction_add(data):
    if data.emoji.name == get_guild_emoji(data.guild_id):
        guild = discord.utils.get(client.guilds, id=data.guild_id)
        channel = discord.utils.get(guild.channels, id=data.channel_id)
        message = await channel.fetch_message(data.message_id)
        member = discord.utils.get(guild.members, id=data.user_id)
        attachment_string = "**\n\nattachments:**"

        dm_channel = member.dm_channel
        if dm_channel == None:
            await member.create_dm()
            dm_channel = member.dm_channel
        await dm_channel.send("**==== NEW MESSAGE ====**\n" + message.content + attachment_string)

f=open("./token","r")
token = f.read().strip()
f.close()
client.run(token)

