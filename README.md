# RIDDLE-ME-THIS Guessing Game

GitHub Pages: https://sonnerz.github.io/project02-interactive-frontend/ <br>

**Build a web application game that asks players to guess the answer to a pictorial or text-based riddle**


## Guidelines and Guideline fulfilment

1.	**The project's logic must be written in Python. HTML, CSS, and JavaScript can be used to enhance the look and feel of the game.**<br>
Python, HTML and CSS were used in this project.
2.	**Whenever possible, strive to use semantic HTML5 elements to structure your HTML code better.**<br>
I have used semantic HTML5 elements to structure my HTML
3.	**We recommended taking a TDD approach to building the game.**<br>
a.	**Create a section in your README.md titled 'Testing.' In this section, summarise your approach to testing and provide pseudocode you have written to develop your tests**<br>
b.	**Write and run automated tests to ensure that your website’s functionality works well**<br>
c.	**If you run any manual tests be sure to document those tests in the 'Testing' section of your README**<br>
d.	**If there are any tests that are not running as expected or are failing, provide a summary in the 'Testing' section of your README of what your expected output was and any reasons as to why the test(s) may be failing.**<br>
Testing is covered in the [Testing](#testing) section of this ReadMe.
4.	**Use flask, a micro-framework, to structure your project's back-end.**<br>
flask has been used <br>
5.	**Provide instructions on how to deploy your project in your README.**<br>
6.	**Make sure your site is as responsive as possible. You can test this by checking the site on different screen sizes and browsers.**<br>
The site was developed using Bootstrap 4 and was continually tested using dev tools in Chrome and viewing the site on mobile devices<br>
7.	**We advise that you write down user stories and create wireframes/mockups before embarking on full-blown development.**<br>
[User Stories](#scenarios) and [Wireframes](#wireframes) have been provided in this ReadMe.<br>
8.	**The site can also make use of CSS frameworks such as Bootstrap, just make sure you maintain a clear separation between the library code and your code.**<br>
Bootstrap 4 was used and custom css was created as scss files and stored in the static/scss directory <br>
9.	**Write a README.md file for your project that explains.**<br>
a.  **what the project does and the need that it fulfills.** <br>
b.	**It should also describe the functionality of the project, as well as the technologies used.**<br>
c.	**If some of the work was based on other code, explain what was kept and how it was changed to fit your need. A project submitted without a README.md file will FAIL**<br>
A ReadMe file has been provided.
10.	**Use Git & GitHub for version control. Each new piece of functionality should be in a separate commit.**<br>
Git and GiHub have been used and commit comments provided with each git commit
11.	**Deploy the final version of your code to a hosting platform such as Heroku.**<br>
Final version was deployed to Heroku


##  Non-requirements for this project:

1.	Secure user authentication (e.g. via passwords) is not required for this particular project. Having each user just choose a username is sufficient. Secure authentication will be introduced in the Django module.
The player has the ability to choose a username, start a game with the username, resume a game and view their username on the leader board at the end of a game.
2.	Persisting data by writing it in files is not required in this project, and indeed is problematic on Heroku due to its ephemeral filesystem. Instead, prefer to keep all of the data you need in memory (in variables) and/or in Flask sessions. Storing data effectively in a database will be the focus of the next module
Flask session was used to store the player username, variables were used there after for tracking player data.
3.	Your project is not expected to support real-time interaction between users on different browsers. There are ways to achieve this with clever use of js polling or websockets, but it's not a requirement for this project. It's perfectly fine if new data is only retrieved from the backend whenever a user loads a new page.




<hr><hr>
<a name="topofpage"></a>

# Table of Contents

*   [Strategy Plane](#strategy)
    *   [Define roles and responsibilities](#randr)
    *   [Project Charter](#charter)
    *   [Website development Roadmap](#roadmap)
    *   [Strategy Trade-off](#trade)
    *   [Defensive Design](#def)
*   [Scope Plane](#scope)
    *   [Scenarios](#scenarios)
    *   [Functional Specifications](#func)
    *   [Content Requirements](#content)
        *   [Navigation](#nav)
*   [Structure & Skeleton Plane](#sands)
    *   [Information architecture](#architecture)
*   [Wireframes](#wireframes)
    *   Start Application Page
    *   Application Page
    *   Leader Board Page
*   [Surface Plane](#surface)
    *   [Development Phase](#dev)
        *   [IDE](#ide)
        *   [Version Control](#version)
        *   [Readme](#readmeheader)
        *   [HTML/CSS Structure](#html)
            *   Start Application Page
            *   Application Page
            *   Leader Board Page
            *   Data
            *   SCSS/CSS
        *   [Content Sections](#contsect)
            *   Python
            *   riddleList.py
            *   run.py
            *   test_riddle.py
        *   [Testing](#testing)
            *   [Development/Defensive Design Testing](#devtesting)
            *   [Initial Testing](#initial)
            *   [Ongoing Testing](#ongoing)
            *   [Usability Testing](#usability)
            *   [Final Testing](#final)
        *   [Deployment](#deployment)
*  [Credit](#external)


<a name="strategy"></a>
# Strategy Plane
The overall aim of the project is to build a web application game that asks players to guess the answer to a pictorial or text-based riddle.  The logic of the game will be written in Python, HTML, CSS, and JavaScript can be used to enhance the look and feel of the game. 

The player is presented with a riddle they must answer and depending on their answer the game follows one of two paths – a correct answer takes the player to a new question; an incorrect answer gives the player the option to try again.

A leader board displays the players with the highest scores.


<a name="randr"></a>
## Define roles and responsibilities
For the purposes of this project, Sonya Cooley had full authority, primary responsibility, and full accountability for all aspects of the project. 
She had a Mentor available to her throughout the development of the game app.


[Top of page](#topofpage)
<a name="charter"></a>
## Project Charter 
||Objectives |
|:---|:---|
|**Purpose:** What purpose does the website serve?|The web application is for entertainment purposes only. The addition of a leader board adds a competition element to the game|
|**Goals:** What outcomes does it need to achieve?|<ul><li>To entertain players</li><li>Store and display player interaction and scores</li></ul>
|**Target audience:** Whom must the product appeal to and work for?|<ul><li>Puzzle enthusiasts and </li><li>curious site visitors</li></ul>|
|**Success indicators:** How will you know you have achieved project goals?|The leader board is regularly updated|
|**Strategies:** What approaches will help to realise the goals?|<ul><li>We will take a mobile first approach to Content. </li><li>Provide interesting and focused content for our target audience</li><li>Aim to keep the site simple and not over complicated</li><li>Present leader board data in a clear and user-friendly way</li></ul>
|**Tactics:** What activities might help to realise the strategies?|<ul><li>Provide interesting content (riddles) for players</li><li>Provide a user experience that is accessible and enjoyable for all visitors</li><ul><li>following conventions for design and interaction</li><li>providing clear and consistent navigation</li><li>testing usability with a wide range of clients and industry standard tools</li></ul></ul>

[Top of page](#topofpage)
<a name="roadmap"></a>
### Website development Roadmap
The UXD will be driven by the API data and user needs.
|**Define**|Requirements gathering, SEO, Research Competitors,  Content Strategy – Personas, Interesting Riddles.|
|:---|:---|
|**Design**|Information architecture, Functional & technical requirements, Navigation design, Wireframes, UX/UI, Pages, Branding, style guides, mock-ups.|
|**Develop**|Look & feel, Design and Development, Build, Version control, Testing, Deploy|

[Top of page](#topofpage) 

<a name="trade"></a>
### Strategy Trade-off
|Opportunity/Problem|Importance|Viability/Feasibility|
|:---|:---|:---|
|Interesting and fun GUI|5|5|
|Usable GUI|5|5|
|Leader board|5|5|
|Interesting Riddles|5|4|


[Top of page](#topofpage)
<a name="def"></a>
## Defensive Design
Defensive design for our Riddle-Me-This Web application will focus on the most common points of failure: user input areas, feedback and server problems.
*	I will employ validation to check for user mistakes before they frustrate the player
*   I will protect players from server errors and broken links with informative messages
*   My Defensive design will assist the player before mistakes happen.


If players are unsuccessful with their guess, they will be informed by on screen messages and provided with the option of guessing the answer again. 
Their guesses will be limited to 2 attempts and on-screen text will inform players of how many attempts remain.

Players will be allowed to enter a username to appear on the leader board when they finish a game. They will be informed if that username has already been taken and asked to enter a different username option.

The input area will be protected against malicious code.
A pattern will be added to the input form controls to only allow the input of letters and numbers, no special characters will be allowed: pattern="[A-Za-z0-9]{1,50}"



[Top of page](#topofpage)
<a name="scope"></a>
# Scope Plane
The project scope is based on our defined Strategy.
Scoping will;
*   fully define the web application requirements 
*   determine the key functionalities
*   determine what features are to be included in this and possible future product releases

The Riddle-Me-This application will target puzzle enthusiasts and attract casual site visitors. The site will provide riddles for players to solve. A combination of images, and HTML5 will be used to make the interface useful and interesting. Semantic HTML will used throughout and the site will be responsive to a broad range of devices.
Python and the Flask micro-framework will be the primary technologies used to implement the application functionality.


[Top of page](#topofpage)

<a name="scenarios"></a>
## Scenarios
### Puzzle enthusiast:
A puzzle enthusiast will be a player who is familiar with riddles and their veiled meaning. They will most likely be familiar with a game 
interface where player input is required. They will also be familiar with leader boards and the information they provide.
They will expect features for example, a defined number of attempts, attempt count indicator, input area and good feedback.


### Puzzle player:
A puzzle player will visit the site out of curiosity to investigate a possible new riddle source. They may attempt a few riddles and then abandon the 
game when they answer incorrectly or they may continue until they appear on the leader board. 

### Casual player:
A casual player will visit the site out of curiosity to investigate the type of game. They may attempt a few riddles and then 
abandon the game when they answer incorrectly. They may not visit the leader board.

[Top of page](#topofpage)

<a name="func"></a>
## Functional Specifications

The site will provide players with access to a series of Riddles.
The site will provide the ability for players;
*   to enter a username and be identified by that username
*   to provide answers to the riddles
*   to make 2 attempts at a riddle answer
*   to have their score recorded
*   to have their score appear on a score sorted leader board
*   to have the correct answer provided to them after 2 attempts

The Riddle-Me-This application will be optimised for latest version of Chrome, Firefox, Internet Explorer, Safari and Opera and 
optimised for mobile usage. HTML and CSS will be written using the Mobile-First approach. The mobile-first approach is designing for the 
smallest screen and working your way up to desktop.

![Functional flow](static/img/readme_images/Functionalflow.png)


[Top of page](#topofpage)
<a name="content"></a>
##    Content Requirements
The Riddle-Me-This application will follow a standard format, with a HTML5 structure based on Bootstrap 4. 
The application will have a sticky navbar/info bar always available to players.
The game interface will provide players with; 
*   a username entry
*   a username entry submit button
*   game help information
*   the riddle question, 
*   an answer input area,
*   a submit button
*   a feedback area
*   an attempt count display
*   an answer area whether it’s correct or incorrect
*   a leader board
*   navigation to the leader board 

All html pages will be created using HTML5 and CSS3, supported by the Bootstrap 4.0 Framework 

**Start**
![Application Start](static/img/readme_images/start_page.png)

**Application structure**
![Application page](static/img/readme_images/app_page.png)

**Leader Board structure**
![Leader Board layout](static/img/readme_images/leader_page.png)

<a name="nav"></a>
### Navigation
The navbar/info bar will be available to players at the top of the application.
It will provide navigation to the leader board, navigation to the start page and the identity of the player.


[Top of page](#topofpage)
<a name="sands"></a>
#  Structure & Skeleton Plane
Our goal for the Structure plane is to organise the information architecture and interactions for the application. We will keep a consistent, predictable, and learnable interface that game users would be familiar with. We will use industry standard technologies to implement expected behaviours when using the application, e.g. tooltips, navigation, including accessibility, etc.
Users will find navigation and user information at the top of the application. 
The input fields will follow user expectations where feedback is provided if user interactions are unexpected, correct or incorrect.


<a name="architecture"></a>
## Information architecture
The entire application will be implemented in three pages. 
The application directories and files will be organised in the following way;


|<ul><li>Site Root</li><ul><li>Procfile</li><li>ReadMe</li><li>Requirements.txt</li><li>RiddleList.py</li><li>Run.py</li><li>Test_riddle.py</li></ul></ul>|<ul><li>Static Directory</li><ul><li>CSS sub-directory</li><li>Images sub-directory</li><li>JS sub-directory</li></ul></ul><ul><li>SCSS Directory</li><ul><li>scss files for css</li></ul></ul><ul><li>Templates Directory</li><ul><li>404.html</li><li>500.html</li><li>Base.html</li><li>End.html</li><li>Index.html</li><li>Play.html</li></ul></ul>|
|:---|:---|


[Top of page](#topofpage)
<a name="wireframes"></a>
#  Wireframes
## Start Application Page (‘/’ index.html)<a name="apodwf"></a>
![start application](static/img/readme_images/start_application.png)
## Application Page (‘/play’ play.html)<a name="epicwf"></a>
![application page](static/img/readme_images/application_page.png)
## Leader Board Page (‘/end’ end.html)<a name="librarywf"></a>
![leaderboard](static/img/readme_images/leaderboard.png)


[Top of page](#topofpage)
<a name="surface"></a>
#  Surface Plane

<a name="dev"></a>
## Development Phase

<a name="ide"></a>
### IDE
The web application will be developed using the Cloud9 IDE. 
Cloud9 IDE is an online integrated development environment, that supports hundreds of programming languages. 
It enables developers to get started with coding immediately with pre-configured workspaces, collaborate with their peers
with collaborative coding features, and web development features like live preview and browser compatibility testing.


<a name="version"></a>
### Version Control
Git will be used to manage the source code for this project. Git is a version control system for tracking changes in project files.
Project files will be committed to Git after each major functional addition, update or implementation of testing results.
Following the initial commit to Git, each major update will be followed by a Git add and commit. 
**A full Git log is available on the GitHub project repository.**


<a name="readmeheader"></a>
### Readme
A Readme markdown file is provided with the site on GitHub. It explains what the project does and the need that it fulfils. 
It also describes the functionality of the site, the technologies used and how it was tested. 

The Readme provides information on how the site was deployed and tested and if some of the work was based on other code.



[Top of page](#topofpage)
<a name="html"></a>
### HTML/CSS Structure
**Start Application Page**

The web application start page gives the player the options of; starting the game by entering a username, or viewing the game help.  A logo will take a prominent position on the page. The options; play the game, and view help will be placed beside the logo.
The page and its functionality will be created using the Bootstrap 4 Framework, Python and The Flask micro-framework.


**Application Page**

The web application game page displays the riddle question and provides a text input area where the player can enter their answer. After clicking the submit button, the answer will be evaluated and feedback will be provided in the message area under the submit button.
An attempt count will be provided below the answer input area.
The page and its functionality will be created using the Bootstrap 4 Framework, Python and The Flask micro-framework.


**Leader Board Page**

The leader board page will provide players with a list of the top 15 scoring players.
The list will show the username, score and the timestamp when that score was created.
The page and its functionality will be created using the Bootstrap 4 Framework, Python and The Flask micro-framework.

**Data**

The riddles and answers will be read from a python file (riddlesList.py) on the application site and the usernames will be stored as a dictionary in a python list.

**SCSS/CSS**

Bootstrap 4 provides the fundamental HTML5, CSS and JavaScript for the application to ensure that it meets the Responsive requirement.
However, custom styles have been created and a styles.css file can be found in the static/css directory.

Custom styles for each page, and bootstrap overrides are in their own SCSS file.
<ul><li>base.scss </li><li>
bootstrap-overrides.scss</li><li>
end.scss</li><li>
index.scss</li><li>
mixins.scss</li><li>
Play.scss</li><li>
Styles.scss</li><li>
variables.scss</li></ul>

[Top of page](#topofpage)
<a name="contsect"></a>
###  Content Sections - Python

**Python**

<ul><li>run.py file has been created for the app code</li><li>
test_riddle.py contains unittests for the app</li><li>
riddlesList.py contain the riddle questions and answers </li></ul>

**riddleList .py**

Content structure taken from sentdex on YouTube: https://www.youtube.com/channel/UCfzlCWGWYyIQ0aLC5w48gBQ

*Content function: Dictionary inside riddles tuple*
```
{ 
“Question”: value,
“Answer”: value,
“Number”: value,
“Path”: value
}
```
```Python
def content():
    riddles = (
                {
                    "Question": "What belongs to you but others use it more than you do?",
                    "Answer": "name",
                    "Number": 0,
                    "Path": ""
                 },
                 {
                    "Question": "Work out this Anagram: edlpoemvent",
                    "Answer": 'development',
                    "Number": 1,
                    "Path": ""
                 },...
            )
```
**run. py**

```Python
riddles = content()

    app = Flask(__name__)
    app.secret_key = 'The cat is on the roof'
    usernames = []
    leaderboard = []
    player_info = []
    riddle = {}
```
Set riddles to be the value of content() imported from riddlesList.py

 Global variables: 
 - Usernames List, 
 - Leaderboard List, 
 - Player_info List,
 - Riddle dictionary.

```Python
leaderboard = []
{
"username": session['username'],
"score": player['score'],
"timestamp": date_completed
}
```
Leader board list contains a dictionary for each entry with key values: username, score, timestamp
```Python
Player_info = []
{
"username":username,
"score":0,
"attempt":0,
"wrong":0,
"riddle_number":0,
"attempt_total":0,
"restart":False,
"resume":False
}
```
Player info list contains a dictionary for each entry with key values: username, score, attempt, wrong, riddle_number, attempt_total, restart, resume.
```Python
riddle = {}
{
“Question”: *value*,
“Answer”: *value*,
“Number”: *value*,
“Path”: *value*
}
```
Riddle dictionary; for each entry has key values: Question, Answer, Number, Path

**test_riddle.py**

Tested: get_next_riddle() function<br>
Tested: ensure that a session gets created<br>
Tested: that a response is received from the html files<br>
Tested: create_player() function<br>
Tested: check_username() function<br>
Tested: helper function  - number_to_string()


[Top of page](#topofpage)
<a name="testing"></a>
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


[Top of page](#topofpage)

<a name="deployment"></a>
### Deployment
GitHub is used to host the code and publish the pages.

A new repository was created in GitHub called: **project02-interactive-frontend**

After a final Git Add and Git commit

``$git add .``

``$git commit -m "Final commit"``

The pages were pushed to the new GitHub repository

``$ git remote add origin https://github.com/Sonnerz/project02-interactive-frontend``

``$ git push -u origin master``

``$Username``

``$Password``

Under the Settings – GitHub Pages of the new repository, the master branch of the code is published to the url: 

https://sonnerz.github.io/project02-interactive-frontend/

[Top of page](#topofpage)

<a name="external"></a>
# Credit
##  Content/ Acknowledgements

The following sites were used as resources to get sample css and debugging css.

|Site|URL|Resource
|:---|:---|:---|
|Stack Overflow|http://stackoverflow.com|Code snippets/idea throughout the project
|w3schools Python|https://www.w3schools.com/python/|How to access dictionaries, etc
|Mentor - Chris Zelinski||Helped with my app logic in the mid project meeting and GET/POST methods
|Flask|http://flask.pocoo.org/docs/1.0/quickstart/|Went back to basics to learn about flask
|Youtube|https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ|Pretty Printed flask content
|Youtube|https://www.youtube.com/channel/UCfzlCWGWYyIQ0aLC5w48gBQ|Sentdex Flask content
|Website|https://www.patricksoftwareblog.com/unit-testing-a-flask-application/ |Flask unit testing
|Slack||Slack members tested my app as users


##  Media

|Media|Scource|
|:---|:---|
|Riddler background image|https://www.desktopbackground.org/
|Running water in riddle about tank	|http://worldartsme.com/
|Tank riddle image|http://oddmenot.com
|Riddles and answers|https://riddles.fyi/
|Riddle Me This|Sonya Cooley created in Photoshop
|Google Fonts|Margarine


[Top of page](#topofpage)


