import pandas as pd
from datetime import datetime
from collections import deque
import time
from dotenv import load_dotenv
import argparse


# TODO try to differentiate from dmy instead of american mdy using argparse?
# TODO use Objects in one dictionary



# lambda functions 
total = lambda quantity, price, discount: quantity * price * (1 - discount)
duplicateAccount = lambda key, dict: print(f"Duplicate Found: {key}") if key in dict else ''
existsDict = lambda key, dict: True if key in dict else False


"""
Create data objects here

data will be stored in objects using the following key value pair
{accountID : object}
"""

class account:
    def __init__(self, id, subId, subscripItems, ultParent, arr, hierArr):
        self.id = id
        self.subId = [subId]
        self.subscripItems = [subscripItems]
        self.ultParent = ultParent
        self.arr = arr
        self.hierArr = hierArr

    def getSub(self):
        return self.subId
    
    def setSubs(self, id):
        self.subId = id

    def getSubItems(self):
        return self.subscripItems
    
    def setSubItems(self, item):
        self.subscripItems.append(item)

    def getUltParent(self):
        return self.ultParent

    def getArr(self):
        return self.arr
    
    def getHierArr(self):
        return self.hierArr


"""
Compares given string date with today's date
to check if a subscription is still valid
"""
def countRevenue(startDate, endDate):
    today = datetime.now().date()
    endDateTime = datetime.strptime(endDate, '%Y-%m-%d').date()
    startDateTime = datetime.strptime(startDate, '%Y-%m-%d').date()
    if(today >= startDateTime and today <= endDateTime):
        # End date is today or in the future, Start date is today or past
        # subscription is NOT over
        return True
    else:
        # End date is in the past, subscription IS over
        # OR subscription hasn't started yet.
        return False


# go through accounts and add key value pairs
# {account id : object} to the dictionary
def sortAccounts(acctFile, dict):

    df = pd.read_csv(acctFile)

    for row in df.iterrows():
        # Check if account already exists in dict
        duplicateAccount(row['id'], dict)

        # Otherwise create a new account object and store in dictionary
        accountId = row['id']
        newAccount = account(accountId)
        dict[accountId] = newAccount

    print('Finished dict 1')
    return dict


# Return dict with {accountid : [list of subscriptions]}
def acctSubscriptions(subscriptionFile, dict):
    df2 = pd.read_csv(subscriptionFile)

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
        startDate = row['start_date']
        endDate = row['end_date']
        subtotal = 0

        if (quant == 0 or disc == 1 or countRevenue(startDate, endDate) == False):
            """
            If quantity = 0 OR discount = 1 OR subscription isn't over we can skip
            They either bought nothing OR it was free
            OR their subscription is not active
            """
            subtotal = 0
        elif(quant > 0 and disc < 1.0 and countRevenue(startDate, endDate) == True):
            # Otherwise subscription is active
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
def findChildren(d1):
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
def getHierarchyArr(accountId, arr, d2, d3, d4):
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
Make the 4 dictionaries and fill out
ultimate_parent, arr, hierarchy_arr 
using the helper methods above
""" 
def fillColumns(fp, fp2, fp3):
    dict1 = sortAccounts(fp)
    dict2 = acctSubscriptions(fp2)
    dict3 = moneyOwed(fp3)
    dict4 = findChildren(dict1)
    df5 = pd.read_csv(fp)

    for index, row in df5.iterrows():
        acctId = row['id']
        df5.loc[index, 'ultimate_parent_id'] = findUltParent(acctId, dict1)
        tempArr = getArr(acctId, dict2, dict3)
        df5.loc[index, 'arr'] = tempArr
        df5.loc[index, 'hierarchy_arr'] = getHierarchyArr(acctId, tempArr, dict2, dict3, dict4)

        #print(row['ultimate_parent_id'], row['arr'], row['hierarchy_arr'])
    
    #print(df5)

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
