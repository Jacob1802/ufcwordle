from requests import get
from bs4 import BeautifulSoup
from helpers import connect_db

def main():
    db = connect_db()
    set_fighters(db, get_fighters())


def get_fighters():
    """ Fetch fighter data from url """
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
    """ Sets fighter stats in a sqlite db"""
    for value in items:
        match value[0]:
            case "Hometown":
                match value[-1].strip():
                    case "States":
                        hometown = "United States"
                    case "Kingdom":
                        hometown = "United Kingdom"
                    case "Zealand":
                        hometown = "New Zealand"
                    case _:
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
    """ Set weights for fighters in sqlite db"""
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
    """ Set names for fighters in sqlite db"""
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
        count += 1
        db.execute("UPDATE fighters SET name = ? WHERE id = ?;", name, count)
        # if new table
        # db.execute("INSERT INTO fighters(name) VALUES(?)", name)

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


if __name__ == "__main__":
    main()