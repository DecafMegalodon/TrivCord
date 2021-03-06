import random
import re
from datetime import datetime

unmasked_chars = ",.\\/!@#$%^&()[]{};:'\" "
vowels = "aeiou"
mask_char = "*"
hint_ratio = .3  #The percent of characters to displayed for hint 2

class triviagame:
    def __init__(self, channel):
        self.channel = channel
        self.question_type = "standard"
        self.question = "Uninitialized question"
        self.answers = ["Uninitialized answer"]
        self.display_answer_index = 0 #The answer we're building hints off of. Possibly just one of many
        self.canonical_answers = ["Uninitialized"]
        self.game_state = "pre-question"
        self.question_start = None
        self.questionDB = open('questions.txt', 'r').readlines()  #Temporary until the full DB setup is available
        self.current_hint = 0  #The next time a hint is displayed, show this one
        self.hints = ["Uninit 1",
                            "Uninit 2",
                            "Uninit 3"]
        self.last_question_answered = datetime.now()
        
    def grab_new_question(self):
        answer_line = self.questionDB[random.randint(0,len(self.questionDB)-1)]
        star_split = answer_line.split('*')
        self.question = star_split[0]
        if self.question.startswith("KAOS"):
            self.question_type = "KAOS"
        else:
            self.question_type = "standard"
        self.answers = [ans.lower().strip() for ans in star_split[1:]]
        self.generate_hints()
        self.question_start = datetime.now()
        self.current_hint = 0
        self.canonical_answers = [canonicalize_answer(ans) for ans in self.answers]
        self.display_answer_index = random.randint(0, len(self.answers) - 1)
        
    def check_answer(self, guess):
        #todo: implement UOL
        canon_ans = canonicalize_answer(guess)
        correct = canon_ans in self.canonical_answers
        if correct:
            correct_index = self.answers.index(canon_ans)
            self.canonical_answers.pop(correct_index)
            self.answers.pop(correct_index)
            self.last_question_answered = datetime.now()
            [hints.pop(correct_index) for hints in self.hints]
        return correct
        
    def get_cur_quesiton(self):
        return self.question

    def generate_hints(self):
    #Todo: add per-question-type hints, as needed
        hint_answer = random.choice(self.answers)
        hint_all_1, hint_all_2, hint_all_3 = [], [], []
        for ans in self.answers:
            hint_1 = ''.join([char if char in unmasked_chars else mask_char
                                    for char in ans])
            hint_2_divider = min(int(len(ans) * hint_ratio),  #Show the first `hint_ratio` proportion of the answer
                                            3, len(ans) - 1)
            hint_2 = ans[:hint_2_divider]
            hint_2 += ''.join(hint_1[hint_2_divider:])
            hint_3 = hint_2[:hint_2_divider] + ''.join([char if char in unmasked_chars+vowels else mask_char  #Reveal vowels in the part not revealed by hint 2
                                                                                for char in ans[hint_2_divider:]])
            hint_all_1.append(hint_1)
            hint_all_2.append(hint_2)
            hint_all_3.append(hint_3)
        self.hints = [hint_all_1, hint_all_2, hint_all_3]
        
    async def send_new_question(self, client):
        if self.game_state != "pre-question":
            await self.channel.send("Hmm state weirdness" + str(self.game_state))
            return
            
        if (datetime.now() - self.last_question_answered).total_seconds() > 240:  # Todo: config
            await self.channel.send("Trivia is shutting down due to inactivity")
            self.game_state = "stopped"
            return

        self.grab_new_question()
        self.game_state = "question"
        await self.channel.send("%d: `%s`" % (random.randint(1,99), self.question))  #send question
        client.dispatch("display_hint", self, wait_time=0)
        
    async def send_hint(self, client):
        if self.game_state != "question":
            return
        if self.current_hint == 3:  #Did we run out of time/hints?
            self.game_state = 'post-question'
            client.dispatch("question_over", self)
            return
            
        hint_data = ""
        if self.question_type == "standard":
            hint_data = self.hints[self.current_hint][self.display_answer_index] 
        elif self.question_type == "KAOS":
            hint_data = "`, `".join(self.hints[self.current_hint])
            
        await self.channel.send("Hint %d: `%s`" % (self.current_hint + 1, hint_data))
        self.current_hint += 1
        client.dispatch("display_hint", self)

    async def send_question_missed(self, client):
        if self.game_state != 'post-question':
            await self.channel.send("Hmm state weirdness (oqm) " + str(self.game_state))
            return
        self.game_state = 'pre-question'
        if self.question_type == "standard":
            await self.channel.send("Time's up! The correct answer was `%s`" % self.answers[0])
        elif self.question_type == "KAOS":
            await self.channel.send("Time's up! The remaining answers were `%s`" % ", ".join(self.answers))
        client.dispatch("new_question", self, 10)

#Todo: consider stripping characters too
def canonicalize_answer(answer):
    return answer.lower()