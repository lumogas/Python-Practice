# coding: utf-8
#The program works as follows: you (the user) thinks of an integer between 0 (inclusive) and 100 (not 
#inclusive). The computer makes guesses, and you give it input - is its guess too high or too low? Using 
#bisection search, the computer will guess the user's secret number!

#Start with upper bound of 100, lower bound of 0
upperBound = 100
lowerBound = 0
kGuess = upperBound/2
solved = 0

#Ask the user whether the guess is accurate, three possible answers, 'l', 'h' or 'y'
def kAsk():
    kQuestion = "Is the number %s?" % (str(kGuess))
    x = raw_input(kQuestion)
    if x.lower() == "h": 
        lowerBound = kGuess
        kGuess += ((upperBound - lowerBound)/2)
    elif x.lower() == "l":
        upperBound = kGuess
        kGuess -= ((upperBound - lowerBound)/2)
    elif x.lower() == "y":
        solved = 1
    else:
        print("Please either type 'h','l', or 'y!'")
        kAsk()

print #looks purty!
print "Think of a number between 0 and 100!"

while solved != 1:
    kAsk()
    

print("Ok!")
print("The number was %s, then. Who knew?") % (kGuess)
#Vary upper and lower bounds accordingly until the answer is reached                
