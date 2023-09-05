import unittest
from arr import getHierarchyArr, countRevenue, getArr

"""
File for unit testing arr.py
"""


class testCountRevenue(unittest.TestCase):

    """
    What if we have Day/Month/Year dates instead of
    US style Month/Day/Year?
    """

    def testDates(self):
        date = '9/5/23' # 9/5/23 Sept 5th 2023
        date2 = '9/30/23'
        result = countRevenue(date, date2)
        expectedResult = True
        self.assertEqual(result, expectedResult)



class TestGetHierarchyArr(unittest.TestCase):

    """
    I keep getting grandchild  ['fcf7c377-b55f-44b8-a644-382712e377fe'],
    child  fcf7c377-b55f-44b8-a644-382712e377fe in an endless loop for 
    getHierarchyArr() in addition to non-existant keys throwing key errors.
    
    Probably a flaw in the logic

    NOTE: The function was extending child with a list of length 0, which led
    to infinite length

    Solution: Add 4th dictionary and refactor dict 2.  Then build around this.

    """
    def test_child_id_extension(self):
        # Define data, we want to call account 1
        # and its child, 1, who has subscriptions a, b, and c
        # worth 100, 200, and 300 respectively
        account_id = 1
        arr = 100
        d2 = {1: ['a', 'b', 'c'], 2: ['a', 'b'], 3: ['a']}
        d3 = {'a': 100, 'b': 200, 'c': 300}
        d4 = {1: [1], 2: [2], 3: [2, 3]}

        
        result = getHierarchyArr(account_id, arr, d2, d3, d4)

    
        expected_arr = 700  # 100 + 100 + 200 + 300
        self.assertEqual(result, expected_arr) 


class testGetArr(unittest.TestCase):

    """
    Check if getArr() is functional
    """

    def testArr(self):
        dict2 = {'a': ['b', 'c', 'd']}
        dict3 = {'b': 1200, 'c': 100, 'd': 500}
        result = getArr('a', dict2, dict3)
        expectedResult = 1800
        self.assertEqual(result, expectedResult)



if __name__ == '__main__':
    unittest.main()
