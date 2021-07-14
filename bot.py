import discord
import credentials
import triviatime
import time
import asyncio
import random  #Random timer IDs
from datetime import datetime
import triviatime

client = discord.Client()
trivia = triviatime.triviatime(client)
privs = [181457913490046976]  #Users with access to privledged commands
bot_prefix = "."

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:  #Don't respond to my own messages
        return
        
    await trivia.on_message(message)
    
    if message.content.startswith(bot_prefix+'hello'):
        await message.channel.send('Hello!')
        
    if message.content.startswith(bot_prefix+'start'):
        await trivia.start_game(message)

    if message.content.startswith(bot_prefix+'die'):
        if message.author.id in privs:
            await message.channel.send('Goodbye :(')
            await client.close()
        else:
            await message.channel.send("You haven't been given the privledges to use this command")
            

@client.event
async def on_message_edit(before, message):
    if message.author == client.user:  #Don't respond to my own messages
        return
    await trivia.on_message(message)

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
        
    hint_data = ""
    if game.question_type == "standard":
        hint_data = game.hints[game.current_hint][game.display_answer_index] 
    elif game.question_type == "KAOS":
        hint_data = "`, `".join(game.hints[game.current_hint])
        
    await game.channel.send("Hint %d: `%s`" % (game.current_hint + 1, hint_data))
    game.current_hint += 1
    client.dispatch("display_hint", game)

@client.event
async def on_question_over(game):
    #"Dang! We ran out of time without completing the question"
    if game.trivia_state != 'post-question':
        return
    game.trivia_state = 'pre-question'
    if game.question_type == "standard":
        await game.channel.send("Time's up! The correct answer was `%s`" % game.answers[0])
    elif game.question_type == "KAOS":
        await game.channel.send("Time's up! The remaining answers were `%s`" % game.answers)
    client.dispatch("new_question", game, 10)

client.run(credentials.oauth2_token)