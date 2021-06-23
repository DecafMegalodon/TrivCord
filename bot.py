import discord
import credentials
import trivgame
import time
import asyncio
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
            games[message.channel.id].game_state = "pre-question"
            client.dispatch("new_question", games[message.channel.id])

    if message.content.startswith(prefix+'hello'):
        await message.channel.send('Hello!')
        
    if message.content == prefix + 'start':
        if message.channel.id in games:
            await message.channel.send('Trivia is already running here!')
            return
        else:
            if message.channel.id not in channels:
                await message.channel.send('Sorry, trivia is not enabled in this channel at this time')
                return
            await message.channel.send('Loading trivia...')
            cur_game = trivgame.trivgame(message.channel)
            games[message.channel.id] = cur_game
            client.dispatch("new_question", cur_game, wait_time=0)

@client.event
async def on_new_question(game,  wait_time=10):
    await asyncio.sleep(wait_time)
    if game.trivia_state != "pre-question":
        await game.channel.send("Attempted to transition from " + game.trivia_state + " to question state invalidly")
        return
    game.trivia_state = "question"
    #Grab new question
    game.grab_new_question()
    #Send question text
    await game.channel.send(game.get_cur_quesiton())
    #And the hint
    client.dispatch("display_hint", game, wait_time=0)

@client.event
async def on_display_hint(game, wait_time=10):
    '''Display a hint, if we're in a quesiton state. Automatically advance hint number for next hint'''
    await asyncio.sleep(wait_time)
    if game.trivia_state != "question":
        return
    if game.current_hint == 3:  #Did we run out of time/hints?
        game.trivia_state = 'post-question'
        client.dispatch("question_over", game)
        return
        
    await game.channel.send("Hint %d: %s" % (game.current_hint + 1, game.hints[game.current_hint]))
    game.current_hint += 1
    client.dispatch("display_hint", game)

@client.event
async def on_question_over(game):
    #"Dang! We ran out of time without completing the question"
    if game.trivia_state != 'post-question':
        return
    game.trivia_state = 'pre-question'
    await game.channel.send("Womp womp. We didn't get the answer :slight_frown:")
    client.dispatch("new_question", game, 10)

client.run(credentials.oauth2_token)