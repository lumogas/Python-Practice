def minLoop(startAmount, annualInterestRate):
    aIR = annualInterestRate
    def remainingBalance(month,unpBal,aIR):
        remBal = unpBal + ((aIR/12.0) * unpBal)
        return round(remBal,2)

    unpBal = startAmount
    fixedAmount = 0
    count = 1
    while unpBal > 1:
        unpBal = startAmount
        # fixedAmount += round((unpBal/120.0),2)
        fixedAmount += 10
        print "Round: %d" % (count)
        print "Start amount: %d" % (startAmount)
        print "Fixed amount: %d" % (fixedAmount)
        for i in range(1,13):
            unpBal -= fixedAmount
            remBal = (remainingBalance(i,unpBal,aIR))
            unpBal = remBal
            print "Month %d:" % (i)
            print "Amount left: %d:" % (unpBal)
        print ("New fixed amount: %d" % (fixedAmount))
        count += 1
    return fixedAmount

