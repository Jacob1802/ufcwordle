from requests import get
from bs4 import BeautifulSoup
import cs50

def main():
    db = cs50.SQL("sqlite:///fighters.db")
    set_fighters(db, get_fighters())
    # get_fighters_names()


def get_fighters():
    request = get("https://www.ufc.com/rankings")
    soup = BeautifulSoup(request.text, "html.parser")
    filtered_fighters = []
    unfiltered_fighters = soup.find_all(class_="views-row")

    for name in unfiltered_fighters[15:len(unfiltered_fighters)]:
        if str(name.text).strip().lower() == "amanda nunes":
            return filtered_fighters

        filtered_fighters.append(name.text.strip().replace("ř", "r").replace("í", "i").replace("á", "a").replace("ć", "c").replace("ł", "l").replace("'", "").replace("ñ", "n"))
    
    return filtered_fighters


def set_stats(items, name, db):
    for i, value in enumerate(items):
        match value[0]:
            case "Hometown":
                if value[-1].strip() == "States":
                    hometown = "United States"
                elif value[-1].strip() == "Kingdom":
                    hometown = "United Kingdom"
                elif value[-1].strip() == "Zealand":
                    hometown = "New Zealand"
                else:
                    hometown = value[-1]
                db.execute("UPDATE fighters SET hometown = ? WHERE name = ?;", hometown, name)
                
            case "Trains":
                gym = " ".join(value[2:])
                db.execute("UPDATE fighters SET gym = ? WHERE name = ?;", gym, name)
                
            case "Fighting":
                style = " ".join(value[2:])
                db.execute("UPDATE fighters SET style = ? WHERE name = ?", style, name)
                
            case "Age":
                age = value[1]
                db.execute("UPDATE fighters SET age = ? WHERE name = ?", age, name)
                
            case "Height":
                height = value[1]
                db.execute("UPDATE fighters SET height = ? WHERE name = ?", height, name)
                
            # case "Weight":
            #     weight = value[1]
            #     db.execute("UPDATE fighters SET weight = ? WHERE name = ?", weight, name)
                
            case "Octagon":
                debut = " ".join(value[2:])
                db.execute("UPDATE fighters SET debut = ? WHERE name = ?", debut, name)
                
            case "Reach":
                reach = value[1]
                db.execute("UPDATE fighters SET reach = ? WHERE name = ?", reach, name)
                
            case "Leg":
                leg_reach = value[2]
                db.execute("UPDATE fighters SET legreach = ? WHERE name = ?", leg_reach, name)


def set_weight(weights, name, db):
    for weight in weights:
        if not weight:
            weight = ["Flyweight"]

        if weight[0] == "Light":
            weight = weight[0] + weight[1]
            db.execute("UPDATE fighters SET weight = ? WHERE name = ?", weight, name)
            return
            
        weight = weight[0]
        db.execute("UPDATE fighters SET weight = ? WHERE name = ?", weight, name)
        return


def set_fighters(db, fighters):
    count = 0

    for name in fighters:
        try:
            name = name.lower()
            first, last = name.split()
            if "-" in last:
                last, _ = last.split("-")

            response = get(f"https://www.ufc.com/athlete/{first}-{last}")

        except ValueError:
                if len(name.split()) > 2:
                    first, middle, last = name.split()

                    response = get(f"https://www.ufc.com/athlete/{first}-{middle}-{last}")
                else:
                    first = "Su"
                    last = "Mudaerji"

                    response = get(f"https://www.ufc.com/athlete/{first}-{last}")

        # if updating table
        # count += 1
        # db.execute("UPDATE fighters SET name = ? WHERE id = ?;", name, count)
        # if new table
        db.execute("INSERT INTO fighters(name) VALUES(?)", name)

        soup = BeautifulSoup(response.text, "html.parser")
        #fighter stats from ufc website
        result = soup.find_all(class_="c-bio__field")
        #weight from ufc website
        weights_result = soup.find_all(class_="hero-profile__division-title")
        weights = []
        for weight in weights_result:
            weights.append(weight.text.split())
        
        set_weight(weights, name, db)

        items = []
        for item in result:
            item = (item.text.split())
            items.append(item)
        
        set_stats(items, name, db)
        



def get_fighters_names():
    db = cs50.SQL("sqlite:///fighters.db")
    result = db.execute("SELECT name FROM fighters")
    fighters = []
    for name in result:
        fighters.append(name['name'])
    return fighters


if __name__ == "__main__":
    main()


# CREATE TABLE fighters (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                       name TEXT NOT NULL,
#                       hometown TEXT DEFAULT NULL, gym TEXT DEFAULT NULL,
#                       style TEXT DEFAULT NULL, age TEXT DEFAULT NULL,
#                       height TEXT DEFAULT NULL, weight TEXT DEFAULT NULL,
#                       debut TEXT DEFAULT NULL, reach TEXT DEFAULT NULL,
#                       legreach TEXT DEFAULT NULL);