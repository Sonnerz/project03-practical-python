import os
import ast
from flask import Markup
from datetime import datetime
from riddlesList import content
from operator import itemgetter
from flask import Flask, render_template, request, flash, redirect, url_for, session, current_app

riddles = content()        

app = Flask(__name__)
app.secret_key = 'The cat is on the roof'
usernames = []
leaderboard = [{"username": "sonya", "score": 4, "timestamp":"10:15:23"}]
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
    player_info.append({"username":username, "score":0, "attempt":0, "riddle_number":0}) #creates a player
    return player_info


@app.route('/start_game', methods=["GET", "POST"])
def start_game():
    '''
    Intialise the global lists and riddle dictionary. Populate with the player info to track their progress.
    Get the first riddle to start the game. Redirect to the game html page - play() play.html.
    '''
    #leaderboard.append({"username":session['username'], "score":0, "timestamp":date}) # added to leaderboard
    create_player(session['username'])
    global riddle
    riddle = get_next_riddle(0) #returns a dictionary FIRST RIDDLE
    return redirect(url_for('play'))    


@app.route('/play')
def play():
    return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                        player_info=player_info, usernames=usernames, riddle=riddle, session=session)

@app.route('/end')
def end():
        try:
            if session.get('username'):
                gameend_message = Markup("<strong>{}</strong> your Game is Over!<br>View the leaderboard below".format(session['username']))
                flash(gameend_message)
                date_completed = datetime.now().strftime("%d-%m-%Y")
                for player in player_info:
                    if player['username'] == session['username']:
                        leaderboard.append({"username": session['username'], "score": player['score'], "timestamp":date_completed}) # added to leaderboard
                sorted_leaderboard_list = sorted(leaderboard, key=itemgetter('score'), reverse=True) # show sorted by score leader board
                session.pop('username', None)
                return render_template("end.html", page_title="Riddle-Me-This - Game Over", session=session, leaderboard=leaderboard, players=player_info, sorted_leaderboard_list=sorted_leaderboard_list)
            else:
                sorted_leaderboard_list = sorted(leaderboard, key=itemgetter('score'), reverse=True) # show sorted by score leader board
                return render_template("end.html", page_title="Riddle-Me-This - Game Over", leaderboard=leaderboard, sorted_leaderboard_list=sorted_leaderboard_list)
        except Exception as e:
            return render_template("500.html", error=e)        
                
    


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
                flash("Correct! The answer was:  {}.".format(correct_answer))
                player['attempt'] = 0
                player['score'] += 1 # increase score by 1
                player['riddle_number'] += 1
                if (player['riddle_number'] < len(riddles)): # check for last riddle
                    return player['riddle_number'] 
            else:
                flash("{} is incorrect.".format(answerInputByPlayer)) # flash(incorrect_message)
                player['attempt'] += 1 # increase attempt by 1
                if player['attempt'] == 2: # max of 2 attempts
                    flash("{} was the correct answer.".format(correct_answer)) # flash(incorrect_message)
                    player['attempt'] = 0 # reset attempts back to 0
                    player['riddle_number'] += 1                    #riddle_index += 1 # attempts over, next question
                    if (player['riddle_number'] < len(riddles)): #check for last riddle
                        return player['riddle_number'] 
            return player['riddle_number'] # index of next riddle

def number_to_string(number):
    '''
    Helper function - to change a digit to a word of number e.g. 7 to seven
    '''
    switcher = {
        1: "One",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six",
        7: "Seven",
        8: "Eight",
        9: "Nine",
        10: "Ten",
        18: "Eighteen"
    }
    return switcher.get(number, "Invalid number")
    
        

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
        next_riddle_index = check_answer(checked_player_answer.title(), riddle['Answer']) # check_answer() called. Index of next riddle returned.
        if next_riddle_index == len(riddles): # check for last riddle
            return redirect(url_for('end')) # end of game
        else:
            riddle = get_next_riddle(next_riddle_index) # not end of game, get next riddle
    return redirect(url_for('play'))    



def check_username(username):
    '''
    check if it's already taken
    '''
    if (username not in usernames) and session.get('username') == username:
        message_false = Markup("{}, a game with this name has already started. You cannot continue or restart this game.<br>Register with a new name".format(username))
        flash(message_false) # username taken try again until username is not in usernames[]  
        return False
    elif (username in usernames) and not session.get('username') == username:
        message_false = Markup("{}, this name has already been taken. <br>Enter a different player name".format(username))
        flash(message_false) # username taken try again until username is not in usernames[]  
        return False
    elif (username in usernames) and session.get('username') == username:
        message_false = Markup("{}, a game with this name has already started. You cannot continue or restart this game.<br>Register with a new name".format(username))
        flash(message_false) # username taken try again and usnername already in a session - so game underway  
        return False
    elif (username not in usernames):
        usernames.append(username) # if its a new unique username, add to usernames[]
        session['username'] = username # add username to flask session
        return True        
    else:
        flash("{}, this player name has been taken, please try a different name.".format(username)) # username taken try again until username is not in usernames[]  
        return render_template("index.html", page_title="Riddle-Me-This - Home", usernames=usernames, leaderboard=leaderboard) 
   
    


@app.route('/', methods=["GET", "POST"])
def index():
    '''
    Get username from form
    '''
    #session.pop('username', None)
    session.pop('_flashes', None)
    try:
        if request.method == "POST":
            username_from_form = request.form['addUsername'].title()
            if check_username(username_from_form):
                return redirect(url_for('start_game')) # start the game
    except Exception as e:
        return render_template("500.html", error=e)
    return render_template("index.html", page_title="Riddle-Me-This - Home", usernames=usernames, leaderboard=leaderboard)     
      


    
@app.errorhandler(404)
def page_not_found(error):
    '''
    404 error is redirected to 404.html
    '''
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    '''
    500 error is redirected to 500.html
    '''
    session.pop('_flashes', None)
    session.pop('username', None)
    return render_template('500.html'), 500  
    


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
    
    
    
# incorrect_message = Markup("<strong>{}</strong> is incorrect.<br> Please try again, you have one more attempt".format(answerInputByPlayer)) 
