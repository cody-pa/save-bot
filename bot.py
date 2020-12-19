import discord
import asyncio
import configparser
import random
import os.path

client = discord.Client(intents = discord.Intents.all())
EMOJI = "💾"

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
        print("No custom emoji for guild " + str(guild_id))

    global EMOJI
    return EMOJI

#events ===================================================
@client.event
async def on_ready():
    global EMOJI
    print('logged in'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=" pings."))

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
                    await message.channel.send("Server save emoji is " + get_guild_emoji(message.channel.guild.id) + '.\nServer admins can change it by pinging me followed by a new emoji (e.g `@DM-Save Bot :emoji:`), or reset it to default by pinging me followed by "reset" (e.g `@DM-Save Bot reset`)')
            else:
                await message.channel.send("You need Manage Server permission to do that.")

@client.event
async def on_raw_reaction_add(data):
    if data.emoji.name == get_guild_emoji(data.guild_id):
        print("\nReaction event fired.")
        guild = discord.utils.get(client.guilds, id=data.guild_id)
        print("Reaction occurred in guild: " + str(guild))
        channel = discord.utils.get(guild.channels, id=data.channel_id)
        print("In channel: " + str(channel))
        member = guild.get_member(data.user_id)
        print("Member: " + str(member))

        dm_channel = member.dm_channel
        if dm_channel == None:
            await member.create_dm()
            dm_channel = member.dm_channel
        
        message = await channel.fetch_message(data.message_id)
        attachment_string = ""
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                print("attachment: " + attachment.url)
                attachment_string += "\n" + attachment.url
        await dm_channel.send("**==== NEW MESSAGE ====**\n" + message.content + attachment_string)

f=open("./token","r")
token = f.read().strip()
f.close()
client.run(token)

