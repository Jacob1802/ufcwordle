from flask import Flask, render_template, request, flash, session, jsonify
from helpers import connect_db, inch_to_ft, get_fighters_names, pick_random_fighter
import json


app = Flask(__name__)
app.secret_key = "543216789"
app.jinja_env.filters["inch_to_ft"] = inch_to_ft

features = ['name', 'hometown', 'debut', 'age', 'weight', 'height']

def build_game():
    session['guesses'] = []
    session['num_guesses'] = 0
    session['fighter_names'] = get_fighters_names()
    session['fighter_names'].sort()
    session['answer'] = pick_random_fighter()
    session['game_over'] = False


@app.route('/', methods=['GET', 'POST'])
def index():
    db = connect_db()

    # Initialize session variables if not already initialized
    if 'answer' not in session:
        build_game()
    
    if request.method == "GET":
        return render_template("index.html", fighter_names=json.dumps(session['fighter_names']), answer=session['answer']) 

    name = request.form.get("guess").lower()
    
    if session['answer']['name'].lower() == name:
        show_answer('correct')
        flash("Correct!")
        session['game_over'] = True
        return render_template("index.html", num_guesses=session['num_guesses'], guesses=session['guesses'], fighter_names=json.dumps(session['fighter_names']), answer=session['answer'])
    
    if name in session['fighter_names']:
        guess = db.execute("SELECT name, hometown, debut, age, weight, height, reach, legreach FROM fighters WHERE name = ?", name)[0]
        guess['colours'] = {}
        session['guesses'].append(guess)
        session['fighter_names'].remove(name)
        session['num_guesses'] += 1
        check_features()
        if session['num_guesses'] == 7:
            show_answer('incorrect')
            flash("Better luck next time!")
            session['game_over'] = True

        return render_template("index.html", num_guesses=session['num_guesses'], guesses=session['guesses'], fighter_names=json.dumps(session['fighter_names']), answer=session['answer'])
    
    return render_template("index.html", num_guesses=session['num_guesses'], guesses=session['guesses'], fighter_names=json.dumps(session['fighter_names']), answer=session['answer'])

@app.route('/reset_game')
def reset_game():
    build_game()
    session.modified = True  # Mark session as modified to ensure changes are saved
    return render_template("index.html", num_guesses=session['num_guesses'], guesses=session['guesses'], fighter_names=json.dumps(session['fighter_names']), answer=session['answer'])

@app.route('/api/data')
def get_data():
    return jsonify({
        'game_over': session.get('game_over', False),
        'answer': session.get('answer', None),
        'fighter_names': session.get('fighter_names', [])
    })

def show_answer(result):
    if result == 'correct':
        rgb_val = "rgb(25, 135, 84)"
    else:
        rgb_val = "rgb(219, 54, 70)"

    answer = session['answer']
    answer['colours'] = {feature : rgb_val for feature in features}
    session['guesses'].append(answer)
    session['fighter_names'].remove(answer['name'])
    session['num_guesses'] += 1

def check_features():
    allowance_map = {
        'debut' : 1,
        'age' : 3,
        'weight' : 2,
        'height' : 3 
    }
    check_hometown()
    check_debut(allowance_map['debut'])
    check_age(allowance_map['age'])
    check_weight(allowance_map['weight'])
    check_height(allowance_map['height'])
    
def check_hometown():
    if session['guesses'][-1]['hometown'] == session['answer']['hometown']:
        session['guesses'][-1]['colours']['hometown'] = "rgb(25, 135, 84)"

def check_debut(allowance):
    guess_feature = int(session['guesses'][-1]['debut'].split(',')[1])
    answer_feature = int(session['answer']['debut'].split(',')[1])
    set_correct_colour(allowance, guess_feature, answer_feature, 'debut')

def check_age(allowance):
    guess_feature = int(session['guesses'][-1]['age'])
    answer_feature = int(session['answer']['age'])
    set_correct_colour(allowance, guess_feature, answer_feature, 'age')

def check_height(allowance):
    guess_feature = int(session['guesses'][-1]['height'].split('.')[0])
    answer_feature = int(session['answer']['height'].split('.')[0])
    set_correct_colour(allowance, guess_feature, answer_feature, 'height')

def check_weight(allowance):
    weightclass_map = {
        "Flyweight" : 1,
        "Bantamweight" : 2,
        "Featherweight" : 3,
        "Lightweight" : 4,
        "Welterweight" : 5,
        "Middleweight" : 6,
        "LightHeavyweight" : 7,
        "Heavyweight" : 8
    }
    guess_feature = weightclass_map[session['guesses'][-1]['weight']]
    answer_feature = weightclass_map[session['answer']['weight']]

    set_correct_colour(allowance, guess_feature, answer_feature, 'weight')

def set_correct_colour(allowance, guess, fighter_stat, column):
    # If correct guess
    if (guess == fighter_stat):
        session['guesses'][-1]['colours'][column] = "rgb(25, 135, 84)"
    # If guess within allowance
    elif (guess < fighter_stat and guess >= (fighter_stat - allowance) or guess > fighter_stat and guess <= (fighter_stat + allowance)):
        session['guesses'][-1]['colours'][column] = "rgb(255, 193, 7)"


if __name__ == '__main__':
    app.run(debug=True)