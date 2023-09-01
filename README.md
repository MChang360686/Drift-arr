# Drift-arr
ARR for Drift coding challenge

Basic Premise - Keep track of Ultimate Parents using an Associative Array (Dict)

TODO
1) Write Python version
2) Make a flowchart graphic and add comments
3) Write a C version
4) Write script to compare results for Python and C
5) Write a Java version

Notes
- What if we have multiples of an account in accounts.csv?
- How do we tell which account is the ultimate parent, parent, or child?
- How do we sum up the money?
- What if we do this multiple times?
    - Search using Pandas?

Assumptions
- Each account is "unique" for the provided dataset
    - How do we deal with duplicates though?
        - Try catch finally?
        - Monads?
- Companies only pay when the subscription ends
    - Date is type str when we pull it from csv