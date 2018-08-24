import os
import ast
import math
import sys 
# sys.path.append('/static/data')
# import riddlesList.py
from flask import Markup
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


@app.context_processor
def debug_on_off():
    return dict(debug=app.debug)

def get_next_riddle(riddleIndex):
    '''
    If answer is correct or attempts are more than two, get the next riddle from the riddle List, based on the riddle number
    '''
    nextRiddle = riddles[riddleIndex] # get next riddle by passing index to riddles[] and return the riddle {} dictionary
    return nextRiddle


def create_player(username):
    '''
    Creates a player dict{} in player_info List to track the players; score, attempts, wrong, current riddle number, 
    total attempts, whether they are resuming a game or restarting after completeing the game.
    '''
    player_info.append({"username":username, "score":0, "attempt":0, "wrong":0, "riddle_number":0, "attempt_total":0, "restart":False, "resume":False}) #creates a player dict{}
    return player_info


@app.route('/start_game', methods=["GET", "POST"])
def start_game():
    '''
    Intialise 'riddle' dictionary. Checks if user is starting/restarting/resuming a game.
    Populate 'player' with player info to track their progress.
    Get the first riddle to start the game, 
    or get the current riddle a player is on if resuming a game
    or get the first riddle if a player is resuming
    '''
    for player in player_info:
        if player['username'] == session['username'] and player['resume'] == True and player['restart'] == False:
            global riddle
            riddle = get_next_riddle(player['riddle_number']) #returns a dictionary FIRST RIDDLE
            player.update({"resume":False})
            return redirect(url_for('play'))
        elif player['username'] == session['username'] and player['resume'] == False and player['restart'] == True or player['username'] == session['username'] and player['resume'] == False and player['restart'] == False:
            global riddle
            riddle = get_next_riddle(0) #returns a dictionary FIRST RIDDLE
            if player['restart'] == True:
                player.update({"restart":False})
            return redirect(url_for('play'))
    else:
        create_player(session['username'])
        global riddle
        riddle = get_next_riddle(0) #returns a dictionary FIRST RIDDLE
        return redirect(url_for('play'))    

@app.route('/play')
def play():
    '''
    If no session is running this page can't be accessed. User is redirected to index page
    '''
    try:
        if session.get('username'):
            for player in player_info:
                if player['username'] == session['username'] and player['restart'] == False or player['username'] == session['username'] and player['restart'] == True:
                    length_of_riddles = len(riddles)
                    return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                            player_info=player_info, player=player, usernames=usernames, riddle=riddle, session=session, length_of_riddles=length_of_riddles)
        else:
            return redirect(url_for('index')) 
    except Exception as e:
        return render_template("500.html", error=e)


@app.route('/end')
def end():
    '''
    User is told the game is over. Their score is added to the Leader Boad List. The leader board list is sorted by Score and rendered to the browser.
    The session is cleared. Else the leaderboard is still rendered to the broswer if there are games in session at the same time.
    '''
    try:
        sorted_leaderboard_list = sorted(leaderboard, key=itemgetter('score'), reverse=True) # show leader board list sorted by score
        return render_template("end.html", page_title="Riddle-Me-This - Game Over", session=session, leaderboard=leaderboard, players=player_info, sorted_leaderboard_list=sorted_leaderboard_list)
    except Exception as e:
        return render_template("500.html", error=e)        
                
    

def check_answer(answerInputByPlayer, riddle):
    '''
    Based on the username in session the inputed answer is compared against the actual riddle answer.
    If the answer is correct, the score is increased by 1, the leaderboard is updated. The index is increased by one to find next riddle in riddle list []
    If the answer is incorrect, the attempt is increased by 1. The user two attempts. The index is increased by one to find next riddle in riddle list []
    The next riddle index is returned
    '''
    for player in player_info:
        if player['username'] == session['username']:
            if riddle['Answer'] == answerInputByPlayer:
                flash("Correct! The answer was:  {}.".format(riddle['Answer'])) # flash - player told answer is correct
                player['attempt'] = 0
                player['score'] += 1 # increase score by 1
                player['riddle_number'] += 1 # increase riddle number by 1
                if (player['riddle_number'] < len(riddles)): # check for last riddle
                    return player # player
            else:
                flash("{} is incorrect.".format(answerInputByPlayer)) # flash - player told answer is incorrect
                player['attempt_total'] = 0
                player['attempt'] += 1 # increase attempt by 1
                player['attempt_total'] += 1# increase attempt_total by 1
                if player['attempt'] == 2: # max of 2 attempts reached
                    player['wrong'] += 1 # increase wrong count by 1
                    player['attempt_total'] += 1 # increase attempt_total by 1
                    flash("{} was the correct answer.".format(riddle['Answer'])) # flash - player told the correct answer
                    player['attempt'] = 0 # reset attempts back to 0
                    player['riddle_number'] += 1 # increase riddle number by 1
                    if (player['riddle_number'] < len(riddles)): # check for last riddle
                        return player # return player
            return player # return player


