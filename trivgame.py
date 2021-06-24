import random
import re

questionlist = [("Let's Get Graphic: In 1987 this online company came up with the GIF, a graphics interchange format", "CompuServe"),
                        ("Which organization was awarded the Nobel Peace Prize during WW II", "the red cross"),
                        ("Science: What name is given to the effect that the Earth is gradually becoming warmer", "global warming"),
                        ("Canadian Capitals: Nova Scotia", "Halifax")]

class trivgame:
    def __init__(self, channel):
        self.channel = channel
        self.question_type = "Standard"
        self.question = "Test question"
        self.answers = ["test answer"]
        self.trivia_state = "pre-question"
        #  States (so far):
        #  "pre-question"
        #  "question"
        #  "post-question"
        self.questionDB = open('questions.txt', 'r').readlines()
        self.current_hint = 0
        self.hints = ["Hints have not been implemented yet", 
                            "Second hints haven't been implemented yet",
                            "This is a third hint"]
        
    def grab_new_question(self):
        answer_line = self.questionDB[random.randint(0,len(self.questionDB)-1)]
        self.question, self.answers = answer_line.split('*')
        self.answers = [self.answers.lower().strip()]
        ans = self.answers[0]  #Todo: Make this choose a random answer, if there's multiple
        self.hints[0] = re.sub(r'\S', '*', ans)
        
        #second hint
        hint = ''
        ratio = .3
        divider = int(len(ans) * ratio)
        divider = min(divider, 3)
        divider = min(divider, len(ans)-1)
        hint = ans[:divider]
        masked = ans[divider:]
        masked = re.sub(r'\S', '*', masked)
        hint += masked
    # hint = self.hint2 if self.hint2 != None else hint
        self.hints[1] = hint
        self.hints[2] = "(Testing mode) The answer is %s" % ans
        self.current_hint = 0
        
    def check_answer(self, guess):
        print(guess.lower(), self.answers)
        return guess.lower() in self.answers
        
    def get_cur_quesiton(self):
        return self.question
        
    def randomize_timer_id(self):
        self.current_timer = random.random()
        return self.current_timer