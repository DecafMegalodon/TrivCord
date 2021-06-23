import random

questionlist = [("Let'S Get Graphic: In 1987 this online company came up with the GIF, a graphics interchange format", "CompuServe"),
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
        self.current_hint = 0
        self.hints = ["Hints did not initialize correctly", 
                            "Hints did not initialize correctly 2",
                            "Hints did not initialize correctly 3"]
        
    def grab_new_question(self):
        rand_question_data = questionlist[random.randint(0,len(questionlist)-1)]
        self.question = rand_question_data[0]
        self.answers = [rand_question_data[1].lower()]
        self.current_hint = 0
        
    def check_answer(self, guess):
        return guess.lower() in self.answers
        
    def get_cur_quesiton(self):
        return self.question
        
    def randomize_timer_id(self):
        self.current_timer = random.random()
        return self.current_timer