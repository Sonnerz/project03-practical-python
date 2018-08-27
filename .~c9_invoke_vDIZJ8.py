import os
import ast
import math
import sys 
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
                # start the game
                return redirect(url_for('start_game')) 
    except Exception as e:
        return render_template("500.html", error=e)
    return render_template("index.html", page_title="Riddle-Me-This - Home",length=length, player_info=player_info, usernames=usernames, leaderboard=leaderboard)     
      


def check_username(username):
    '''
    check if username is already taken or in session so that user can start/restart/resume
    '''
    in_usernames_list = username in usernames
    in_session = session.get('username') == username
    in_both = in_usernames_list and in_session
    in_neither = not in_usernames_list and not in_session
    if not in_usernames_list and in_session or in_usernames_list and not in_session or in_both:
        if not in_usernames_list:
            usernames.append(username)
        if not in_session:
            session['username']=username            
        for player in player_info:
            if player['username'] == username and player['riddle_number'] == len(riddles):
                flash("You have already completed the 10 riddles. You can try again")
                player.update({"restart":True,"resume":False,"riddle_number":0,"score":0,"attempt_total":0,"wrong":0,"attempts":0 })
            elif player['username'] == username and player['riddle_number'] != len(riddles):
                player.update({"resume":True,"restart":False})
        return True
    elif in_neither:
        # if its a new unique username, add to usernames[]
        usernames.append(username)
        # add username to flask session
        session['username'] = username 
        return True        
    else:
         # username taken try again until username is not in usernames[] 
        flash("{}, this player name has been taken, please try a different name.".format(username)) 
        return render_template("index.html", page_title="Riddle-Me-This - Home",  usernames=usernames, leaderboard=leaderboard) 
         


@app.route('/start_game', methods=["GET", "POST"])
def start_game():
    '''
    Intialise 'riddle' dictionary. Checks if user is starting/restarting/resuming a game.
    Populate 'player' with player info to track their progress.
    Get the first riddle to start the game, 
    or get the current riddle a player is on if resuming a game
    or get the first riddle if a player is resuming
    '''
    global riddle
    for player in player_info:
        if player['resume'] == True:
            # returns NEXT riddle for that player
            riddle = get_riddle(player['riddle_number'])
            player.update({"resume":False})
            return redirect(url_for('play'))
        if player['restart'] == True:
            # returns FIRST riddle
            riddle = get_riddle(0)
            player.update({"restart":False})
            return redirect(url_for('play'))
    else:
        create_player(session['username'])
        # returns FIRST riddle
        riddle = get_riddle(0)
        
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



@app.route('/checkPlayerInput', methods=["GET", "POST"])
def check():
    '''
    The player answer is read from the form. The answer, the correct answer and the current riddle index is sent to check_answer()
    The returned riddle index is checked that it is not more than the number of riddles available.
    If the last riddle is complete, player is redirected to end() end.html
    If not the last riddle the index is passed to get_next_riddle() to get the next riddle from riddleList[]
    '''
    global riddle
    if request.method == "POST":
        # get player answer from form
        player_answer = request.form['riddleAnswer']
        # get player current riddle number from form
        player_current_riddle_number = int(request.form['player_current_riddle_number']) 
        # check if answer is a digit instead of text e.g. 7 instead of seven
        if player_answer.isdigit(): 
            # send to helper function
            checked_player_answer = number_to_string(int(player_answer)) 
        else:
            # reset player_answer var with checked answer
            checked_player_answer = player_answer
        # get the correct riddle for that player    
        current_riddle = get_riddle(player_current_riddle_number)
        # check_answer() called. Index of next riddle returned.
        player = check_answer(checked_player_answer.lower(), current_riddle) 
        # check for last riddle
        if player['riddle_number'] < len(riddles): 
            riddle = get_riddle(player['riddle_number'])
        else:
            # set Riddle Number to length of riddles list
            riddle = {'Number':len(riddles)}
            # date now
            date_completed = datetime.now().strftime("%d-%m-%Y") 
            leaderboard.append({"username": session['username'], "score": player['score'], "timestamp":date_completed})
            redirect(url_for('play')) 
    return redirect(url_for('play'))    



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
                # flash - player told answer is correct
                flash("Correct! The answer was:  {}.".format(riddle['Answer'])) 
                player['attempt'] = 0
                # increase score by 1
                player['score'] += 1 
                # increase riddle number by 1
                player['riddle_number'] += 1 
                # check for last riddle
                if (player['riddle_number'] < len(riddles)): 
                    return player # player
            else:
                # flash - player told answer is incorrect
                flash("{} is incorrect.".format(answerInputByPlayer)) 
                # increase attempt by 1
                player['attempt'] += 1 
                # increase attempt_total by 1
                player['attempt_total'] += 1
                # max of 2 attempts reached
                if player['attempt'] == 2: 
                    # increase wrong count by 1
                    player['wrong'] += 1 
                    # flash - player told the correct answer
                    flash("{} was the correct answer.".format(riddle['Answer'])) 
                    # reset attempts back to 0
                    player['attempt'] = 0 
                    # increase riddle number by 1
                    player['riddle_number'] += 1 
                    # check for last riddle
                    if (player['riddle_number'] < len(riddles)): 
                        return player
            return player


 
@app.route('/end')
def end():
    '''
    User is told the game is over. Their score is added to the Leader Boad List. The leader board list is sorted by Score and rendered to the browser.
    The session is cleared. Else the leaderboard is still rendered to the broswer if there are games in session at the same time.
    '''
    try:
        # show leader board list sorted by score
        sorted_leaderboard_list = sorted(leaderboard, key=itemgetter('score'), reverse=True) 
        return render_template("end.html", page_title="Riddle-Me-This - Game Over", session=session, leaderboard=leaderboard, players=player_info, sorted_leaderboard_list=sorted_leaderboard_list)
    except Exception as e:
        return render_template("500.html", error=e)  




@app.context_processor
def debug_on_off():
    return dict(debug=app.debug)
    

def get_riddle(riddleIndex):
    '''
    If answer is correct or attempts are more than two, get the next riddle from the riddle List, based on the riddle number
    '''
    # get next riddle by passing index to riddles[] and return the riddle {} dictionary
    nextRiddle = riddles[riddleIndex] 
    return nextRiddle


def create_player(username):
    '''
    Creates a player dict{} in player_info List to track the players; score, attempts, wrong, current riddle number, 
    total attempts, whether they are resuming a game or restarting after completeing the game.
    '''
    #creates a player dict{}
    player_info.append({"username":username, "score":0, "attempt":0, "wrong":0, "riddle_number":0, "attempt_total":0, "restart":False, "resume":False}) 
    return player_info


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
    








































































































































































































































