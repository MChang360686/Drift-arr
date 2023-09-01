import pandas as pd
from datetime import datetime
from dotenv import load_dotenv


# TODO figure out how to get the Parents IDs and figure out who the Ultimate Parent is
# TODO how to differentiate from dmy instead of american mdy
# TODO Make Flowchart
# TODO Decide if I should make a 4th dictionary of ultimate parents to double check?


# lambda functions 
add = lambda a, b: a + b
sub = lambda a, b: a - b
total = lambda quantity, price, discount: quantity * price * (1 - discount)
existsInDict = lambda key, dict: print(f"Duplicate Found: {key}") if key in dict else ''

# Compares given string date with today's date
# to check if a subscription is still valid
def subscrpOver(endDate):
    today = datetime.now().date()
    compareDate = datetime.strptime(endDate, '%Y-%m-%d').date()
    print(today, compareDate)
    if(today < compareDate):
        # subscription end date is in the future
        # subscription is NOT over
        return False
    else:
        # subscription end date is past or today
        # subscription IS over
        # parent/child owes money
        return True


# Return dict with accountName : parentAccount
def sort(accts):
    acctAndPrnt = {}
    df = pd.read_csv(accts)

    # First add everything to a dict so access time is O(1)
    for index, row in df.iterrows():
        # Check if already exists in dict
        existsInDict(row['id'], acctAndPrnt)

        # Otherwise, just add items to dict
        acctID = row['id']
        parID = row['parent_id']
        acctAndPrnt[acctID] = parID

    print('Finished dict 1')
    return acctAndPrnt


# Return dict with accountName: subscriptionID
def acctSubscriptions(subscritems):
    acctAndSubscription = {}
    df = pd.read_csv()
    # If quantity = 0 OR discount = 1 we can skip
    # They either bought nothing OR it was free
    #if (quant == 0 or disc == 1):
    #    pass
    # Check if 
    #elif(quant > 0 and disc < 1.0):
    #    return total(quant, prce, disc)

    print('Finished dict 2')
    return acctAndSubscription


# Return dict with subscriptionID: moneyOwed
def moneyOwed():
    subscriptionAndOwed = {}
    print('Finished Dict 3')
    return subscriptionAndOwed


if __name__ == '__main__':
    filepath = "accounts.csv"
    fp2 = "subscriptions.csv"
    fp3 = "subscription_items.csv"
    #sort(filepath, fp2, fp3)
    
    df = pd.read_csv("subscriptions.csv")
    line = df.iloc[1]
    end = line['end_date']
    print(subscrpOver(end))
