import cs50
import random

def connect_db():
    db = cs50.SQL("sqlite:///fighters.db")
    return db


def get_fighters_names():
    db = connect_db()

    fighters = []

    for row in db.execute("SELECT * FROM fighters"):
        fighters.append(row['name'])

    return fighters


def inch_to_ft(value):
    value = f"{float(value) / 12:.1f}"
    foot, inch = value.split(".")
    return foot + "'" + inch + '"'


def pick_random_fighter():
    fighter_names = get_fighters_names()
    random_fighter = fighter_names[random.randint(0, len(fighter_names) - 1)].title()
    
    db = connect_db()
    answer = db.execute("SELECT * FROM fighters WHERE name = ?", random_fighter.lower())[0]
    return answer