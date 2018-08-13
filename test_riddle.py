import unittest
import run


class TestRiddle(unittest.TestCase):
    
    
    def test_is_this_thing_on(self):
        self.assertEqual(1,1)
        
        
    def test_get_next_riddle(self):
        """
        Test that the 'get dictionary' function returns a dictionary that has a length greater than 0
        """
        dictionary = run.get_next_riddle(2)
        self.assertGreater(len(dictionary), 0)        