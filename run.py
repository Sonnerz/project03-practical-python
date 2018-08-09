import os
from riddlesList import content
from flask import Flask, render_template, request, flash, redirect, url_for, session

riddles = content()

app = Flask(__name__)
app.secret_key = 'The cat is on the roof'
usernames = []
leaderboard = {}
players = []

def create_player(username):
    players.append({"username":username, "score":0, "attempts":0})
    return


def get_next_riddle(riddleIndex):
    nextRiddle = riddles[riddleIndex]
    return nextRiddle


def check_answer(answerInputByPlayer, correctAnswer, riddleIndex):
    if correctAnswer == answerInputByPlayer:
        flash("you are CORRECT answer {}, next question.".format(correctAnswer))
        for item in players:
            print(item) #{'attempts': 0, 'score': 0, 'username': 'Harley'}{'attempts': 0, 'score': 0, 'username': 'Bob'}{'attempts': 0, 'score': 0, 'username': 'Zed'}
            print(item['score'], item['attempts'], item['username'])#0 0 Zed 0 0 Bob 0 0 Harley
            #for score, attempt, username in item:#.iteritems():
            #    if (username == session['username']):
            #        print(score, attempt)   
        
        
        #riddleIndex += 1
        #leaderboard.update({session['username']:score})
        #riddle = get_next_riddle(riddleIndex) #returns a dictionary NEXT RIDDLE
        #return riddle
    else:
        global attempts
        attempts += 1
        if attempts == 2:
            flash("you are WRONG two attempts, the answer is: {}".format(correctAnswer))
            attempts = 0
        else:
            flash("WRONG try again, one more attempt")
    return


@app.route('/play', methods=["GET", "POST"])
def play():
    riddle = get_next_riddle(0) #returns a dictionary FIRST RIDDLE
    if request.method == "POST":
        userAnswer = request.form['riddleAnswer'].title()
        flash("players answer {}: ".format(userAnswer))
        flash("correct answer {}: ".format(riddle["Answer"]))
        check_answer(userAnswer, riddle['Answer'], riddles.index(riddle))
    return render_template("play.html", page_title="Riddle-Me-This - Play", username=session['username'], leaderboard=leaderboard, 
                            players=players, usernames=usernames, riddleQ=riddle["Question"])



@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "POST":
        username = request.form['addUsername'].title()
        if username not in usernames:
            usernames.append(username)
            flash("Success {}, your name is added. First Question".format(username))
            session['username'] = username
            leaderboard.update({username:0})
            create_player(username)
            return redirect('play')
        else:
            flash("Fail {}, Name taken try again".format(username))     
    return render_template("index.html", page_title="Riddle-Me-This - Home", username=session['username'], usernames=usernames, leaderboard=leaderboard)



#riddleIndex=riddles.index(riddle), riddleQ=riddle['Question'], riddleA=riddle['Answer']





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
        # flash("Riddles: {}.".format(riddles)) #[{'Answer': 'Name', 'Question': 'What belongs to you but others use it more than you do?'}, {'Answer': 'Hole', 'Question': 'The more you take aways, the larger it becomes? What is it?'}].
        # flash("riddle #1: {}".format(riddles[0].values())) #dict_values(['What belongs to you but others use it more than you do?', 'Name'])
        # flash("riddle #1 Q: {}".format(riddles[0]['Question'])) #What belongs to you but others use it more than you do?
        # flash("riddle #1 A: {}".format(riddles[0]['Answer']))

        #riddleA = riddle['Answer'].title()
        
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