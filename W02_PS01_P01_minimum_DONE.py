"""Write a program to calculate the credit card balance after one year
if a person only pays the minimum monthly payment required by the credit
card company each month.
The following variables contain values as described below:

balance - the outstanding balance on the credit card

annualInterestRate - annual interest rate as a decimal

monthlyPaymentRate - minimum monthly payment rate as a decimal

For each month, calculate statements on the monthly payment and remaining
balance, and print to screen something of the format:

Month: 1
Minimum monthly payment: 96.0
Remaining balance: 4784.0

Be sure to print out no more than two decimal digits of accuracy - so print

Remaining balance: 813.41
instead of
Remaining balance: 813.4141998135

Finally, print out the total amount paid that year and the remaining balance
at the end of the year in the format:

Total paid: 96.0
Remaining balance: 4784.0

To help you get started, here is a rough outline of the stages you should
probably follow in writing your code:

    For each month:

    Compute the monthly payment, based on the previous month’s balance.

    Update the outstanding balance by removing the payment, then charging
interest on the result.

    Output the month, the minimum monthly payment and the remaining balance.

    Keep track of the total amount of paid over all the past months so far.

    Print out the result statement with the total amount paid and the
remaining balance.

Use these ideas to guide the creation of your code.

"""

def minimumPay(bal,annualInterestRate,monthlyPaymentRate):
    #variables!
   
    aIR = annualInterestRate
    mPR = monthlyPaymentRate

    #calculate the minimum monthly pay
    def minimumMonthly(bal):
        minMon = (bal * mPR)
        return round(minMon,2)

    #calculate the unpaid balance
    def unpaidBalance(bal, pBal):
        unpBal = bal - pBal
        return round(unpBal,2)

    #calculate the remaining balance
    def remainingBalance(month,unpBal,aIR):
        remBal = unpBal + ((aIR/12.0) * unpBal)
        return round(remBal,2)

    for kMonth in (range(1,13)):
        minMon = minimumMonthly(bal)
        unpBal = (bal - minMon)
        bal = unpBal + ((aIR/12.0)*bal)
        remBal = (remainingBalance(kMonth,unpBal,aIR))
        bal = remBal
       
        print #looks purty!
        print ("Month: %s") % str((kMonth))
        print ("Minimum monthly payment: %s") % (str(minMon))
        print ("Remaining balance: %s") % (str(remBal))

    print ("Total paid: %s") % (str(remBal))
    print ("Remaining balance: %s") % (str(remBal))

    #May 22nd, 2016: 'works', but seems to calculate wrongly
    #the minimumMon, and hence, the rest. So check minimumMonthly,
    #run it for the first month only, until you get a result that
    #matches the example.

