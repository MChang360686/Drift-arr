import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import time
import argparse


# TODO figure out how to get the Parents IDs and figure out who the Ultimate Parent is
# TODO Make Pseudocode -> Make code for 2 new functions
# TODO how to differentiate from dmy instead of american mdy
# TODO unit testing


# lambda functions 
add = lambda a, b: a + b
sub = lambda a, b: a - b
total = lambda quantity, price, discount: quantity * price * (1 - discount)
duplicateAccount = lambda key, dict: print(f"Duplicate Found: {key}") if key in dict else ''
existsDict = lambda key, dict: True if key in dict else False

"""
Compares given string date with today's date
to check if a subscription is still valid
"""
def countRevenue(endDate):
    today = datetime.now().date()
    compareDate = datetime.strptime(endDate, '%Y-%m-%d').date()
    if(today <= compareDate):
        # End date is today or in the future subscription is NOT over
        return True
    elif(today > compareDate):
        # End date is in the past, subscription IS over
        return False


# Return dict with accountName : parentAccount
def sortAccounts(accts):
    acctAndPrnt = {}
    df = pd.read_csv(accts)

    for index, row in df.iterrows():
        # Check if account already exists in dict
        duplicateAccount(row['id'], acctAndPrnt)

        # Otherwise, just add items to dict
        acctID = row['id']
        parID = row['parent_id']
        acctAndPrnt[acctID] = parID

    print('Finished dict 1')
    return acctAndPrnt


# Return dict with subscriptionID: accountID
def acctSubscriptions(subscriptions):
    acctAndSubscription = {}
    df2 = pd.read_csv(subscriptions)

    for index, row in df2.iterrows():
        # Check if account already exists in dict
        duplicateAccount(row['id'], acctAndSubscription)

        # Otherwise, just add items to dict
        subID = row['id']
        acctID = row['account_id']
        acctAndSubscription[subID] = acctID

    print('Finished dict 2')
    return acctAndSubscription


# Return dict with subscriptionID: moneyOwed
def moneyOwed(subscriptionItems):
    subscriptionAndOwed = {}

    df3 = pd.read_csv(subscriptionItems)

    for index, row in df3.iterrows():
        #id = row['id']
        subID = row['subscription_id']
        quant = row['quantity']
        prce = row['list_price']
        disc = row['discount']
        endDate = row['end_date']
        subtotal = 0

        if (quant == 0 or disc == 1 or countRevenue(endDate) == False):
            """
            If quantity = 0 OR discount = 1 OR subscription isn't over we can skip
            They either bought nothing OR it was free
            OR their subscription is not active
            """
            subtotal = 0
        elif(quant > 0 and disc < 1.0):
            # 
            subtotal = total(quant, prce, disc)
        else:
            # Check negative quant and negative disc?
            print("3rd case in moneyOwed, Possible Error in Dataset")

        """
        Duplicates exist because some subscriptions get multiple items 
        Therefore, there needs to be a way to append money
        """

        if(existsDict(subID, subscriptionAndOwed) == True):
            # key/subscription exists in dict
            # We don't want to replace, we want to append
            subscriptionAndOwed[subID] += subtotal
        elif(existsDict(subID, subscriptionAndOwed) == False):
            # key/subscription does NOT exist in dict
            # Create a new one
            subscriptionAndOwed[subID] = subtotal

    print('Finished Dict 3')
    return subscriptionAndOwed


def findUltParent():
    pass

def getHierarchyArr():
    pass


"""
Make the 3 dictionaries and fill out
ultimate_parent, arr, hierarchy_arr 
using the helper methods
"""
def fillColumns(fp, fp2, fp3):
    dict1 = sortAccounts(fp)
    dict2 = acctSubscriptions(fp2)
    dict3 = moneyOwed(fp3)

    df4 = pd.read_csv(fp)

    for index, row in df4.iterows():
        pass
    # Finish by writing dataframe to csv
    df4.to_csv('solutions.csv', index=False)


if __name__ == '__main__':
    startTime = time.time()
    

    fp = "accounts.csv"
    fp2 = "subscriptions.csv"
    fp3 = "subscription_items.csv"

    fillColumns(fp, fp2, fp3)
    

    endTime = time.time()
    elapsedTime = endTime - startTime
    print(elapsedTime)
