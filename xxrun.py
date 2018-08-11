import os
from riddlesList import content
from flask import Flask, render_template, request, flash, redirect, url_for, session

riddles = content()

app = Flask(__name__)
app.secret_key = 'The cat is on the roof'
usernames = []
leaderboard = {}
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


@app.route('/play', methods=["GET", "POST"])
def play():
    return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                    players=playersInfo, usernames=usernames, 
                                    riddleQ=riddle['Question'], riddleA=riddle['Answer'], riddleNumber=riddle['Number'])                                

@app.route('/end')
def end():
    flash("End of game")
    return render_template("end.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                    players=playersInfo, usernames=usernames) 


def check_answer(answerInputByPlayer, correctAnswer, riddleIndex):
    for player in playersInfo:
        if player['username'] == session['username']:
            if correctAnswer == answerInputByPlayer:
                flash("you are CORRECT. Answer:  {}, next question.".format(correctAnswer))
                player['score'] += 1 #increase score by 1
                leaderboard.update({session['username']:player['score']}) #update leaderboard
                riddleIndex += 1 #increase index by 1
                if (int(riddleIndex) < len(riddles)): #check for last riddle
                    global riddle
                    riddle = get_next_riddle(riddleIndex) #returns a dictionary NEXT RIDDLE
                    print("riddleIndex: ", riddleIndex,   "riddleNumber: ", riddle['Number'])
                    return riddle
                else:
                    print("end of game -redirect to end")
                    return render_template("end.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                    players=playersInfo, usernames=usernames)
            else:
                flash("WRONG try again, one more attempt")
                player['attempts'] += 1
                print("attempts: ",player['attempts'])
                if player['attempts'] == 2:
                    player['attempts'] = 0 #reset attempts back to 0
                    riddleIndex += 1
                    print("index: ", riddleIndex)
                    riddle = get_next_riddle(riddleIndex) #returns a dictionary NEXT RIDDLE
                    return riddle
            return redirect(url_for('play'))        


@app.route('/check', methods=["GET", "POST"])
def check():
    if request.method == "POST":
        userAnswer = request.form['riddleAnswer'].title()
        flash("Players answer: {}".format(userAnswer))
        global riddle
        flash("Correct answer: {}".format(riddle["Answer"]))
        riddle = check_answer(userAnswer, riddle['Answer'], riddles.index(riddle))
    return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                    players=playersInfo, usernames=usernames, 
                                    riddleQ=riddle['Question'], riddleA=riddle['Answer'], riddleNumber=riddle['Number']) 
                                    






















@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form['addUsername'].title()
        if username not in usernames:
            usernames.append(username)
            flash("Success {}, your name is added. Her is your first question".format(username))
            session['username'] = username
            leaderboard.update({username:0})
            create_player(username)
            return redirect(url_for('first_riddle'))
        else:
            flash("Fail {}, Name taken try again".format(username))     
    return render_template("index.html", page_title="Riddle-Me-This - Home", usernames=usernames, leaderboard=leaderboard)


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)