from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import pickle
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For session handling

# Load the trained Q-table
with open("q_table.pkl", "rb") as f:
    q_table = pickle.load(f)

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_winner = None
        self.winning_combo = []

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, square, letter):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for combo in win_combinations:
            if all(self.board[i] == letter for i in combo):
                self.winning_combo = combo
                return True
        return False

    def is_full(self):
        return ' ' not in self.board

    def reset(self):
        self.board = [' '] * 9
        self.current_winner = None
        self.winning_combo = []

    def get_state(self):
        return ''.join(self.board)

def ai_move(board, available_moves):
    state = ''.join(board)
    qs = q_table.get(state, [0] * 9)
    q_values = [qs[i] if i in available_moves else -float('inf') for i in range(9)]
    max_q = max(q_values)
    best_actions = [i for i, q in enumerate(q_values) if q == max_q]
    return random.choice(best_actions)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose_side', methods=['POST'])
def choose_side():
    selected_side = request.form.get('side')
    session['side'] = selected_side
    return redirect(url_for('game_board'))

@app.route('/game')
def game_board():
    if 'side' not in session:
        return redirect(url_for('index'))
    player_side = session['side']
    return render_template('game.html', player_side=player_side)

@app.route('/move/<int:square>', methods=['POST'])
def player_move(square):
    game = TicTacToe()
    game.board = request.json['board']
    player_letter = request.json['player']
    ai_letter = 'O' if player_letter == 'X' else 'X'

    # Player move
    game.make_move(square, player_letter)

    # Check after player's move
    if game.current_winner or game.is_full():
        return jsonify({
            'board': game.board,
            'winner': game.current_winner,
            'winning_combo': game.winning_combo
        })

    # AI move
    ai_square = ai_move(game.board, game.available_moves())
    game.make_move(ai_square, ai_letter)

    return jsonify({
        'board': game.board,
        'winner': game.current_winner,
        'winning_combo': game.winning_combo
    })

@app.route('/reset', methods=['POST'])
def reset_game():
    game = TicTacToe()
    game.reset()
    return jsonify({'board': game.board})

if __name__ == "__main__":
    app.run(debug=True)
