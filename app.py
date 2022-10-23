from flask import Flask, render_template, request, flash
from helpers import connect_db, inch_to_ft, get_fighters_names, pick_random_fighter
import json
 
app = Flask(__name__)
app.secret_key = "543216789"
app.jinja_env.filters["inch_to_ft"] = inch_to_ft

guesses = []
num_guesses = 0

fighter_names = get_fighters_names()
fighter_names.sort()
answer = pick_random_fighter()

@app.route('/', methods=['GET', 'POST'])
def index():
    db = connect_db()
    
    global num_guesses
    
    if request.method == "GET":
        return render_template("index.html", fighter_names=json.dumps(fighter_names), answer=answer) 

    name = request.form.get("answer").lower()

    if num_guesses > 6:
        flash("Better luck next time!")  
    elif answer['name'] == name:
        flash("Correct!")

    if name in fighter_names:
        guesses.append(db.execute("SELECT name, hometown, debut, age, weight, height, reach, legreach FROM fighters WHERE name = ?", name))
        fighter_names.remove(name)
        num_guesses += 1

        return render_template("index.html", num_guesses=num_guesses, guesses=guesses, fighter_names=json.dumps(fighter_names),  answer=answer) 

    return render_template("index.html",num_guesses=num_guesses, guesses=guesses, fighter_names=json.dumps(fighter_names),  answer=answer)


if __name__ == '__main__':
    app.run(debug=True)