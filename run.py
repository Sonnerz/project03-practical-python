import os
import ast
from datetime import datetime
from riddlesList import content
from operator import itemgetter
from flask import Flask, render_template, request, flash, redirect, url_for, session, current_app

riddles = content()        

app = Flask(__name__)
app.secret_key = 'The cat is on the roof'
usernames = []
leaderboard = []
player_info = []
riddle = {}

def get_next_riddle(riddleIndex):
    '''
    If answer is correct or attempts are more than two, get the next riddle from the riddle List, based on the list index
    '''
    nextRiddle = riddles[riddleIndex] # get next riddle by passing index to riddles[] and return the riddle {} dictionary
    return nextRiddle

@app.route('/start_game', methods=["GET", "POST"])
def start_game():
    '''
    Intialise the global lists and dictionary. Populate with the player info to track their progress.Intialise.Intialise
    Get the first riddle to start the game. Redirect to the game html page - play() play.html.
    '''
    date = datetime.now().strftime("%d-%m-%Y")
    leaderboard.append({"username":session['username'], "score":0, "timestamp":date}) # added to leaderboard
    player_info.append({"username":session['username'], "score":0, "attempt":0, "riddle_number":0}) #creates a player
    global riddle
    riddle = get_next_riddle(0) #returns a dictionary FIRST RIDDLE
    return redirect(url_for('play'))    


@app.route('/play_v4')
def play():
    return render_template("play_v4.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                    player_info=player_info, usernames=usernames, riddle=riddle)                                

@app.route('/end_v4')
def end():
    flash("End of game")
    newlist = sorted(leaderboard, key=itemgetter('score'), reverse=True) # show leader board
    return render_template("end_v4.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                    players=player_info, usernames=usernames, newlist=newlist) 


def check_answer(answerInputByPlayer, correct_answer):
    '''
    Based on the username in session the inputed answer is compared against the actual riddle answer.
    If the answer is correct, the score is increased by 1, the leaderboard is updated. The index is increased by one to find next riddle in riddle list []
    If the answer is incorrect, the attempt is increased by 1. The user two attempts. The index is increased by one to find next riddle in riddle list []
    The next riddle index is returned
    '''
    
    for player in player_info:
        if player['username'] == session['username']:
            if correct_answer == answerInputByPlayer:
                flash("you are CORRECT. Answer:  {}, next question.".format(correct_answer))
                player['attempt'] = 0
                player['score'] += 1 # increase score by 1
                player['riddle_number'] += 1
                for leader in leaderboard:
                    if leader['username'] == session['username']:
                        leader['score'] += 1 # update leaderboard by 1
                #riddle_index += 1 # increase index by 1 for next riddle
                if (player['riddle_number'] < len(riddles)): # check for last riddle
                    return player['riddle_number'] 
            else:
                flash("WRONG try again, one more attempt")
                player['attempt'] += 1 # increase attempt by 1
                if player['attempt'] == 2: # max of 2 attempts
                    player['attempt'] = 0 # reset attempts back to 0
                    player['riddle_number'] += 1
                    #riddle_index += 1 # attempts over, next question
                    if (player['riddle_number'] < len(riddles)): #check for last riddle
                        return player['riddle_number'] 
            return player['riddle_number'] # index of next riddle


@app.route('/checkPlayerInput', methods=["GET", "POST"])
def check():
    '''
    The player answer is read from the form. The answer, the correct answer and the current riddle index is sent to check_answer()
    The returned riddle index is checked that it is not more than the number of riddles available.
    If the last riddle is complete, player is redirected to end() end.html
    If not the last riddle the index is passed to get_next_riddle() to get the next riddle from riddleList[]
    '''
    
    if request.method == "POST":
        player_answer = request.form['riddleAnswer'].title() # player answer from from input
        flash("Players answer: {}".format(player_answer))
        global riddle
        flash("Correct answer: {}".format(riddle["Answer"]))
        
        #riddle_number = request.form.get('riddle_number')
        #print(session['username'], riddle_number)
        next_riddle_index = check_answer(player_answer, riddle['Answer']) # check_answer() called. Index returned.
        #print(session['username'], riddle_number)
        if next_riddle_index > 2: # check for last riddle
            return redirect(url_for('end')) # end of game
        else:
            riddle = get_next_riddle(next_riddle_index) # not end of game, get next riddle
    return redirect(url_for('play'))    


@app.route('/', methods=["GET", "POST"])
def index():
    '''
    Get username from player and check if it's already taken
    '''
    if request.method == "POST":
        username = request.form['addUsername'].title() # username from from input
        if username not in usernames:
            usernames.append(username) # if its a new unique username, add to usernames[]
            session['username'] = username # add username to flask session
            flash("Success {}, your name is added. Her is your first question. The session is: {}".format(username, session))
            return redirect(url_for('start_game')) # start the game
        else:
            flash("Fail {}, Name taken try again".format(username)) # username taken try again until username is not in usernames[]  
    return render_template("index.html", page_title="Riddle-Me-This - Home", usernames=usernames, leaderboard=leaderboard)


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
    
    
    
    #riddles.index(riddle)
    
    
    
    
    
    
    
#request_username = request.args['username']
#username = ast.literal_eval(request_username)

#session.pop('_flashes', None)