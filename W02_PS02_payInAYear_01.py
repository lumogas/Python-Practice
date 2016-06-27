#Update June 15, 2016: works now, though I still don't understand why
#I had to set the while loop to 1. It would run an extra time when set to 0

startAmount = 500
fixedAmount = 5
def testLoop(startAmount):
    leftAmount = startAmount
    fixedAmount = 0
    count = 1
    while leftAmount > 1:
        leftAmount = startAmount
        fixedAmount += round((leftAmount/120.0),2)
        print "Round: %d" % (count)
        print "Start amount: %d" % (startAmount)
        print "Fixed amount: %d" % (fixedAmount)
        for i in range(1,13):
            leftAmount -= fixedAmount
            print "Month %d:" % (i)
            print "Amount left: %d:" % (leftAmount)
        print ("New fixed amount: %d" % (fixedAmount))
        count += 1
