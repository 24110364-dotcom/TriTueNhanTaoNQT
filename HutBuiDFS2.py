from copy import deepcopy

initial_state = [
    ['x', 0, 0],
    [1,   1, 0],
    [0,   0, 0]
]
goal_state = [
    [0,0,0],
    [0,0,0],
    [0,0,0]
]

def print_state(state):
    for row in state:
        print(row)
    print()

def find_robot(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 'x':
                return i, j
def is_goal(state):
    temp = []
    for row in state:
        new_row = []
        for cell in row:
            if cell == 'x':
                new_row.append(0)
            else:
                new_row.append(cell)
        temp.append(new_row)
    return temp == goal_state

def move(state, direction):
    x, y = find_robot(state)
    new_state = deepcopy(state)
    new_state[x][y] = 0
    if direction == "UP":
        nx, ny = x - 1, y
    elif direction == "DOWN":
        nx, ny = x + 1, y
    elif direction == "LEFT":
        nx, ny = x, y - 1

    elif direction == "RIGHT":
        nx, ny = x, y + 1
    else:
        return None
    if nx < 0 or nx >= 3 or ny < 0 or ny >= 3:
        return None

    new_state[nx][ny] = 'x'
    return new_state 

def suck(state):
    x, y = find_robot(state)
    if state[x][y] == 1:
        new_state = deepcopy(state)
        new_state[x][y] = 'x' 
        return new_state
    return None

def state_to_tuple(state):
    result = []
    for row in state :
        temp = []
        for cell in row:
            temp.append(str(cell))
        result.append(tuple(temp))
    return tuple(result)
def dfs(initial):
    stack = [(initial, [])]  
    visited = set()
    while stack:
        current_state, path = stack.pop()
        print("State hiện tại:")
        print_state(current_state)

        print("Path:", path)
        if is_goal(current_state):
            print("ĐÃ TỚI GOAL!")
            return path
        visited.add(state_to_tuple(current_state))
        x, y = find_robot(current_state)
        original = deepcopy(current_state)
        actions = ["SUCK", "RIGHT", "DOWN", "LEFT", "UP"]

        for action in reversed(actions):

            new_state = move(current_state, action)

            if new_state is not None:
                state_key = state_to_tuple(new_state)

                if state_key not in visited:

                    stack.append((new_state, path + [action]))

    return None
answer = dfs(initial_state)
print("ĐƯỜNG ĐI DFS:")
print(answer)
