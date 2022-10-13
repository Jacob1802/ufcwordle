import cs50

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
