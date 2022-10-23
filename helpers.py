import random
import cs50

def connect_db():
    """ Connect to sqlite db """
    db = cs50.SQL("sqlite:///fighters.db")
    return db


def get_fighters_names():
    """ Return a list of fighter names """
    db = connect_db()

    fighters = []

    for row in db.execute("SELECT * FROM fighters"):
        fighters.append(row['name'])

    return fighters


def inch_to_ft(value):
    """ Convert inches to feet """
    value = f"{float(value) / 12:.1f}"
    foot, inch = value.split(".")
    return foot + "'" + inch + '"'


def pick_random_fighter():
    """ Choose a random fighter from list """
    fighter_names = get_fighters_names()
    random_fighter = fighter_names[random.randint(0, len(fighter_names) - 1)].title()
    
    db = connect_db()
    answer = db.execute("SELECT * FROM fighters WHERE name = ?", random_fighter.lower())[0]
    return answer