import discord
import triviagame
from datetime import datetime

class triviatime:
    channels = [855129476480761888, 857332550724091924]  #TODO: config this
    games = {}
    
    def __init__(self, client):
        self.client = client
    
    async def on_message(self, message):
        if message.channel.id not in triviatime.games or triviatime.games[message.channel.id].game_state != "question":
            return
        game = triviatime.games[message.channel.id]
        if game.check_answer(message.content):
            await message.channel.send("%s got the correct answer `%s` in %d seconds" % (
                                                            message.author,                    message.content, 
                                                            (datetime.now() - game.question_start).total_seconds() ))
            if game.question_type == "standard":
                game.game_state = "pre-question"
                self.client.dispatch("new_question", game)
                return
            if len(game.answers) == 0:  #We got all the answers in a KAOS
                await message.channel.send("That's all the answers for that KAOS!")
                game.game_state = "pre-question"
                self.client.dispatch("new_question", game)
                return
        
    async def start_game(self, message):
        if message.channel.id in triviatime.games and triviatime.games[message.channel.id].trivia_state != "stopped":
            await message.channel.send('Trivia is already running here!')
            return
        else:
            if message.channel.id not in triviatime.channels:
                await message.channel.send('Sorry, trivia is not enabled in this channel at this time')
                return
            await message.channel.send('Loading trivia...')
            new_game = triviagame.triviagame(message.channel)
            triviatime.games[message.channel.id] = new_game
            self.client.dispatch("new_question", new_game, wait_time=0)
        
    async def do_stop_trivia(self, channel_id):
        if channel_id in triviatime.games:
            game = triviatime.games[channel_id]
            if game.game_state != "stopped":
                await game.channel.send("Shutting down trivia")
                game.game_state = "stopped"
                return
        await game.channel.send("Trivia is already stopped!")
            