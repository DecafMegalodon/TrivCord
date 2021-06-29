import random
import re
from datetime import datetime

unmasked_chars = ",.\\/!@#$%^&()[]{};:'\" "
vowels = "aeiou"
mask_char = "*"
hint_ratio = .3  #The percent of characters to displayed for hint 2

class trivgame:
    def __init__(self, channel):
        self.channel = channel
        self.question_type = "standard"
        self.question = "Uninitialized question"
        self.answers = ["Uninitialized answer"]
        self.display_answer = "unintitialized"  #The answer we're building hints off of. Possibly just one of many
        self.trivia_state = "pre-question"
        self.question_start = None
        #  States (so far):
        #  "pre-question"
        #  "question"
        #  "post-question"
        self.questionDB = open('questions.txt', 'r').readlines()  #Temporary until the full DB setup is available
        self.current_hint = 0  #The next time a hint is displayed, show this one
        self.hints = ["Uninit 1",
                            "Uninit 2",
                            "Uninit 3"]
        
    def grab_new_question(self):
        answer_line = self.questionDB[random.randint(0,len(self.questionDB)-1)]
        star_split = answer_line.split('*')
        self.question = star_split[0]
        self.answers = [ans.lower().strip() for ans in star_split[1:]]
        self.generate_hints()
        self.question_start = datetime.now()
        self.current_hint = 0
        
    def check_answer(self, guess):
        return guess.lower() in self.answers
        
    def get_cur_quesiton(self):
        return self.question

    def generate_hints(self):
        hint_answer = random.choice(self.answers)
        self.display_answer = hint_answer
        hint_1 = ''.join([char if char in unmasked_chars else mask_char
                                for char in hint_answer])
        hint_2_divider = min(int(len(hint_answer) * hint_ratio),
                                        3, len(hint_answer) - 1)
        hint_2 = hint_answer[:hint_2_divider]
        hint_2 += ''.join(hint_1[hint_2_divider:])
        hint_3 = hint_2[:hint_2_divider] + ''.join([char if char in unmasked_chars+vowels else mask_char 
                                                                            for char in hint_answer[hint_2_divider:]])
        self.hints = [hint_1, hint_2, hint_3]