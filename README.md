# Tic Tac Toe with Q-Learning AI

This project implements a classic Tic Tac Toe game with an AI opponent trained using the Q-learning reinforcement learning algorithm. The game features a web interface built with Flask, allowing users to play against the AI in their browser.

## Project Structure

The project directory is structured as follows:

```bash
Tictactoe/
├── static/
│   ├── game.css        # Styles for the game board
│   └── index.css       # Styles for the intro selection page
├── templates/
│   ├── game.html       # HTML template for the game board
│   └── index.html      # HTML template for intro selection page
├── app.py            # Flask web application logic
├── q_table.pkl       # Trained Q-table for the AI
└── train_model.py    # Script to train the Q-learning AI
```
## How to Run the Game

1.  **Ensure Python is installed:** This project requires Python 3.
2.  **Install dependencies:** Navigate to the project directory in your terminal and run:
    ```bash
    pip install Flask
    ```
3.  **Train the AI (if `q_table.pkl` is not present or you want to retrain):**
    ```bash
    python train_model.py
    ```
    This script will train the Q-learning agent over a number of episodes and save the resulting Q-table in `q_table.pkl`. This process might take a few moments.
4.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    This will start the Flask development server. You should see output indicating the server is running (usually on `http://127.0.0.1:5000/`).
5.  **Open in your browser:** Open your web browser and navigate to the address provided by the Flask development server (e.g., `http://127.0.0.1:5000/`).

## How to Play

1.  **Choose your side:** On the initial page, you will be prompted to choose whether you want to play as 'X' or 'O'.
2.  **Play the game:** Once you've chosen your side, the game board will appear. Click on an empty square to make your move.
3.  **The AI's turn:** After your move, the AI will make its move.
4.  **Game end:** The game ends when one player gets three in a row (horizontally, vertically, or diagonally) or when all squares are filled (a draw).
5.  **Reset:** You can click the "Reset" button to start a new game.
6.  **Home:** Click the "Home" icon to go back to the side selection page.
7.  **Info:** Click the "Info" icon to learn more about Tic Tac Toe on Wikipedia.

## AI Logic

The AI opponent in this game is powered by a Q-learning agent.

* **Q-learning:** This is a model-free reinforcement learning algorithm that learns a policy telling an agent what action to take under what circumstances. It learns a Q-value for each state-action pair, representing the expected reward of taking a particular action in a given state.
* **State Representation:** The state of the Tic Tac Toe board is represented as a string of 9 characters, where each character corresponds to a square (' ', 'X', or 'O').
* **Actions:** The available actions are the empty squares on the board (represented by their index from 0 to 8).
* **Training:** The `train_model.py` script trains the agent by having it play many games against a random opponent. During training, the agent updates its Q-values based on the rewards it receives (win, lose, draw, or continuing the game).
* **Exploration vs. Exploitation:** During training, the agent uses an epsilon-greedy strategy to balance exploration (trying new actions) and exploitation (choosing the actions with the highest learned Q-values).
* **Inference (Gameplay):** When you play against the AI, the `app.py` uses the pre-trained `q_table.pkl` to determine the AI's best move for the current board state by selecting the action with the highest Q-value.

## Further Development

Potential future enhancements could include:

* Implementing different AI difficulty levels (e.g., by adjusting the epsilon value or the training duration).
* Visual improvements to the user interface (styling in `static/`).
* Allowing two human players to play against each other.
* Exploring other reinforcement learning algorithms.

## Author

Jakir Hussain

