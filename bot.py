import discord
import credentials
import triviatime
import time
import asyncio
import random  #Random timer IDs
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
        client.dispatch("test", None)

    if message.content.startswith(bot_prefix+'stop'):
        await trivia.do_stop_trivia(message.channel)

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
    await trivia.on_message(message)  #Not a typo. Process it as if it's a new message

@client.event
async def on_new_question(game,  wait_time=10):
    await asyncio.sleep(wait_time)
    await game.send_new_question(client)

@client.event
async def on_display_hint(game, wait_time=10):
    '''Display a hint, if we're in a quesiton state. Automatically advance hint number for next hint'''
    await asyncio.sleep(wait_time)
    await game.send_hint(client)

@client.event
async def on_question_over(game):
    #"Dang! We ran out of time without completing the question"
    await game.send_question_missed(client)

client.run(credentials.oauth2_token)