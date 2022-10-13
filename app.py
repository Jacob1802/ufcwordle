from flask import Flask, render_template, request, redirect, Response
from fighters import get_fighters_names
from helpers import connect_db, inch_to_ft, get_fighters_names
import random
import json
 
app = Flask(__name__)

app.jinja_env.filters["inch_to_ft"] = inch_to_ft

guesses = []
num_guesses = 0

FIGHTERS = get_fighters_names()
FIGHTERS.sort()
random_fighter = FIGHTERS[random.randint(0, len(FIGHTERS) - 1)].title()
db = connect_db()
answer = db.execute("SELECT * FROM fighters WHERE name = 'conor mcgregor'")[0]
# answer = db.execute("SELECT * FROM fighters WHERE name = ?", random_fighter.lower())[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    db = connect_db()

    if request.method == "GET":
        return render_template("index.html", FIGHTERS=json.dumps(FIGHTERS), answer=answer) 

    global num_guesses
    num_guesses += 1

    name = request.form.get("answer").lower()

    if name in FIGHTERS:
        guesses.append(db.execute("SELECT name, hometown, debut, age, weight, height, reach, legreach FROM fighters WHERE name = ?", name))
        FIGHTERS.remove(name)
        print("Success")
        return render_template("index.html", guesses=guesses, FIGHTERS=json.dumps(FIGHTERS),  answer=answer) 

    print("Error")
    return render_template("index.html", guesses=guesses, FIGHTERS=json.dumps(FIGHTERS),  answer=answer)
 
if __name__ == '__main__':
    app.run(debug=True)