        if session.get('username'):
            for player in player_info:
                if session['username'] == player['username'] and player['riddle_number'] <= len(riddles)-1:
                    print("player['riddle_number']", player['riddle_number'])
                    riddle = get_next_riddle(player['riddle_number'])
                    print("riddle :", riddle)
                length_of_riddles = len(riddles)

#---------               
    for player in player_info:
        if player['username'] == session['username'] and player['resume'] == True and player['restart'] == False:
            global riddle
            riddle = get_next_riddle(player['riddle_number']) #returns a dictionary FIRST RIDDLE
            player.update({"resume":False})
            return redirect(url_for('play'))
        elif player['username'] == session['username'] and player['resume'] == False and player['restart'] == True:
            global riddle
            riddle = get_next_riddle(0) #returns a dictionary FIRST RIDDLE
            player.update({"restart":False})
            return redirect(url_for('play')) 
        elif player['username'] == session['username'] and player['resume'] == False and player['restart'] == False:
            global riddle
            riddle = get_next_riddle(0) #returns a dictionary FIRST RIDDLE
            return redirect(url_for('play'))            
    else:
        create_player(session['username'])
        global riddle
        riddle = get_next_riddle(0) #returns a dictionary FIRST RIDDLE
        return redirect(url_for('play'))  
        
        
#----------
@app.route('/play')
def play():
    '''
    If no session is running this page can't be accessed. User is redirected to index page
    '''
    try:
        if session.get('username'):
            for player in player_info:
                if player['username'] == session['username'] and player['restart'] == False:
                    length_of_riddles = len(riddles)
                    return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                            player_info=player_info, player=player, usernames=usernames, riddle=riddle, session=session, length_of_riddles=length_of_riddles)
                elif player['username'] == session['username'] and player['restart'] == True:
                    length_of_riddles = len(riddles)
                    return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                            player_info=player_info, player=player, usernames=usernames, riddle=riddle, session=session, length_of_riddles=length_of_riddles)
        else:
            return redirect(url_for('index')) 
    except Exception as e:
        return render_template("500.html", error=e)
        
        
#-------
def check_username(username):
    '''
    check if it's already taken
    '''
    if username not in usernames and session.get('username') == username:
        usernames.append(username)
        for player in player_info:
            if player['username'] == username and player['riddle_number'] == len(riddles):
                flash("You have already completed the 10 riddles. You can try again")
                player.update({"restart":True,"resume":False,"riddle_number":0,"score":0,"attempt_total":0,"wrong":0,"attempts":0 })
                return True
            elif player['username'] == username and player['riddle_number'] != len(riddles):
                player.update({"resume":True,"restart":False})
                return True
        return True
    elif username in usernames and not session.get('username') == username:
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
    elif username in usernames and session.get('username') == username:
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
        