import pandas as pd


# TODO figure out how to get the Parents IDs and figure out who the Ultimate Parent is
# TODO figure out how to append money to acct - make new lambda?
# TODO figure out how to check active subscriptions by getting the date in m/d/y with a lambda

# lambda functions 
add = lambda a, b: a + b
sub = lambda a, b: a - b
discount = lambda a, b: a * (1 - b)
existsInDict = lambda key, dict: print(f"Duplicate Found: {key}") if key in dict else ''



def sort(accts, subscrp, subscritems):
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

    print('Finished')
    pass


if __name__ == '__main__':
    filepath = "accounts.csv"
    fp2 = "subscriptions.csv"
    fp3 = "subscription_items.csv"


    sort(filepath, fp2, fp3)
