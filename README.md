# UFC Wordle
#### Video Demo:  <https://youtu.be/0NrDy9jxLAI>
#### Description: Jacob Dilonardo, FROM: Sydney, NSW, Australia, Date of submission: 1/11/2022. My project is a UFC version of Wordle using Python, Javascript, Html, Css & Sqlite.
This project was inspired from the game of wordle found at https://www.nytimes.com/games/wordle/index.html and a common interest I have which is the watching the ufc as I have been for many years.
###### Python files
helpers.py is made up of four functions connect_db which returns a connection to the fighters database, get_fighter_names gets a list of all the fighters names from the database, inch_to_ft will convert inchs to feet and is use in html witch jinja templating and pick_random_fighter to return a randomly selected fighter from the database. These functions help to tidy up the code for the backend of the app in app.py.
fighters.py is also made up of four functions, get_fighters which fetches the ufc fighters data from the https://www.ufc.com/rankings and stores it in a list, set_fighter_names which takes the list and stores the names and primary key in a sqlite database, set_stats fetches the stats from https://www.ufc.com/athlete/first-last, parses and organises the data to then store it in a database along with set_weights.
app.py is a flask app that will control the backend in combination with a sqlite database to query and send the data to the web app at index.html.
app.py also uses some functions from helpers.py and the flask module. the flask modules app.py incorperates are the flash function to display to the user whether they've won or lost at the end of the game along with render_templete to feed the web app the index.html file and the request function the determine wether the submitted request was GET or POST.
###### Javascript files
static/scripts.js is made up of functions such as autocomplete for the inputs, tracking the amount of guesses and showing the correct answer when max guesses is reached showing the matches from the inputs.
###### CSS files
static/styles.css is made up of many to styles and designs to add to the webpage with the help of bootstrap.
###### HTML files
templates/index.html displays the layout and structure of the page, taking inputs from the flask backend and using jinja templating displaying those inputs onto the webapp. Also including a modal to display the rules of the game. index.html also uses the popular css library bootstrap the help format the display of the page.
