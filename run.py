import os
from riddlesList import * 
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'The cat is on the roof'
usernames = []
attempts = 0

def checkUsername(username):
    if username not in usernames:
        usernames.append(username)
        print(usernames)
        flash("Success {}, your name is added. Click play".format(username))
    else:
        flash("Fail {}, Name taken try again".format(username))
    return

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["addusername"]
        checkUsername(username)
    return render_template("index.html", page_title="Riddle-Me-This - Home")
    









    
@app.route('/play', methods=["GET", "POST"])
def play():
    if request.method == "POST":
        print(request.form)
    return render_template("play.html", page_title="Riddle-Me-This - Play")    


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)