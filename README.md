# Drift-arr
ARR for Drift coding challenge

Basic Premise - Keep track of Ultimate Parents using an Associative Array (Dict)

TODO
1) Write Python version
2) Make a flowchart graphic and add comments
3) Make a MySQL DB and compare
4) Write a C version
5) Write script to compare results for Python and C
6) Write a Java version


Assumptions
- Each account is "unique" for the provided dataset in accounts.csv
    - May not be the case for other datasets
- Companies are considered when the subscription is active
    - We're counting the money we are getting from them
    while the subscription is active as revenue
- for hierarchy_arr, I assume that it should be filled with
how much money the hierarchy INCLUDING the given account NOT
how much money the hierarchy as a WHOLE has made

Unit Tests
- Date - what if today is the deadline?
- Money - Are we getting the full amount?

Questions
- is if(statement): or if(statement == True): better? 