import random
import pickle

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_winner = None

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row = square // 3
        col = square % 3
        row_win = all([self.board[row * 3 + i] == letter for i in range(3)])
        col_win = all([self.board[i * 3 + col] == letter for i in range(3)])
        diag1_win = all([self.board[i] == letter for i in [0, 4, 8]])
        diag2_win = all([self.board[i] == letter for i in [2, 4, 6]])
        return row_win or col_win or (square in [0, 2, 4, 6, 8] and (diag1_win or diag2_win))

    def is_full(self):
        return ' ' not in self.board

    def reset(self):
        self.board = [' '] * 9
        self.current_winner = None

    def get_state(self):
        return ''.join(self.board)

class QLearningAgent:
    def __init__(self, alpha=0.3, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_qs(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0] * 9
        return self.q_table[state]

    def choose_action(self, state, available_moves):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(available_moves)
        qs = self.get_qs(state)
        q_values = [qs[i] if i in available_moves else -float('inf') for i in range(9)]
        max_q = max(q_values)
        best_actions = [i for i, q in enumerate(q_values) if q == max_q]
        return random.choice(best_actions)

    def update(self, state, action, reward, next_state, done):
        current_q = self.get_qs(state)[action]
        max_future_q = max(self.get_qs(next_state)) if not done else 0
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[state][action] = new_q

def train(agent, episodes=50000):
    env = TicTacToe()
    for _ in range(episodes):
        env.reset()
        state = env.get_state()
        while True:
            available = env.available_moves()
            action = agent.choose_action(state, available)
            env.make_move(action, 'X')
            next_state = env.get_state()
            if env.current_winner == 'X':
                agent.update(state, action, 1, next_state, True)
                break
            elif env.is_full():
                agent.update(state, action, 0.5, next_state, True)
                break
            opponent_move = random.choice(env.available_moves())
            env.make_move(opponent_move, 'O')
            next_state2 = env.get_state()
            if env.current_winner == 'O':
                agent.update(state, action, -1, next_state2, True)
                break
            elif env.is_full():
                agent.update(state, action, 0.5, next_state2, True)
                break
            agent.update(state, action, 0, next_state2, False)
            state = next_state2

if __name__ == "__main__":
    agent = QLearningAgent()
    print("Training AI agent... Please wait.")
    train(agent)
    print("Training complete. Saving Q-table...")
    with open("q_table.pkl", "wb") as f:
        pickle.dump(agent.q_table, f)
    print("Q-table saved as q_table.pkl.")
