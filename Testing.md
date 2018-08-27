#   Testing the Riddle-Me-This game
<a name="topofpage"></a>

## Table of Contents

*  [Development/Defensive Design Testing](devtesting)
    *   [Deployment](#deployment)
*  [Credit](#external)




###    Testing
The app was tested on an ongoing basis. Chrome and Chrome Developer Tools were the primary browser and tool used for testing. However, the site was also tested using Firefox and Internet Explorer.

*   CSS was validated using the **CSS Validation Service** provided by The World Wide Web Consortium (W3C): https://jigsaw.w3.org/css-validator/

##### During development:
 *  **print()** was used extensively for viewing returned data and testing.
 *	Div’s had vibrant background colours so that the developer was easily able to identify them 
   *	Each change was viewed in a chrome browser and tested using developer tools at full width resolution and using a variety of device emulators; Galaxy SIII, Galaxy 5, Laptop touch screen, iPhone 5/SE, iPhone 6/7/8, iPhone 6/7/8 Plus, iPhone X, iPad. 
   *	Remote debugging using Android, Windows OS and Chrome Dev
   Tools was used to test each new functionality and new/updated page.

[Top of page](#topofpage)

<a name="devtesting"></a>
#### Development/Defensive Design Testing
Testing was carried out continuously while developing the app. 
As per the Defensive Design Strategy described in the Strategy Plan, all form inputs are checked for empty values. Users are messaged if they click a submit button without providing text.
Users are also informed by an on-screen text if their answer was correct or incorrect. 


| | |
|:---|:---|
|Users are informed if the input box is not completed.|![Input Check](static/img/readme_images/inputcheck.png)|
|If the username is taken.|Users are informed: 'username', this name has already been taken. Enter a different player name|
|Correct answer feedback.|![Correct answer](static/img/readme_images/correct_anwer.png)|
|Incorrect answer feedback and player is informed of attempt count and attempts remaining|![Incorrect answer](static/img/readme_images/incorrect_anwer.png)|
|Player is informed of riddle count <br>If it’s riddle number 1:<br>try answering this first riddle:<br><br>If it’s riddle number 10:<br>try answering this last riddle:<br><br>If it’s riddle number 2 to 9:<br>try answering this first riddle:<br><br>If it’s the end of the game:<br>there are no more riddles<br>|![Try Anwering](static/img/readme_images/try_anwering.png)|
|At the end of 10 riddles:<br>Player is informed of their <br>Score<br>Incorrect score<br>Attempt count<br>They are presented with a button to take them to the leader board.|![Game Over](static/img/readme_images/end_game.png)|


[Top of page](#topofpage)

<a name="initial"></a>
##### Initial  Testing

Ensured routing was working
```Python
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
```


**Test scenario**

Importing riddle content and ensuring it is available to the browser
1.   Created riddleList.py
2.   Imported to run.py: from riddlesList import *
3.	riddles = content()
4.	Rendered to browser: <br>
return render_template("index.html", 
page_title="Riddle-Me-This - Home", 
riddles=riddles)
5.	<p>{{riddles.values()[0]}}</p>




<a name="ongoing"></a>
##### Ongoing Testing
|Page/functionality|Chrome|Firefox|IE|Chrome Android-Remote Debugging|
|:---|:---:|:---:|:---:|:---:|
|index|General formatting issues|General formatting issues|General formatting issues|General formatting issues|
|play|General formatting issues|General formatting issues|General formatting issues|General formatting issues
|end|General formatting issues|General formatting issues|General formatting issues|General formatting issues|
|Responsive Design|Styling issues|Styling issues|Styling issues|Styling issues|
|Feedback messages|Passed|Passed|Passed|Passed|
|Player score/attempts|Multiple same user instance|Multiple same user instance|Multiple same user instance|Multiple same user instance

I had a div on each page which I called my debug panel. It displayed the values of all my lists and variables so that I could monitor them with every interaction and test that variables were being set correctly

![Debug Panel](static/img/readme_images/debug_panel1.png)|


**Test scenario**

    Click 'How to Play' link on index page. - Confirm Modal appears
    Click Close - Confirm Modal disappears
    
    Confirmed
	

**Test scenario**

debug=False<br>
Confirm that debug button not visible “Hide/Show Debug Panel (only available in Debug Mode)”


    Debug panel
    Click button hide / show panel
    Run.py
    if __name__ == '__main__':
        app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=False)
    Restart app
    
    Confirmed

**Test scenario**

    1.   Player logs in
    2.   Player begins a game
    3.   Player visits the leaderboard
    4.   Player can return to the game page and resume their game
    
    Confirmed
    
    
**Test scenario**

    1.   Player logs in
    2.   Player begins a game
    3.   Player visits the start page
    4.   If Player still in session, player can log back in and resume game
    
    Confirmed
    
**Test scenario**

    1.   Player logs in
    2.   Player begins a game
    3.   Player abondons a game
    4.   If Player session expired and player not in usernames list, player is asked to log in with a username not in the usernames list 
    
    Confirmed     
    
    
**Test scenario**

    1.   Player logs in
    2.   Player begins a game
    3.   Player abondons a game
    4.   If Player session expired and player name is in usernames list, player can log back in and resume their game 
    
    Confirmed       

[Top of page](#topofpage)

<a name="usability"></a>
#### Usability Testing
During usability testing, 
*   Testers commented that the player name input box on the start page was not very obvious. 
    <br>I redesigned the start page to make the input field more obviously an input field, and I changed the help button to a hyperlink with a font awesome icon. This made the submit button the only button on the page.
*   Testers noticed that the lowercase version of an answer wasn’t accepted. So I added .lower() function to the function that gets the player response.

*   Testers were frustrated at 
    *   not being able to log back into the game with the same user name, 
    *   resume a game after visiting the leader board or 
    *   resume a game after logging back in

As a result the code was overhauled to add these player abilities

<a name="final"></a>
####   Final Testing
#####   Unit Testing

Unit testing setup

```Python
def setUp(self):
        client = app.test_client(self)
        self.app = app.test_client()


    # executed after each test
    def tearDown(self):
        pass
```
Test that get_next_riddle() is returning a riddle dictionary
```Python    ''' TEST 02 '''    
    def test_get_next_riddle(self):
        """
        Test that the 'get_next_riddle' function returns a dictionary that has a length greater than 0
        """
        #dictionary = run.get_next_riddle(5) # will fail as list has 3 riddles
        dictionary = run.get_next_riddle(2) # will pass as list has 3 riddles
        self.assertGreater(len(dictionary), 0)
```
Test that a session is being created. Test that each html page responds
```Python
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
```

Test that the create_player() creates a dictionary of player in the player_info list
```Python
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

```
Test that check_username() Works for each scenario
```Python''' TEST 05 '''
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
```

Test to ensure the helper function number_to_string() takes in a digit and returns a string.
```Python
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
```



|Page/functionality|Chrome|Firefox|IE|Chrome Android-Remote Debugging|
|:---|:---:|:---:|:---:|:---:|
|index|Passed|Passed|Passed|Passed|
|play|Passed|Passed|Passed|Passed|
|end|Passed|Passed|Passed|Passed|
|Responsive Design|Passed|Passed|Passed|Passed
|Feedback messages|Passed|Passed|Passed|Passed|
|Player score/attempts|Passed|Passed|Passed|Passed|

|Device/Test|Galaxy SIII|Galaxy 5|Laptop touch screen|iPhone 5/SE|iPhone 6/7/8|iPhone 6/7/8 Plus|iPhone X|iPad|
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|Responsive Design|Passed|Passed|Not Applicable|Passed|Passed|Passed|Passed|Passed
|Styling|Passed|Passed|Passed|Passed|Passed|Passed|Passed|Passed|
|Error messages|Passed|Passed|Passed|Passed|Passed|Passed|Passed|Passed|

