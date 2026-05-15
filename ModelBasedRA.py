goal = [
    [1,2,3],
    [4,5,6],
    [7,8,0]
]

def input_board():
    board = []
    print("Nhập 8 puzzles")
    for i in range(3):
        row = list(map(int,input().split()))
        board.append(row)
    return board

def print_board(board):
    for row in board :
        print(row)
    print()

def find_blank(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i,j

def copy_board(board):
    return [row[:] for row in board]

def move(board, direction):
    x, y = find_blank(board)
    new = copy_board(board)

    if direction == "UP" and x > 0 :
        new[x][y], new[x-1][y] = new[x-1][y], new[x][y]
        return new 
    if direction == "DOWN" and x < 2 :
        new[x][y], new[x+1][y] = new[x+1][y], new[x][y]
        return new
    if direction == "LEFT" and y > 0 :
        new[x][y], new[x][y-1] = new[x][y-1], new[x][y]
        return new
    if direction == "RIGHT" and y < 2 :
        new[x][y], new[x][y+1] = new[x][y+1], new[x][y]
        return new
    return None

def heuristic(board):
    wrong = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != goal[i][j]:
                wrong += 1
    return wrong

def opposite(a):
    if a == "UP":
        return "DOWN"
    if a == "DOWN":
        return "UP"
    if a == "LEFT":
        return "RIGHT"
    if a == "RIGHT":
        return "LEFT"
    return None

def rule_match(state, last_action):
    actions = ["UP", "DOWN", "LEFT", "RIGHT"]

    best = None
    best_score = 999

    for a in actions:

        if a == opposite(last_action):
            continue

        new_state = move(state, a)

        if new_state is not None:
            score = heuristic(new_state)

            
            if score < best_score:
                best_score = score
                best = a

    return best

def solve(start):
    state = start
    action = None
    step = 0
    visited = []

    print("Initial:")
    print_board(state)

    while state != goal and step < 30:

        visited.append(str(state))

        action = rule_match(state, action)

        if action is None:
            print("Khong tim duoc")
            return

        new_state = move(state, action)

        if str(new_state) in visited:
            print("Bi lap")
            return

        state = new_state
        step += 1

        print("Step", step, ":", action)
        print_board(state)

    if state == goal:
        print("Solved!")
    else :
        print("Dung vi qua buoc")
    
initial = input_board()
solve(initial)