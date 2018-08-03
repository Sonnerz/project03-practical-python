import os
from riddlesList import * 
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'The cat is on the roof'
usernames = []
leaderboard = {}
score = 0
attempts = 0


def loadRiddles():
    riddles_list = riddles #all riddles LIST
    #print(riddles_list[0]) # first dict riddle
    #print(riddles_list[0].keys()) # first dict riddle = Answer, Question
    #print(riddles_list[0].values()) # first dict riddle = Q value, A value
    return riddles_list
    
    
def check_answer(username, answer):
    if answer == answer:
        print('correct answer,next question')
        score += 1
        if username in leaderboard['username']:
           leaderboard['score'] = score
    else:
        attempt += 1
        print('wrong answer, try again')
    return

def initialise_leaderboard(username):
    leaderboard["username"] = username
    leaderboard["score"] = 0
    return
    

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["addusername"].title()
    
        if username not in usernames:
            usernames.append(username)
            flash("Success {}, your name is added. Click play".format(username))
            initialise_leaderboard(username)
            # return redirect(username)
        else:
            flash("Fail {}, Name taken try again".format(username)) 
    return render_template("index.html", page_title="Riddle-Me-This - Home")
    
    
    
@app.route('/<username>')
def user(username):
    riddlesQ = loadRiddles()
    print(type(riddlesQ))
    print(leaderboard)
    return render_template("play.html", page_title="Riddle-Me-This - Play", username=username, riddles=riddlesQ)
    
    
   
@app.route('/play')
def play():
    return render_template("play.html", page_title="Riddle-Me-This - Play", username=username)
    


# @app.route('/index2')
# def index2():
#     return render_template("index2.html", page_title="Riddle-Me-This - Home")
    
# @app.route('/instructions', methods=["GET", "POST"])
# def instructions():
#     username = request.form["addusername"].title()
#     return render_template("instructions.html", context={'username': 'test'})
    
    
"""
Logic:

1. User enters a username
2. Upon submit, GET riddle page fron the riddle function
3. Riddle page displays:
    - the question
    - a textbox for the answer
    - submit button to submit the answer
4. User submits their answer
5. POST to the riddle function with the answer
6. Check the answer against a list of answers
7. Return correct or incorrect with the same template and iterate to the next question
"""


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)