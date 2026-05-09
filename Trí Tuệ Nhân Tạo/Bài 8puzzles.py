import random

# Trạng thái đích
GOAL = [1, 2, 3, 4, 5, 6, 7, 8, 0]

class SimpleReflexAgent:
    def __init__(self):
        self.rules = ["UP", "DOWN", "LEFT", "RIGHT"]

    def interpret_input(self, percept):
        return percept

    def rule_match(self, state, rules):
        empty_idx = state.index(0)
        possible_moves = []
        
        if empty_idx >= 3: possible_moves.append("UP")
        if empty_idx <= 5: possible_moves.append("DOWN")
        if empty_idx % 3 != 0: possible_moves.append("LEFT")
        if empty_idx % 3 != 2: possible_moves.append("RIGHT")
        
        if state == GOAL:
            return None
            
        return random.choice(possible_moves)

    def act(self, percept):
        state = self.interpret_input(percept)
        action = self.rule_match(state, self.rules)
        return action

def move(state, action):
    new_state = state[:]
    idx = new_state.index(0)
    if action == "UP":
        new_state[idx], new_state[idx-3] = new_state[idx-3], new_state[idx]
    elif action == "DOWN":
        new_state[idx], new_state[idx+3] = new_state[idx+3], new_state[idx]
    elif action == "LEFT":
        new_state[idx], new_state[idx-1] = new_state[idx-1], new_state[idx]
    elif action == "RIGHT":
        new_state[idx], new_state[idx+1] = new_state[idx+1], new_state[idx]
    return new_state

def display(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print("-" * 10)

# Chạy thử
board = [1, 2, 3, 4, 0, 5, 7, 8, 6]
agent = SimpleReflexAgent()

display(board)
for i in range(5):
    step = agent.act(board)
    if not step: break
    board = move(board, step)
    print(f"Step {i+1}: {step}")
    display(board) 