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
        if games[message.channel.id].check_answer(message.content):
            await message.channel.send('That is the correct answer :partying_face: ')
        else:
            await message.channel.send('That was not the correct answer')

    if message.content.startswith(prefix+'hello'):
        await message.channel.send('Hello!')
        
    if message.content == prefix + 'start':
        if message.channel.id in games:
            await message.channel.send('Trivia is already running here!')
            return
        else:
            await message.channel.send('Loading trivia...')
            cur_game = trivgame.trivgame(message.channel.id)
            games[message.channel.id] = cur_game
            cur_game.grab_new_question()
            await message.channel.send(cur_game.get_cur_quesiton())


client.run(credentials.oauth2_token)