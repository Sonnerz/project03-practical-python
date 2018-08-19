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
    playersInfo.append({"username":username, "score":0, "attempts":0})
    return

def get_next_riddle(riddleIndex):
    nextRiddle = riddles[riddleIndex]
    return nextRiddle

@app.route('/first_riddle', methods=["GET", "POST"])
def first_riddle():
    global riddle
    riddle = get_next_riddle(0) #returns a dictionary FIRST RIDDLE
    return redirect(url_for('play'))    


@app.route('/play_v1', methods=["GET", "POST"])
def play():
    return render_template("play_v1.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                    players=playersInfo, usernames=usernames, 
                                    riddleQ=riddle['Question'], riddleA=riddle['Answer'])                                

@app.route('/end_v1')
def end():
    flash("End of game")
    newlist = sorted(leaderboard, key=itemgetter('score'), reverse=True)
    return render_template("end_v1.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                    players=playersInfo, usernames=usernames, newlist=newlist) 


def check_answer(answerInputByPlayer, correctAnswer, riddleIndex):
    for player in playersInfo:
        if player['username'] == session['username']:
            if correctAnswer == answerInputByPlayer:
                flash("you are CORRECT. Answer:  {}, next question.".format(correctAnswer))
                player['attempts'] = 0
                player['score'] += 1 #increase score by 1
                for leader in leaderboard:
                    if leader['username'] == session['username']:
                        leader['score'] += 1 #update leaderboard by 1
                riddleIndex += 1 #increase index by 1 for next riddle
                if (riddleIndex < len(riddles)): #check for last riddle
                    return riddleIndex
                else:
                    riddleIndex = 100 #crude method of returning some index value
                    return riddleIndex
            else:
                flash("WRONG try again, one more attempt")
                print("A: ", riddleIndex)
                player['attempts'] += 1 #increase attempt by 1
                print("B: ",player['attempts'])
                if player['attempts'] == 2: # max of 2 attempts
                    print("C: ",player['attempts'])
                    player['attempts'] = 0 #reset attempts back to 0
                    print("D: ",player['attempts'])
                    riddleIndex += 1 # attempts over, next question
                    print("E: ", riddleIndex)
                    if (riddleIndex < len(riddles)): #check for last riddle
                        return riddleIndex
                    else:
                        riddleIndex = 100 #crude method of returning some index value
                        return riddleIndex
                print("F: ", riddleIndex)    
            return riddleIndex # index of next riddle


@app.route('/checkPlayerInput', methods=["GET", "POST"])
def check():
    if request.method == "POST":
        userAnswer = request.form['riddleAnswer'].title()
        flash("Players answer: {}".format(userAnswer))
        global riddle
        flash("Correct answer: {}".format(riddle["Answer"]))
        riddleIndex = check_answer(userAnswer, riddle['Answer'], riddles.index(riddle))
        if riddleIndex == 100:
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