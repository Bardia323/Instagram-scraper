from random import randint
from time import sleep
class ExGen:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generateComment(self):
        A = ['what a ','such a ','Wow! ', 'Beautiful! ', "<3 ", ":O ", 'O.O ', 'damn! ', 'Nice! ', 'Damn! ', 'Absolutely ', '😍😍😍 ', '❤️❤️ ',  'woooww ']
        B = ['Stunning ', 'beautiful ','fantastic ','wonderful ','gorgeus ', 'inspiring ', 'profound ', 'exquisite ', 'awestrucking ', 'awesome ', 'holy ', 'dreamy ', 'Amazing ', 'lovely ', 'incredible ', 'spectacular ',]
        C = ['photo ','image ', 'view ', 'imagery ', 'sight ', 'beauty ', 'wonder ', 'pic ', 'picture '] 
        D = [ 'to behold', 'to put in perspective', ', I\'m enjoying a lot', '...me gusta', '...I like it', ', I love it']
        E = ['!!!', '!' '...!', '.', '...', ' <3', ' ^v^', '..', '!!', '❤️❤️❤️', '😍❤️', '😍😍']
        cat = [A,B,C,D, E]

        p = randint(0,100)
        if (p > 65 & p<= 75):            
            return cat[1][randint(0,len(cat[1])-1)] + cat[2][randint(0,len(cat[2])-1)] + cat[4][randint(0,len(cat[4])-1)]
        elif (p >75 & p<= 80):
            return cat[1][randint(0,len(cat[1])-1)] + cat[2][randint(0,len(cat[2])-1)]+ cat[3][randint(0,len(cat[3])-1)]+ cat[4][randint(0,len(cat[4])-1)]
        elif (p > 80 & p <=90):
            return  cat[0][randint(0,len(cat[0])-1)] + cat[1][randint(0,len(cat[1])-1)] + cat[2][randint(0,len(cat[2])-1)]+ cat[3][randint(0,len(cat[3])-1)]+ cat[4][randint(0,len(cat[4])-1)]
        elif (p > 90):
            return cat[0][randint(0,len(cat[0])-1)] + cat[1][randint(0,len(cat[1])-1)] + cat[2][randint(0,len(cat[2])-1)]+ cat[4][randint(0,len(cat[4])-1)]
        elif (p <= 65):
            return cat[1][randint(0,len(cat[1])-1)] + cat[4][randint(0,len(cat[4])-1)]

    def generateCaption():
        Greet = ["Hello, ", "Hey ", "Good Morning, ", "Another Beautiful Day, ", "Another Lovely Morning, "]
        My = ["My ", "my ", '', '' , '']
        Adj = ["", "Awesome", 'Free', 'Lovely', 'Dear', 'Wonderful', 'Amazing', 'Fabulous', "Curious"]
        Them = ["Followers", "Friends", "Chaps", "ladies and gentlemen", 'fellows', 'friend', 'follower']
        Address = [My + Adj + Them]

        #Today's destination is [Location]
        #The language spoken here is [language]
        # currently the weather is [weather] degrees c/f
        # 
        # 
if (__name__ == "__main__"):
    t = ExGen()

    for i in range(200):
       
        print(t.generateComment())
        sleep(1)