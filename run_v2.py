import os
import ast
from riddlesList import content
from operator import itemgetter
from flask import Flask, render_template, request, flash, redirect, url_for, session

riddles = content()

app = Flask(__name__)
app.secret_key = 'The cat is on the roof'
usernames = []
leaderboard_list = []
game_data= []
user_data = {}

def get_next_riddle(riddle_index):
    next_riddle = riddles[riddle_index]
    return next_riddle

def leaderboard(username):
    leaderboard_list.append({"username":session['username'], "score":user['score']})
    return leaderboard_list

def set_game_vars(username):
    username = username
    score = 0
    attempt = 0
    riddle_index = 0
    riddle = get_next_riddle(riddle_index)
    user = {
        "username" : session['username'],
        "score" : score,
        "attempt" : attempt,
        "riddle_index" : riddle_index,
        "riddle_question" : riddle['Question'],
        "riddle_answer" : riddle['Answer']
    }
    return user


@app.route('/first_riddle')
def first_riddle():
    global user
    user = set_game_vars(session['username'])
    game_data.append(user)
    return redirect(url_for('play'))



def check_answer(answerInputByPlayer, userdata):
    if userdata['username'] == session['username']:
        if userdata['riddle_answer'] == answerInputByPlayer:
            flash("you are CORRECT. Answer:  {}, next question.".format(userdata['riddle_answer']))
            userdata['score'] +=1
            userdata['riddle_index'] +=1
            if (userdata['riddle_index'] < len(riddles)): #check for last riddle
                return userdata
            else:
                #game_data['riddle_index'] = 100 #crude method of returning some index value
                return userdata
        else:
            flash("WRONG try again, one more attempt")
            userdata['attempt'] +=1 #increase attempt by 1
            if userdata['attempt'] == 2: # max of 2 attempts
                userdata['attempt'] = 0 #reset attempts back to 0
                userdata['riddle_index'] += 1 # attempts over, next question
                if (userdata['riddle_index'] < len(riddles)): #check for last riddle
                    return userdata
                else:
                    #riddleIndex = 100 #crude method of returning some index value
                    return userdata
        return userdata # index of next riddle


@app.route('/checkPlayerInput', methods=["GET", "POST"])
def check():
    if request.method == "POST":
        userAnswer = request.form['riddleAnswer'].title()
        flash("Players answer: {}".format(userAnswer))
        global user
        flash("Correct answer: {}".format(user['riddle_answer']))
        checked_answer = check_answer(userAnswer, user)

        if checked_answer['riddle_index'] > 2:
            return redirect(url_for('end'))
        else:
            riddle = get_next_riddle(checked_answer['riddle_index'])
            global user
            user = {
                "username" : session['username'],
                "score" : checked_answer['score'],
                "attempt" : checked_answer['attempt'],
                "riddle_index" : checked_answer['riddle_index'],
                "riddle_question" : riddle['Question'],
                "riddle_answer" : riddle['Answer']
            }
    return redirect(url_for('play'))  




@app.route('/play_v2', methods=["GET", "POST"])
def play():
    return render_template("play_v2.html", page_title="Riddle-Me-This - Play", riddle_question=user['riddle_question'],
                            riddle_answer=user['riddle_answer'], riddle_index=user['riddle_index'],
                            score=user['score'], attempt=user['attempt'], username=user['username'], usernames=usernames)                                


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form['addUsername'].title()
        if username not in usernames:
            usernames.append(username)
            session['username'] = username
            flash("Success {}, your name is added. Her is your first question".format(username))            
            return redirect(url_for('first_riddle'))
        else:
            flash("Fail {}, Name taken try again".format(username))     
    return render_template("index.html", page_title="Riddle-Me-This - Home", usernames=usernames)


@app.route('/end_v2')
def end():
    flash("End of game")
    global game_data
    leader_board = leaderboard(session['username'])
    #newlist = sorted(leaderboard, key=itemgetter('score'), reverse=True)
    return render_template("end_v2.html", page_title="Riddle-Me-This - Play", username=session['username'], usernames=usernames,
                            game_data=game_data, leaderboard=leader_board) 


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
    
    
    
    
    
    
    
    
    
    
    
        #request_game_data = request.args['data']
    #game_data = ast.literal_eval(request_game_data)