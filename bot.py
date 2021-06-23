import discord
import credentials
import trivgame
import time
import random  #Random timer IDs

client = discord.Client()
channels = [855129476480761888]
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
            #Stop existing timers
            #Fetch new question
            #Start timer for next question to start

    if message.content.startswith(prefix+'hello'):
        await message.channel.send('Hello!')
        
    if message.content == prefix + 'start':
        if message.channel.id in games:
            await message.channel.send('Trivia is already running here!')
            return
        else:
            if message.channel.id not in channels:
                await message.channel.send('Sorry, trivia is not allowlisted in this channel at this time')
                return
            await message.channel.send('Loading trivia...')
            cur_game = trivgame.trivgame(message.channel)
            games[message.channel.id] = cur_game
            client.dispatch("new_question", cur_game)

@client.event
async def on_new_question(game):
    #Grab new question
    game.grab_new_question()
    #Send question text
    await game.channel.send(game.get_cur_quesiton())
    await game.channel.send(game.hints[0])
    #Queue hint timer
    timer_id = game.randomize_timer_id()
    time.sleep(10)
    client.dispatch("hint_timer", game, timer_id)

@client.event
async def on_hint_timer(game, timer_ID):
    #check if our timer is the current timer
    #if we haven't changed states, it will match
    #if we have, the ID won't match and we'll just throw the timer away
    print("Timer ran!")
    if timer_ID != game.current_timer:
        return
    await game.channel.send("This would be a hint")
    print("And passed our ID check!")
    

client.run(credentials.oauth2_token)