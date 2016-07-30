def minLoop(startAmount, annualInterestRate):
    aIR = annualInterestRate
    mIR = round((aIR/12.0),2)
    unpBal = startAmount
    #set the lower bound
    kLower = round((unpBal/12.0),2)
    #set the higher bound
    kUpper = round((unpBal*((1 + mIR)**12)/12.0),2)
    
    def remainingBalance(month,unpBal,aIR):
        remBal = unpBal + ((aIR/12.0) * unpBal)
        return round(remBal,2)

    def bisectGuess(kUpper,kLower):
        kGuess = round((((kUpper-kLower)/2.0)+ kLower),2)
        return kGuess
    
    count = 1
    while abs(unpBal) > 0.1:
         unpBal = startAmount
         kBuffer = bisectGuess(kUpper,kLower)
         fixedAmount = kBuffer
         print "Round: %d" % (count)
         print "Start amount: %s" % (str(startAmount))
         print "Fixed amount: %s" % (str(fixedAmount))
         for i in range(1,13):
             unpBal -= fixedAmount
             remBal = (remainingBalance(i,unpBal,aIR))
             unpBal = remBal
             print "Month %d:" % (i)
             print "Amount left: %s:" % (str(unpBal))
         print ("New fixed amount: %s" % (str(fixedAmount)))
         count += 1
         print("peich!")
         if unpBal > 0.1:
             kLower = fixedAmount
         elif unpBal < 0:
             kUpper = fixedAmount
         print(unpBal, kLower, kUpper, bisectGuess(kLower,kUpper))

#Works. Finally. Main problem was I did not realize negative values on
#the while loop would make it false, and therefore stop it.