def number_to_string(number):
    '''
    Helper function - to change a digit to the word version of a number e.g. 7 to seven
    '''
    switcher = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        18: "eighteen"
    }
    return switcher.get(number, str(number))
    
        

@app.route('/checkPlayerInput', methods=["GET", "POST"])
def check():
    '''
    The player answer is read from the form. The answer, the correct answer and the current riddle index is sent to check_answer()
    The returned riddle index is checked that it is not more than the number of riddles available.
    If the last riddle is complete, player is redirected to end() end.html
    If not the last riddle the index is passed to get_next_riddle() to get the next riddle from riddleList[]
    '''
    if request.method == "POST":
        player_answer = request.form['riddleAnswer'] # get player answer from form
        if player_answer.isdigit(): #check if answer is a digit instead of text e.g. 7 instead of seven
            checked_player_answer = number_to_string(int(player_answer)) # send to helper function
        else:
            checked_player_answer = player_answer # reset player_answer var with checked answer
        global riddle
        player = check_answer(checked_player_answer.lower(), riddle) # check_answer() called. Index of next riddle returned.
        if player['riddle_number'] < len(riddles): # check for last riddle
            riddle = get_next_riddle(player['riddle_number'])
        else:
            riddle = {'Number':len(riddles)} # set Riddle Number to length of riddles list
            date_completed = datetime.now().strftime("%d-%m-%Y") # date now
            leaderboard.append({"username": session['username'], "score": player['score'], "timestamp":date_completed})
            redirect(url_for('play')) 
    return redirect(url_for('play'))    



def check_username(username):
    '''
    check if it's already taken
    '''
    if username not in usernames and session.get('username') == username or username in usernames and not session.get('username') == username or username in usernames and session.get('username') == username:
        if username not in usernames:
            usernames.append(username)
        if not session.get('username') == username:
            session['username'] = username
        for player in player_info:
            if player['username'] == username and player['riddle_number'] == len(riddles):
                flash("You have already completed the 10 riddles. You can try again")
                player.update({"restart":True,"resume":False,"riddle_number":0,"score":0,"attempt_total":0,"wrong":0,"attempts":0 })
                return True
            elif player['username'] == username and player['riddle_number'] != len(riddles):
                player.update({"resume":True,"restart":False})
                return True
        return True
    elif username not in usernames:
        usernames.append(username) # if its a new unique username, add to usernames[]
        session['username'] = username # add username to flask session
        return True        
    else:
        flash("{}, this player name has been taken, please try a different name.".format(username)) # username taken try again until username is not in usernames[]  
        return render_template("index.html", page_title="Riddle-Me-This - Home",  usernames=usernames, leaderboard=leaderboard) 
   
    


@app.route('/', methods=["GET", "POST"])
def index():
    '''
    Get username from form
    '''
    #session.pop('username', None)
    session.pop('_flashes', None)
    length = len(riddles)
    try:
        if request.method == "POST":
            username_from_form = request.form['addUsername']
            if check_username(username_from_form):
                return redirect(url_for('start_game')) # start the game
    except Exception as e:
        return render_template("500.html", error=e)
    return render_template("index.html", page_title="Riddle-Me-This - Home",length=length, player_info=player_info, usernames=usernames, leaderboard=leaderboard)     
      


    
@app.errorhandler(404)
def page_not_found(error):
    '''
    404 error is redirected to 404.html
    '''
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
    '''
    500 error is redirected to 500.html
    '''
    session.pop('_flashes', None)
    session.pop('username', None)
    return render_template('500.html') 
    


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
    
    
    
# incorrect_message = Markup("<strong>{}</strong> is incorrect.<br> Please try again, you have one more attempt".format(answerInputByPlayer)) 
