import pandas as pd
from datetime import datetime
from collections import deque
import time


# TODO fix setting children in findChildren() by making a second dictionary of {parent : [children]}



# lambda functions 
total = lambda quantity, price, discount: quantity * price * (1 - discount)
duplicateAccount = lambda key, dict: print(f"Duplicate Found: {key}") if key in dict else ''
existsDict = lambda key, dict: True if key in dict else False


"""
Create data objects here

data will be stored in objects using the following key value pair
{accountID : object}
"""

class Account:
    def __init__(self, id, subId, subscripItems, children, descendants, parent, ultParent, arr, hierArr):
        self.id = id
        self.subId = [subId]
        self.subscripItems = [subscripItems]
        self.children = [children]
        self.descendants = [descendants]
        self.parent = parent
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

    def getChildren(self):
        return self.children
    
    def setChildren(self, child):
        self.children.append(child)
    
    def getDescendants(self):
        return self.descendants
    
    def getParent(self):
        return self.parent
    
    def setParent(self, par):
        self.parent = par

    def getUltParent(self):
        return self.ultParent
    
    def getUltParent(self, ultPar):
        self.ultParent = ultPar

    def getArr(self):
        return self.arr
    
    def setArr(self, value):
        self.arr = value
    
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
# Additionally, create a temporary dict for later usage
# with {parent : [children]}
def sortAccounts(acctFile, dict):
    tempDict = {}
    parentAndChildren = {}
    df = pd.read_csv(acctFile)

    for index, row in df.iterrows():
        # Check if account already exists in dict
        #duplicateAccount(row['id'], dict)

        # Otherwise create a new account object and store in dictionary
        accountId = row['id']
        parent = row['parent_id']
        newAccount = Account(accountId, None, None, None, None, parent, '', 0, 0)
        dict[accountId] = newAccount

        tempDict[accountId] = parent

        # Next, check if the parent is in the dictionary parentAndChildren
        # If yes, add a new child to its list.  If no, add it

        if parent in parentAndChildren:
            parentAndChildren[parent].append(accountId)
        else:
            parentAndChildren[parent] = [accountId]

    
    for parent, children in parentAndChildren.items():
        if parent in tempDict.keys() and type(tempDict[parent]) == Account:
            for child in children:
                tempDict[parent].setChildren(child)
        

    print('Finished dict 1')
    return tempDict


# Go through subscriptions and check each account_id
# Then give each 
def acctSubscriptions(subscriptionFile, dict):
    df2 = pd.read_csv(subscriptionFile)

    for index, row in df2.iterrows():
        # Add items to dict
        subID = row['id']
        acctID = row['account_id']
        dict[acctID].setSubs(subID)

    print('Finished dict 2')


# Create subdict with subscriptionID: moneyOwed
# Then, append this information to original dictionary
def moneyOwed(subscriptionItemFile, dict):
    subdict = {}
    df3 = pd.read_csv(subscriptionItemFile)

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
        elif(countRevenue(startDate, endDate) == True):
            # Otherwise subscription is active
            subtotal = total(quant, prce, disc)

        # Append subtotal to dict
        if subID in subdict:
            subdict[subID] += subtotal
        else:
             subdict[subID] = subtotal

    # Now append this information to dict
    for key, value in dict.items():
        subscription = value.getSub()
        if subscription[0] == None:
            continue
        elif subscription in subdict:
            #print(subscription)
            subtotal = subdict[subscription]
            #print(subtotal)
            value.setArr(subdict[subscription])
                
        
    print('Finished dict 3')


"""
DFS is O(v+e), dict comprehension seems slow, we want to speed things up
Takes dict and gives each data object a list of children
"""
def findChildren(dict):
    
    for key, value in dict.items():
        if value.getParent() is None:
            # No parent, so account is its own child
            dict[key].setChild(key)
        else:
            # item has a parent, so it is parent's child
            #parentId = value.getParent()
            #dict[parentId].setParent(key)
            pass
    
    print("Finished dict 4")


"""
Searches for account in dictionary
with no parent id using temp dict from above
"""
def findUltParent(accountId, tempDict):
    childID = accountId
    knowParent = False

    while knowParent == False:
        if (tempDict[childID] == None or tempDict[childID] == '' or pd.isna(tempDict[childID])):
            # if value IS empty, return
            ultParent = childID
            knowParent = True
        else:
            # if value is NOT empty, get value from dict1 again
            childID = tempDict[childID]

    return ultParent


"""
Takes account_id and checks dict2 and dict3 to
return money owed aka arr using dictionary comprehension
"""
def getArr(accountId, dict):
    # Check if in dict
    if accountId in dict:
        arr = dict[accountId].getArr()
        #print(arr)

    return arr


"""
Takes account_id, arr, and checks dict1 - dict3
to find the amount of money made by the hierarchy
where account_id is the parent 
"""
def getHierarchyArr(accountId, arr, dict):
    hierarchyArr = arr

    # If list is empty, no children, return 
    # hierarchyArr = arr
    #if len(dict[accountId].getChildren()) > 0:
        
    #else:
    #    return hierarchyArr

    children = dict[accountId].getChildren()
    #print(children)

    # Otherwise BFS to check for children
    descendants = []
    visited = set()
    queue = deque(children)

    while queue:
        current_account = queue.popleft()
        #visited.add(current_account)

        if current_account == None:
            continue

        # add current child account's arr value
        # to hierarchyArr

        #print(current_account)

        if current_account in dict:
            hierarchyArr += dict[current_account].getArr()


        # Check if the account has children
        if len(dict[current_account].getChildren()) > 0:

            grandchildren =  dict[current_account].getChildren()

            # Add children to the queue if they haven't been visited
            for grandChild in grandchildren:
                if grandChild not in visited:
                    queue.append(grandChild)
                    descendants.append(grandChild)

    return hierarchyArr


"""
Make the dictionary and fill out
ultimate_parent, arr, hierarchy_arr 
using the helper methods above
""" 
def fillColumns(fp, fp2, fp3):
    dictionary = {}
    tempDict = sortAccounts(fp, dictionary)
    acctSubscriptions(fp2, dictionary)
    moneyOwed(fp3, dictionary)
    findChildren(dictionary)
    df5 = pd.read_csv(fp)

    for index, row in df5.iterrows():
        acctId = row['id']
        df5.loc[index, 'ultimate_parent_id'] = findUltParent(acctId, tempDict)
        tempArr = getArr(acctId, dictionary)
        df5.loc[index, 'arr'] = tempArr
        df5.loc[index, 'hierarchy_arr'] = getHierarchyArr(acctId, tempArr, dictionary)

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
