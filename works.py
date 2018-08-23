        if session.get('username'):
            for player in player_info:
                if session['username'] == player['username'] and player['riddle_number'] <= len(riddles)-1:
                    print("player['riddle_number']", player['riddle_number'])
                    riddle = get_next_riddle(player['riddle_number'])
                    print("riddle :", riddle)
                length_of_riddles = len(riddles)