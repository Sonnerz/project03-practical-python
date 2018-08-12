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
game_data = []

def get_next_riddle(riddle_index):
    next_riddle = riddles[riddle_index]
    return next_riddle

def leaderboard(username):
    leaderboard_list.append({"username":session['username'], "score":game_data['score']})
    return leaderboard_list

def set_game(username, riddle_index):
    username = username
    score = 0
    attempt = 0
    riddle_index = riddle_index
    riddle = get_next_riddle(riddle_index)
    data = {
        "username" : session['username'],
        "score" : score,
        "attempt" : attempt,
        "riddle_index" : riddle_index,
        "riddle_question" : riddle['Question'],
        "riddle_answer" : riddle['Answer']
    }
    return data


@app.route('/first_riddle', methods=["GET", "POST"])
def first_riddle():
    global game_data
    game_data.append(set_game(session['username'], 0))
    return redirect(url_for('play'))



def check_answer(answerInputByPlayer, game_data):
    game_data_index = next((index for (index, d) in enumerate(game_data) if d["username"] == session['username']), None)
    if game_data[game_data_index]['username'] == session['username']:
        if game_data[game_data_index]['riddle_answer'] == answerInputByPlayer:
            flash("you are CORRECT. Answer:  {}, next question.".format(game_data['riddle_answer']))
            game_data[game_data_index]['score'] +=1
            game_data[game_data_index]['riddle_index'] +=1
            if (game_data[game_data_index]['riddle_index'] < len(riddles)): #check for last riddle
                return game_data
            else:
                #game_data['riddle_index'] = 100 #crude method of returning some index value
                return game_data
        else:
            flash("WRONG try again, one more attempt")
            game_data[game_data_index]['attempt'] +=1 #increase attempt by 1
            if game_data[game_data_index]['attempt'] == 2: # max of 2 attempts
                game_data[game_data_index]['attempt'] = 0 #reset attempts back to 0
                game_data[game_data_index]['riddle_index'] += 1 # attempts over, next question
                if (game_data[game_data_index]['riddle_index'] < len(riddles)): #check for last riddle
                    return game_data
                else:
                    #riddleIndex = 100 #crude method of returning some index value
                    return game_data
        return game_data # index of next riddle


@app.route('/checkPlayerInput', methods=["GET", "POST"])
def check():
    if request.method == "POST":
        userAnswer = request.form['riddleAnswer'].title()
        flash("Players answer: {}".format(userAnswer))
        game_data_index = next((index for (index, d) in enumerate(game_data) if d["username"] == session['username']), None)
        flash("Correct answer: {}".format(game_data[game_data_index]['riddle_answer']))
        global game_data
        game_data = check_answer(userAnswer, game_data)
        if game_data['riddle_index'] > 2:
            return redirect(url_for('end'))
        else:
            riddle = get_next_riddle(game_data[game_data_index]['riddle_index'])
            game_data = {
            "username" : session['username'],
            "score" : game_data['score'],
            "attempt" : game_data['attempt'],
            "riddle_index" : game_data['riddle_index'],
            "riddle_question" : riddle['Question'],
            "riddle_answer" : riddle['Answer']
            }
    return redirect(url_for('play'))  




@app.route('/play_v2', methods=["GET", "POST"])
def play():
    #request_game_data = request.args['data']
    #game_data = ast.literal_eval(request_game_data)
    game_data_index = next((index for (index, d) in enumerate(game_data) if d["username"] == session['username']), None)
    return render_template("play_v2.html", page_title="Riddle-Me-This - Play", game_data=game_data, riddle_question=game_data[game_data_index]['riddle_question'],
                            riddle_answer=game_data[game_data_index]['riddle_answer'], riddle_index=game_data[game_data_index]['riddle_index'],
                            score=game_data[game_data_index]['score'], attempt=game_data[game_data_index]['attempt'], username=game_data[game_data_index]['username'], usernames=usernames)                                


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