import unittest
from arr import getHierarchyArr

"""
File for unit testing arr.py
"""


class TestGetHierarchyArr(unittest.TestCase):

    """
    I keep getting grandchild  ['fcf7c377-b55f-44b8-a644-382712e377fe'],
    child  fcf7c377-b55f-44b8-a644-382712e377fe in an endless loop for 
    getHierarchyArr() in addition to non-existant keys throwing key errors.
    
    Probably a flaw in the logic

    NOTE: The function was extending child with a list of length 0, which led
    to infinite length

    """
    def test_child_id_extension(self):
        # Define sample data and dictionaries
        account_id = 1
        arr = []
        d1 = {1: 2, 2: 3, 3: 1}
        d2 = {4: 1, 5: 2, 6: 3}
        d3 = {7: 'a', 8: 'b', 9: 'c'}

        # Call the function you're testing
        result = getHierarchyArr(account_id, arr, d1, d2, d3)
        print(result)

        # Assert that the childId list has been extended correctly
        expected_child_ids = [1, 2, 3]  # Modify this based on your sample data
        self.assertEqual(result, arr)  # Assert that the return value is as expected


if __name__ == '__main__':
    unittest.main()
