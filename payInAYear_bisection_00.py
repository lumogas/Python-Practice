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
        kGuess = round(((kUpper-kLower)/2.0),2)
        return kGuess
    
    count = 1
    # while unpBal > .1:
    #     unpBal = startAmount
    #     # fixedAmount += round((unpBal/120.0),2)
    #     fixedAmount = bisectGuess(kUpper,kLower)
    #     print "Round: %d" % (count)
    #     print "Start amount: %d" % (startAmount)
    #     print "Fixed amount: %d" % (fixedAmount)
    #     for i in range(1,13):
    #         unpBal -= fixedAmount
    #         remBal = (remainingBalance(i,unpBal,aIR))
    #         unpBal = remBal
    #         print "Month %d:" % (i)
    #         print "Amount left: %d:" % (unpBal)
    #     print ("New fixed amount: %d" % (fixedAmount))
    #     count += 1
    # return fixedAmount
    print kLower
    print kUpper
    print bisectGuess(kUpper,kLower)


    #run it through twelve months
    #is it too high? Adjust
    #is it too low? Adjust
    #July 26th, 2016: Got a working upper and lower bound, so far
