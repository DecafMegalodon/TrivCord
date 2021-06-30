import discord
import credentials
import trivgame
import time
import asyncio
import random  #Random timer IDs
from datetime import datetime

client = discord.Client()
channels = [855129476480761888, 857332550724091924]
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
        game = games[message.channel.id]
        if game.trivia_state == 'question' and game.check_answer(message.content):
            await message.channel.send("%s got the correct answer `%s` in %d seconds" % (
                                                            message.author,                    message.content, 
                                                            (datetime.now() - game.question_start).total_seconds() ))
            game.trivia_state = "pre-question"
            client.dispatch("new_question", game)
        if message.content.startswith(prefix+'stop'):
            game.trivia_state = "stopped"
            await message.channel.send('Trivia has been insta-stopped! :exploding_head:')

    if message.content.startswith(prefix+'hello'):
        await message.channel.send('Hello!')
        
    if message.content == prefix + 'start':
        if message.channel.id in games and games[message.channel.id].trivia_state != "stopped":
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
        #print("Unexpected state transition from %s to question" % game.trivia_state)
        return
    game.trivia_state = "question"
    game.grab_new_question()
    #Send question text
    await game.channel.send("%d: `%s`" % (random.randint(1,99), game.get_cur_quesiton()))
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
        
    await game.channel.send("Hint %d: `%s`" % (game.current_hint + 1, game.hints[game.current_hint]))
    game.current_hint += 1
    client.dispatch("display_hint", game)

@client.event
async def on_question_over(game):
    #"Dang! We ran out of time without completing the question"
    if game.trivia_state != 'post-question':
        return
    game.trivia_state = 'pre-question'
    await game.channel.send("Time's up! The correct answer was `%s`" % game.answers[0])
    client.dispatch("new_question", game, 10)

client.run(credentials.oauth2_token)