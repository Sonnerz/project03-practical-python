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




def create_player(username, riddle):
    '''
    Creates a player dict{} in player_info List to track the players; score, attempts and their current riddle
    '''
    player_info.append({"first":True, "username":username, "score":0, "attempt":0, "wrong":0, "riddle_number":0, "attempt_total":0, "riddle_question":riddle['Question'], "riddle_answer":riddle['Answer'], "riddle_path":riddle['Path']}) #creates a player
    return player_info


@app.route('/start_game', methods=["GET", "POST"])
def start_game():
    '''
    Intialise the global lists and riddle dictionary. Populate with the player info to track their progress.
    Get the first riddle to start the game. Redirect to the game html page - play() play.html.
    '''
    # global riddle
    riddle = get_next_riddle(0) #returns a dictionary FIRST RIDDLE
    create_player(session['username'], riddle)
    return redirect(url_for('play')) 
    
def get_player(session_username):
    for player in player_info:
        if session_username == player['username']:
            return player    
    
    
@app.route('/play')
def play():
    '''
    If no session is running this page can't be accessed. User is redirected to index page
    '''
    player = get_player(session['username'])
    length_of_riddles = len(riddles)
    if session.get('username') and player['first'] == True:
        if session['username'] == player['username'] and player['riddle_number'] <= len(riddles)-1:
            riddle = get_next_riddle(player['riddle_number'])
            player.update({"riddle_question":riddle['Question'], "riddle_answer":riddle['Answer'], "riddle_path":riddle['Path'], "first":False,}) #creates a players
            return render_template("play.html", page_title="Riddle-Me-This - Play", leaderboard=leaderboard, 
                                                player_info=player_info, player=player, usernames=usernames, session=session, length_of_riddles=length_of_riddles)
    elif session['username'] == player['username'] and player['riddle_number'] <= len(riddles)-1:
        riddle = get_next_riddle(player['riddle_number'])
        return render_template("play.html", page_title="Riddle-Me-This - Play", leaderboard=leaderboard, 
                                                player_info=player_info, player=player, usernames=usernames, session=session, length_of_riddles=length_of_riddles)
    else:
        return render_template("play.html", page_title="Riddle-Me-This - Play", leaderboard=leaderboard, 
                                player_info=player_info, player=player, usernames=usernames, session=session, length_of_riddles=length_of_riddles)
    #return redirect(url_for('index'))
    return render_template("play.html", page_title="Riddle-Me-This - Play", leaderboard=leaderboard, 
                                        player_info=player_info, player=player, usernames=usernames, session=session, length_of_riddles=length_of_riddles)
    
    #try:
        # player = get_player(session['username'])
        # length_of_riddles = len(riddles)
        # if session.get('username') and player.first == True:
        #     if session['username'] == player['username'] and player['riddle_number'] <= len(riddles)-1:
        #         riddle = get_next_riddle(player['riddle_number'])
        #         player.update({"riddle_question":riddle['Question'], "riddle_answer":riddle['Answer'], "riddle_path":riddle['Path'], "first":False,}) #creates a players
        #         return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
        #                                         player_info=player_info, player=player, usernames=usernames, session=session, length_of_riddles=length_of_riddles)
        #     else:                                                
        #         return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
        #                                 player_info=player_info, player=player, usernames=usernames, session=session, length_of_riddles=length_of_riddles)
        # else:
        #     return redirect(url_for('index')) 
    #except Exception as e:
        #return render_template("500.html", error=e)
        #return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
        #                        player_info=player_info, player=player, usernames=usernames, session=session, length_of_riddles=length_of_riddles)

      

@app.route('/end')
def end():
    '''
    User is told the game is over. Their score is added to the Leader Boad List. The leader board list is sorted by Score and rendered to the browser.
    The session is cleared. Else the leaderboard is still rendered to the broswer if there are games in session at the same time.
    '''
    try:
        # if session.get('username'):
        #     date_completed = datetime.now().strftime("%d-%m-%Y") # date now
        #     for player in player_info:
        #         if not leaderboard:
        #             leaderboard.append({"username": session['username'], "score": player['score'], "timestamp":date_completed}) # added to leaderboard list
        #         else:    
        #             for leader in leaderboard:
        #                 print(leaderboard)
        #                 if player['username'] == session['username'] and player['username'] != leader['username']:
        #                     print(player['username'] ,session['username'] , player['username'] , leader['username'])
        #                     leaderboard.append({"username": session['username'], "score": player['score'], "timestamp":date_completed}) # added to leaderboard list
            sorted_leaderboard_list = sorted(leaderboard, key=itemgetter('score'), reverse=True) # show leader board list sorted by score
            #session.pop('username', None) # clear the session
            return render_template("end.html", page_title="Riddle-Me-This - Game Over", session=session, leaderboard=leaderboard, players=player_info, sorted_leaderboard_list=sorted_leaderboard_list)
        # else:
        #     sorted_leaderboard_list = sorted(leaderboard, key=itemgetter('score'), reverse=True) # show leader board list sorted by score 
        #     return render_template("end.html", page_title="Riddle-Me-This - Game Over", leaderboard=leaderboard, sorted_leaderboard_list=sorted_leaderboard_list)
    except Exception as e:
        return render_template("500.html", error=e)        
                
    

def check_answer(answerInputByPlayer):
    '''
    Based on the username in session the inputed answer is compared against the actual riddle answer.
    If the answer is correct, the score is increased by 1, the leaderboard is updated. The index is increased by one to find next riddle in riddle list []
    If the answer is incorrect, the attempt is increased by 1. The user two attempts. The index is increased by one to find next riddle in riddle list []
    The next riddle index is returned
    '''
    for player in player_info:
        if player['username'] == session['username']:
            if player['riddle_answer'] == answerInputByPlayer:
                flash("Correct! The answer was:  {}.".format(player['riddle_answer'])) # flash - player told answer is correct
                player['attempt'] = 0
                player['score'] += 1 # increase score by 1
                player['riddle_number'] += 1 # increase riddle number by 1
                if (player['riddle_number'] < len(riddles)): # check for last riddle
                    return player # player
            else:
                flash("{} is incorrect.".format(answerInputByPlayer)) # flash - player told answer is incorrect
                player['attempt'] += 1 # increase attempt by 1
                player['attempt_total'] +1# increase attempt_total by 1
                if player['attempt'] == 2: # max of 2 attempts reached
                    player['wrong'] += 1 # increase wrong count by 1
                    player['attempt_total'] +=2 # increase attempt_total by 2
                    flash("{} was the correct answer.".format(player['riddle_answer'])) # flash - player told the correct answer
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
        player = check_answer(checked_player_answer.lower()) # check_answer() called. Index of next riddle returned.
        if player['riddle_number'] < len(riddles): # check for last riddle
            next_riddle = get_next_riddle(player['riddle_number'])
            player.update({"riddle_question":next_riddle['Question'], "riddle_answer":next_riddle['Answer'], "riddle_path":next_riddle['Path']}) #creates a players
        else:
            player['riddle_number'] = len(riddles) # set Riddle Number to length of riddles list
            date_completed = datetime.now().strftime("%d-%m-%Y") # date now
            print("leaderboard updated")
            print(player['riddle_number'])
            leaderboard.append({"username": session['username'], "score": player['score'], "timestamp":date_completed})
            redirect(url_for('play')) 
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
            username_from_form = request.form['addUsername']
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
