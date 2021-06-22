import discord
import credentials
import trivgame

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

    if message.content.startswith(prefix+'hello'):
        await message.channel.send('Hello!')
        
    if message.content == prefix + 'start':
        if message.channel.id in games:
            await message.channel.send('Trivia is already running here!')
        else:
            games[message.channel.id] = trivgame.trivgame(message.channel.id)
            await message.channel.send('Loading trivia...')


client.run(credentials.oauth2_token)