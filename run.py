import os
from riddlesList import * 
from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'The cat is on the roof'
usernames = []
leaderboard = {}
score = 0
attempts = 0

def initialise_leaderboard(username):
    leaderboard.update({session['username']:session['score']})
    return

def initialise_session(username):
    session['username'] = username
    session['attempts'] = attempts
    session['score'] = score
    return session


@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "POST":
        username = request.form['addUsername'].title()
        if username not in usernames:
            usernames.append(username)
            flash("Success {}, your name is added. First Question".format(username))
            initialise_session(username)
            initialise_leaderboard(session['username'])
            return redirect('play')
        else:
            flash("Fail {}, Name taken try again".format(session['username']))     
    return render_template("index.html", page_title="Riddle-Me-This - Home", leaderboard=leaderboard)
    
    
    
    
    
    
def check_answer(answerInputByPlayer, correctAnswer):
    if correctAnswer == answerInputByPlayer:
        session['score'] += 1
        flash("CORRECT answer {}, next question.".format(correctAnswer))
        print("CORRECT answer" , correctAnswer)
        leaderboard.update({session['username']: session['score']})
        return    
    else:
        session['attempts'] += 1
        if session['attempts'] == 2:
            flash("WRONG two attempts, the answer is: {}".format(correctAnswer))
            session['attempts'] = 0
        return
    return

def getNextRiddle(riddleIndex):
    if riddleIndex == 0:
        return riddles[0]
    else:    
        #riddleIndex +=1
        #print(riddleIndex)
        nextRiddle = riddles[riddleIndex]
        #print(nextRiddle)
        return nextRiddle
     

@app.route('/play')
def play():
    nextRiddle = getNextRiddle(0) #dictionary
    session['currentRiddleIndex'] =  0
    session['currentRiddle'] = nextRiddle
    return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], 
                            leaderboard=leaderboard, currentRiddleIndex=session['currentRiddleIndex'], nextRiddle=nextRiddle['Question'])
    

@app.route('/riddle', methods=["GET", "POST"])
def riddle():
    getNextRiddle(session['currentRiddleIndex'])
    if request.method == "POST":
        userAnswer = request.form['riddleAnswer'].title()
        flash("Answer added {}.".format(userAnswer))
        print(session['currentRiddle']['Answer'].title())
        check_answer(userAnswer, session['currentRiddle']['Answer'].title())
        #print("check answer done - moved on")
        
        session['currentRiddleIndex'] +=1
        nextRiddle = getNextRiddle(session['currentRiddleIndex'])
        #flash("nextRiddle :::: {}".format(nextRiddle))
    return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard,
                            currentRiddleIndex=session['currentRiddleIndex'], nextRiddle=nextRiddle['Question'])


#session.pop('username', None)
#nextRiddle=nextRiddle['Question']

    #first_riddleQ = riddles[0]['Question']
    #first_riddleA = riddles[0]['Answer'].title()
#firstRiddleQ = first_riddleQ, 
        # flash("Riddles: {}.".format(riddles)) #[{'Answer': 'Name', 'Question': 'What belongs to you but others use it more than you do?'}, {'Answer': 'Hole', 'Question': 'The more you take aways, the larger it becomes? What is it?'}].
        # flash("riddle #1: {}".format(riddles[0].values())) #dict_values(['What belongs to you but others use it more than you do?', 'Name'])
        # flash("riddle #1 Q: {}".format(riddles[0]['Question'])) #What belongs to you but others use it more than you do?
        # flash("riddle #1 A: {}".format(riddles[0]['Answer']))

        #riddleA = riddle['Answer'].title()
        
        #print(riddle.items())
        #for key in riddle.items():
            #print("Key: ", key)





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