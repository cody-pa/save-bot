import discord
import asyncio
import configparser
import random
import os.path

#variables ================================================
client = discord.Client()
DEFAULT_EMOJI = "📌"

#functions ================================================
def locate_channel(guild, channelName):
    for chan in guild.channels:
        if chan.name == channelName:
            return chan
    return None

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

##def get_guild_emoji(guild_id):
 #   path="./guilds/" + str(guild_id) + "/emoji"
 #   if 

#events ===================================================
@client.event
async def on_ready():
    global DEFAULT_EMOJI
    print('logged in'.format(client))
    act = discord.Activity(type=discord.ActivityType.custom, name=DEFAULT_EMOJI+"subscribe")
    await client.change_presence(activity=act)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global DEFAULT_EMOJI
    command = message.content.strip().lower().replace(" ", "")

@client.event
async def on_raw_reaction_add(data):
    global DEFAULT_EMOJI
    if data.emoji.name == DEFAULT_EMOJI:
        filename = "./guilds/" + str(data.guild_id) + "/" + str(data.user_id)
        if os.path.exists(filename):
            guild = discord.utils.get(client.guilds, id=data.guild_id)
            channel = discord.utils.get(guild.channels, id=data.channel_id)
            message = await channel.fetch_message(data.message_id)
            member = discord.utils.get(guild.members, id=data.user_id)
            attachment_string = "**\n\nattachments:**"
            for attachment in message.attachments:
                attachment_string += '\n' + attachment.url

            dm_channel = member.dm_channel
            if dm_channel == None:
                await member.create_dm()
                dm_channel = member.dm_channel
            await dm_channel.send("**==== NEW MESSAGE ====**\n" + message.content + attachment_string)

        

f=open("./token","r")
token = f.read().strip()
f.close()
client.run(token)

