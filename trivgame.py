class trivgame:
    def __init__(self, channel_ID):
        self.channel = channel_ID
        self.question_type = "Standard"
        self.question = "Test question"
        self.answers = ["test answer"]
        self.hints = ["Hints did not initialize correctly", 
                            "Hints did not initialize correctly 2",
                            "Hints did not initialize correctly 3"]
        
    def grab_new_question(self):
        return
        
    def check_answer(self, guess):
        return guess.lower() in self.answers
        
    def get_cur_quesiton(self):
        return self.question