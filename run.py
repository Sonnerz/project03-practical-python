import os
from riddlesList import content
from operator import itemgetter
from flask import Flask, render_template, request, flash, redirect, url_for, session

riddles = content()

app = Flask(__name__)
app.secret_key = 'The cat is on the roof'
usernames = []
leaderboard = []
playersInfo = []
riddle = {}

def create_player(username):
    playersInfo.append({"username":username, "score":0, "attempt":0, "riddle_number":0})
    return

def get_next_riddle(riddleIndex):
    nextRiddle = riddles[riddleIndex]
    return nextRiddle

@app.route('/first_riddle', methods=["GET", "POST"])
def first_riddle():
    global riddle
    riddle = get_next_riddle(0) #returns a dictionary FIRST RIDDLE
    return redirect(url_for('play'))    


@app.route('/play_v3', methods=["GET", "POST"])
def play():
    return render_template("play_v3.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                    players=playersInfo, usernames=usernames, 
                                    riddle_question=riddle['Question'], riddle_answer=riddle['Answer'])                                

@app.route('/end_v3')
def end():
    flash("End of game")
    newlist = sorted(leaderboard, key=itemgetter('score'), reverse=True)
    return render_template("end_v3.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                    players=playersInfo, usernames=usernames, newlist=newlist) 


def check_answer(answerInputByPlayer, correctAnswer, riddleIndex):
    for player in playersInfo:
        if player['username'] == session['username']:
            if correctAnswer == answerInputByPlayer:
                flash("you are CORRECT. Answer:  {}, next question.".format(correctAnswer))
                player['attempt'] = 0
                player['score'] += 1 #increase score by 1
                player['riddle_number'] += 1
                for leader in leaderboard:
                    if leader['username'] == session['username']:
                        leader['score'] += 1 #update leaderboard by 1
                riddleIndex += 1 #increase index by 1 for next riddle
                if (riddleIndex < len(riddles)): #check for last riddle
                    return player['riddle_number']
                else:
                    return player['riddle_number']
            else:
                flash("WRONG try again, one more attempt")
                player['attempt'] += 1 #increase attempt by 1
                if player['attempt'] == 2: # max of 2 attempts
                    player['attempt'] = 0 #reset attempts back to 0
                    player['riddle_number'] += 1
                    riddleIndex += 1 # attempts over, next question
                    if (riddleIndex < len(riddles)): #check for last riddle
                        return player['riddle_number']
                    else:
                        return player['riddle_number']
            return player['riddle_number'] # index of next riddle


@app.route('/checkPlayerInput', methods=["GET", "POST"])
def check():
    if request.method == "POST":
        userAnswer = request.form['riddleAnswer'].title()
        flash("Players answer: {}".format(userAnswer))
        global riddle
        flash("Correct answer: {}".format(riddle["Answer"]))
        riddleIndex = check_answer(userAnswer, riddle['Answer'], riddles.index(riddle))
        if riddleIndex > 2:
            return redirect(url_for('end'))
        else:
            riddle = get_next_riddle(riddleIndex) 
    return redirect(url_for('play'))    


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form['addUsername'].title()
        if username not in usernames:
            usernames.append(username)
            flash("Success {}, your name is added. Her is your first question".format(username))
            session['username'] = username
            leaderboard.append({"username":username, "score":0})
            create_player(username)
            return redirect(url_for('first_riddle'))
        else:
            flash("Fail {}, Name taken try again".format(username))     
    return render_template("index.html", page_title="Riddle-Me-This - Home", usernames=usernames, leaderboard=leaderboard)


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)