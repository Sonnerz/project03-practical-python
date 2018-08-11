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
    #return riddles[index] if index < 10 else None
    nextRiddle = riddles[riddleIndex]
    return nextRiddle

    


def check_answer(answerInputByPlayer, correctAnswer, riddleIndex):
    for player in playersInfo:
        if player['username'] == session['username']:
            if correctAnswer == answerInputByPlayer:
                flash("you are CORRECT. Answer:  {}, next question.".format(correctAnswer))
                player['score'] += 1 #increase score by 1
                leaderboard.update({session['username']:player['score']}) #update leaderboard
                riddleIndex += 1 #increase index by 1
                if (riddleIndex <= 2): #check for last riddle
                    riddle = get_next_riddle(riddleIndex) #returns a dictionary NEXT RIDDLE
                    print("riddleIndex: ", riddleIndex,   "riddleNumber: ", riddle['Number'])
                    return riddle
                else:
                    redirect(url_for('end'))
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
                return    
            return redirect(url_for('play'))


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

@app.route('/end', methods=["GET", "POST"])
def end():
    flash("End of game")
    return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                                    players=playersInfo, usernames=usernames) 


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













#riddleIndex=riddles.index(riddle), riddleQ=riddle['Question'], riddleA=riddle['Answer']


            #for score, attempt, username in item:#.iteritems():
            #    if (username == session['username']):
            #        print(score, attempt)


#'hello world'[::-1] #reverse the answer

# firstRiddle=getNextRiddle(1)
# print(type(firstRiddle))
# print(firstRiddle['Question'])
# print(firstRiddle['Answer'])
# print(riddles.index(firstRiddle))

#session.pop('_flashes', None) # Clear flashed messages if we're on the final question
#session.pop('username', None)
#nextRiddle=nextRiddle['Question']

    #first_riddleQ = riddles[0]['Question']
    #first_riddleA = riddles[0]['Answer'].title()
#firstRiddleQ = first_riddleQ, 


       
        #print(riddle.items())
        #for key in riddle.items():
            #print("Key: ", key)





# @app.route('/index2')
# def index2():
#     return render_template("index2.html", page_title="Riddle-Me-This - Home")
    
# @app.route('/instructions', methods=["GET", "POST"])
# def instructions():
#     username = request.form["addusername"].title()
#     return render_template("instructions.html", context={'username': 'test'})
    
    
"""
Logic:

1. User enters a username
2. Upon submit, GET riddle page fron the riddle function
3. Riddle page displays:
    - the question
    - a textbox for the answer
    - submit button to submit the answer
4. User submits their answer
5. POST to the riddle function with the answer
6. Check the answer against a list of answers
7. Return correct or incorrect with the same template and iterate to the next question
"""


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)