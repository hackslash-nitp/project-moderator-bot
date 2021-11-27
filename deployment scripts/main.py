import discord
from discord.ext import commands
from predict import predictions


def execute():

 client = discord.Client()

 karma = {}
 db = {}

 if "responding" not in db.keys():
    db["responding"] = False


 @client.event
 async def on_ready():
    print('Logged in as {0.user} !'.format(client))


 @client.event
 async def on_message(message):
    if(message.author == client.user):
        return
    if(message.author not in karma.keys()):
        karma[message.author] = 0
    if message.content.startswith(">reset"):
        if message.author.has_permissions(administrator=True) :
           username = message.content.split(">reset ",1)[1]
           await message.channel.send("{0.user} karma has been reset !".format(username))
           karma[username.id] = 0
    if message.content.startswith(">hello"):
        await message.channel.send("Hello I am {0.user}!".format(client))
    if message.content.startswith(">responding"):
        value = message.content.split(">responding ", 1)[1]
        if(value.lower() == "true"):
            db["responding"] = True
            await message.channel.send("Responding is ON !")
        elif(value.lower() == "false"):
            db["responding"] = False
            await message.channel.send("Responding is OFF !")
        else:
            await message.channel.send("Invalid argumment passed with >Responding !")
    if db["responding"]:
        result_1, result_2 = predictions(message.content)
        if(result_1 is not None):
            karma[message.author] += 1
            if(karma[message.author] % 6 == 0):
                if(karma[message.author] == 12):
                    await message.channel.send("{0} has been banned !".format(message.author.name))
                    karma.pop(message.author)
                    await message.author.ban()
                    return
                await message.channel.send("{0} has been kicked !".format(message.author.name))
                await message.author.kick()
                return
            await message.channel.send("{0} has been warned for {1} and {2} total warning count is {3}!".format(message.author.name, result_1, result_2, karma[message.author]))
        else:
            return

 # 'key' is the generated discord client access token. 
 client.run(key)
 
if __name__=="__main__":
    execute()