from flask import url_for
import unittest
import run
from run import app

class TestRiddle(unittest.TestCase):
    
    
    ''' https://www.patricksoftwareblog.com/unit-testing-a-flask-application/ '''
    # # executed prior to each test
    def setUp(self):
        client = app.test_client(self)
        self.app = app.test_client()


    # executed after each test
    def tearDown(self):
        pass
    

    ''' TEST 01 '''
    def test_is_this_thing_on(self):
        self.assertEqual(1,1)
        
    
    ''' TEST 02 '''    
    def test_get_next_riddle(self):
        """
        Test that the 'get_next_riddle' function returns a dictionary that has a length greater than 0
        """
        #dictionary = run.get_next_riddle(5) # will fail as list has 3 riddles
        dictionary = run.get_next_riddle(2) # will pass as list has 3 riddles
        self.assertGreater(len(dictionary), 0)
        
    
    
    ''' TEST 03 '''
    ''' StackOverflow sourced session information'''
    def test_index(self):
        """
        Test that the a session is created and populated with a value for username
        """
        with self.app as c:
            with c.session_transaction() as sess: #creates session
                sess['username'] = 'bob'
                self.assertEqual(sess['username'], 'bob')
                
        """
        Test that the page is reached
        """        
        #client = app.test_client(self)
        response = self.app.get('/', follow_redirects=True)
        response1 = self.app.get('/play_v4', follow_redirects=True)
        response2 = self.app.get('/end_v4', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    
    ''' TEST 04 '''
    def test_create_player(self):
        """
        Test that the a session is created and populated with a value for username and appended to player_info [] list as dictionary
        """
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['username'] = 'bob'
                with app.test_request_context():
                    self.assertEqual(run.create_player(sess['username']), [{'username':'bob', 'score':0, 'attempt':0,  "wrong":0, "riddle_number":0, "attempt_total":0, "restart":False, "resume":False}])
                    

    ''' TEST 05 '''
    def test_check_username(self):
        with self.app as c:
            with c.session_transaction() as sess: #creates session
                sess['username'] = 'bob'
                with app.test_request_context():
                    username = 'bob'
                    usernames = []
                    if not usernames and username == 'bob' and sess['username']:
                        self.assertTrue(run.check_username(username))
                    username = 'bob'
                    usernames = []
                    if usernames and username == 'bob' and not sess['username']: 
                        self.assertFalse(run.check_username(username))                        
                    username = 'bob'
                    usernames = ['bob']
                    if usernames and username == 'bob' and sess['username']:
                        self.assertTrue(run.check_username(username))
                    username = 'bob'
                    usernames = ['bob']
                    if not usernames and username == 'bob':
                        self.assertFalse(run.check_username(username))
                        
                        
    ''' TEST 06 '''
    def test_number_to_string(self):
        """
        Test helper function number_to_string()
        """
        test_number = run.number_to_string(2) # take a number return a word
        test_number1 = run.number_to_string(345) # take a number return a string
        test_number2 = run.number_to_string("answer") # take a number return a string
        self.assertEqual(test_number, "two")
        self.assertEqual(test_number1, "345")
        self.assertEqual(test_number2, "answer")
     

if __name__ == "__main__":
    unittest.main()             

#run option 1: $ python3 test_riddle.py  
#run option 2: $ python3 -m unittest -v
                