import discord
import triviagame

class triviatime:
    channels = [855129476480761888, 857332550724091924]  #TODO: config this
    games = {}
    
    def __init__(self, client)
        self.client = client
    
    def on_message(self, message):
        # if message.channel.id in games:  #The message was sent in a channel with an active game
            # game = games[message.channel.id]
            # if game.trivia_state == 'question' and game.check_answer(message.content):
                # await message.channel.send("%s got the correct answer `%s` in %d seconds" % (
                                                                # message.author,                    message.content, 
                                                                # (datetime.now() - game.question_start).total_seconds() ))
                # if game.question_type == "standard":
                    # game.trivia_state = "pre-question"
                    # client.dispatch("new_question", game)
                    # return
                # if len(game.answers) == 0:  #We got all the answers in a KAOS
                    # await message.channel.send("That's all the answers for that KAOS!")
                    # game.trivia_state = "pre-question"
                    # client.dispatch("new_question", game)
                    # return
        return
        
    def start_game(self)
    # if message.content == prefix + 'start':
        # if message.channel.id in games and games[message.channel.id].trivia_state != "stopped":
            # await message.channel.send('Trivia is already running here!')
            # return
        # else:
            # if message.channel.id not in channels:
                # await message.channel.send('Sorry, trivia is not enabled in this channel at this time')
                # return
            # await message.channel.send('Loading trivia...')
            # cur_game = trivgame.trivgame(message.channel)
            # games[message.channel.id] = cur_game
            # client.dispatch("new_question", cur_game, wait_time=0)