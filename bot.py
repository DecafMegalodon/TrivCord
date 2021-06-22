import discord
import credentials

client = discord.Client()
games = {}
prefix = "."

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:  #Don't respond to my own messages
        return
        
    if message.channel.id in games:  #The message was sent in a channel with an active game
        #Check answer
        print("Active channel")

    if message.content.startswith(prefix+'hello'):
        await message.channel.send('Hello!')
        
    if message.content == prefix + 'start':
        await message.channel.send('This is where I would put my trivia game... IF I HAD ONE')


client.run(credentials.oauth2_token)