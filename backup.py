import discord
import asyncio
import configparser
import random
import os.path
import re
import urllib.request

master_id = 0
archive_path = ""
saved_path = ""
client = discord.Client(intents = discord.Intents.all())
prog = re.compile("(?P<url>https?://[^\s'\"]+)", re.MULTILINE|re.UNICODE)
nameprog = re.compile("(?=\w+\.\w{3,4}$).+")

def process_message_list(message):
    full_path = saved_path + "\\" + str(message.id)
    if not os.path.exists(full_path):
        urls = prog.findall(message.content)
        if len(urls) > 0:
            print("Message " + str(message.id))
            for url in urls:
                print("\tFetching " + url)
                try:
                    filename = archive_path + "\\" + nameprog.search(url).group(0)
                    print("\tsaving to " + filename)
                    
                    try:
                        req = urllib.request.Request(
                            url, 
                            data=None, 
                            headers={
                                'User-Agent': 'Mozilla/5.0'
                            }
                        )
                        f = open(filename, "wb")
                        f.write(urllib.request.urlopen(req).read())
                        f.close()

                    except Exception as e:
                        print("\tError: " + str(e))
                except:
                    print("\tNo filename for this url, cannot download")

        else:
            print("No content in " + str(message.id))
        
        # mark this file as already saved
        open(full_path, "a").close()
        return False
    else:
        print( "Message " + str(message.id) + " already archived")
    return True

@client.event
async def on_ready():
    #dm_chan = None

    print('Logged in'.format(client))

    print("My master's ID is: " + str(master_id))

    for guild in client.guilds:
        master_member = guild.get_member(master_id)
        if master_member != None:
            if master_member.dm_channel == None:
                await master_member.create_dm()

            print("DM channel: " + str(master_member.dm_channel))

            bef = None
            oldest = None
            done = False

            async for message in master_member.dm_channel.history(limit=1, oldest_first=True):
                oldest = message

            async for message in master_member.dm_channel.history(limit=1):
                done = process_message_list(message)
                bef = message

            while bef != oldest and not done:
                async for message in master_member.dm_channel.history(limit=10, before=bef):
                    done = process_message_list(message)
                    bef = message
                    if done:
                        break
            break
        
    print("Logging out.")
    await client.close()


if os.path.exists("./backup-data"):
    if os.path.exists("./token.backup"):
        f = open("./backup-data", "r")
        master_id = int(f.readline().strip())
        archive_path = f.readline().strip()
        f.close()

        if os.path.exists(archive_path):
            saved_path = archive_path + "\\saved"
            if not os.path.exists(saved_path):
                try:
                    os.mkdir(saved_path)
                except:
                    print("Creation of save dir inside archive path failed")

            if os.path.exists(saved_path):
                f=open("./token.backup","r")
                token = f.read().strip()
                f.close()
                client.run(token)
            else:
                print("Cannot track saved messages")
        else:
            print("Archive path invalid")
    else:
        print("No token file found in running directory!")
else:
    print("No backup-data found in running directory!")