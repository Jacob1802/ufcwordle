# UFC Wordle
#### Video Demo:  <https://www.youtube.com/watch?v=Z1tKxDoCpRY>
# Features

- **Seven Guesses:** Players have up to seven guesses to find the correct fighter.
- **Feedback System:** Provides color-coded feedback (green and yellow) to indicate how close the guess is to the target fighter's attributes.
- **Autocomplete:** An autocomplete feature helps players select fighters from a predefined list.
- **Game Reset:** Players can reset the game at any time.

# Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/ufc-wordle.git
cd ufc-wordle
pip install -r requirements.txt
flask run
```
Navigate to http://127.0.0.1:5000/ in your web browser to play the game

# Gameplay Instructions

- **Start the Game:** Open the web application and start a new game.
- **Make a Guess:** Type the name of a UFC fighter and submit your guess.
- **Feedback:** The game will provide feedback on how close your guess is to the target fighter:
  - **Green:** Indicates an exact match for an attribute.
  - **Yellow:** Indicates that the guessed attribute is within a certain range of the target attribute.
- **Win or Lose:** If you guess the correct fighter within seven attempts, you win. Otherwise, you lose and can start a new game.

# How It Works

**app.py**
- **Flask Setup:** Initializes the Flask app, sets up routes, and manages sessions.
- **Game Logic:** Handles the core game logic, including initializing the game, processing guesses, and providing feedback.
- **API:** Provides an API endpoint to fetch game data.

**helpers.py**
- **Database Connection:** Connects to the SQLite database containing fighter information.
- **Utility Functions:** Contains utility functions for converting measurements and fetching fighter data.

**scripts.js**
- **Autocomplete:** Implements the autocomplete functionality for fighter names.
- **Modal:** Manages the display of the "How to Play" modal.

**styles.css**
- **Styling:** Contains CSS styles for the application, including the layout and color schemes.

**index.html**
- **HTML Template:** The main HTML template for rendering the game interface.

# Acknowledgements

- **Wordle:** The original game that inspired this project.

Enjoy playing UFC Wordle! If you have any questions or suggestions, feel free to open an issue.