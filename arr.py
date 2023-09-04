import pandas as pd
from datetime import datetime
from collections import deque
import time
from dotenv import load_dotenv
import argparse


# TODO how to differentiate from dmy instead of american mdy
# TODO unit test arr() and getHierarchyArr()



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


# Return dict with {accountid : [list of subscriptions]}
def acctSubscriptions(subscriptions):
    acctAndSubscriptions = {}
    df2 = pd.read_csv(subscriptions)

    for index, row in df2.iterrows():
        # Check if account already exists in dict
        duplicateAccount(row['id'], acctAndSubscriptions)

        # Otherwise, just add items to dict
        subID = row['id']
        acctID = row['account_id']

        if acctID not in acctAndSubscriptions:
            acctAndSubscriptions[acctID] = [subID]
        else:
            acctAndSubscriptions[acctID].append(subID)

    print('Finished dict 2')
    return acctAndSubscriptions


# Return dict with subscriptionID: moneyOwed
def moneyOwed(subscriptionItems):
    subscriptionAndOwed = {}

    df3 = pd.read_csv(subscriptionItems)

    for index, row in df3.iterrows():
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

    print('Finished dict 3')
    return subscriptionAndOwed


"""
Make a 4th dictionary that is the opposite of dict 1
DFS is O(v+e), dict comprehension seems slow, we want to speed things up
Takes dict 1 and makes a dict that is the complete opposite
{parent account id : [children]}
"""
def findChildren(d1, d2):
    parentAndChildren = {}
    
    for key, value in d1.items():
        if value is None:
            parentAndChildren[key].append(key)
        elif value not in parentAndChildren:
            parentAndChildren[value] = [key]
        else:
            parentAndChildren[value].append(key)
    
    print("Finished dict 4")
    return parentAndChildren


"""
Takes child account_id and dict1
returns ultimate parent
dict1 = {account_id : parent_id}
"""
def findUltParent(accountId, d):
    childID = accountId
    knowParent = False
    while knowParent == False:
        if (d[childID] == '' or pd.isna(d[childID]) == True or d[childID] == None):
            # if value IS empty, return
            parent = childID
            knowParent = True
        elif (d[childID] != '' or pd.isna(d[childID]) == False):
            # if value is NOT empty, get value from dict1 again
            childID = d[childID]

    return parent


"""
Takes account_id and checks dict2 and dict3 to
return money owed aka arr using dictionary comprehension
"""
def getArr(accountId, d2, d3):
    arr = 0
    try:
        # On the off chance that an account doesn't exist
        # in d2, just return arr = 0 because no subscription
        subId = d2[accountId]
    except KeyError:
        return arr
    
    for sub in subId:
        try:
            arr += d3[sub]
        except KeyError:
            pass

    return arr


"""
Takes account_id, arr, and checks dict1 - dict3
to find the amount of money made by the hierarchy
where account_id is the parent 
"""
def getHierarchyArr(accountId, arr, d1, d2, d3, d4):
    hierarchyArr = arr

    try:
        children = d4[accountId]
    except KeyError:
        # account is child, has no children
        # Therefore hierarchy_arr == arr 
        return hierarchyArr

    # BFS to check for children
    descendants = []
    visited = set()
    queue = deque(children)

    while queue:
        current_account = queue.popleft()
        visited.add(current_account)

        # add current child account's arr value
        # to hierarchyArr
        try:
            childSubscriptions = d2[current_account]

            for subscription in childSubscriptions:
                hierarchyArr += d3[subscription]
        except KeyError:
            continue

        # Check if the account has children
        if existsDict(current_account, d4):
            children = d4[current_account]

            # Add children to the queue if they haven't been visited
            for child in children:
                if child not in visited:
                    queue.append(child)
                    descendants.append(child)

    return hierarchyArr


"""
Make the 3 dictionaries and fill out
ultimate_parent, arr, hierarchy_arr 
using the helper methods above
"""
def fillColumns(fp, fp2, fp3):
    dict1 = sortAccounts(fp)
    dict2 = acctSubscriptions(fp2)
    dict3 = moneyOwed(fp3)
    dict4 = findChildren(dict1, dict2)
    df5 = pd.read_csv(fp)

    for index, row in df5.iterrows():
        acctId = row['id']
        df5.loc[index, 'ultimate_parent_id'] = findUltParent(acctId, dict1)
        df5.loc[index, 'arr'] = getArr(acctId, dict2, dict3)
        df5.loc[index, 'hierarchy_arr'] = getHierarchyArr(acctId, row['arr'], dict1, dict2, dict3, dict4)

        #print(row['ultimate_parent_id'], row['arr'], row['hierarchy_arr'])
    
    print(df5)

    # Finish by writing dataframe to csv
    df5.to_csv('solutions.csv', index=False, mode='w')


if __name__ == '__main__':
    startTime = time.time()
    
    fp = "accounts.csv"
    fp2 = "subscriptions.csv"
    fp3 = "subscription_items.csv"

    fillColumns(fp, fp2, fp3)

    endTime = time.time()
    elapsedTime = endTime - startTime
    print(elapsedTime)
