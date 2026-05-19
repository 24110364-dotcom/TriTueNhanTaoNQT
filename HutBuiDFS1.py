from copy import deepcopy
initial_state = [
    ['x', 0, 0],
    [1,   1, 0],
    [0,   0, 0]
]
goal_state = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
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
    for row in state:
        if 1 in row:
            return False
    return True

def move(state, direction):
    x, y = find_robot(state)
    nx, ny = x, y
    if direction == "UP" : nx = x - 1
    elif direction == "DOWN": nx = x + 1
    elif direction == "LEFT": ny = y - 1
    elif direction == "RIGHT": ny = y + 1

    if nx < 0 or nx >= 3 or ny < 0 or ny >= 3 :
        return None
    new_state = deepcopy(state)
    new_state[x][y] = 0
    new_state[nx][ny] = 'x'
    return new_state

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def dfs(initial):
    stack = [(initial, [])]
    visited = set()
    step = 0
    while stack:
        current_state, path = stack.pop()
        state_key = state_to_tuple(current_state)
        if state_key in visited:
            continue
        visited.add(state_key)
        print(f"---Bước {step}---")
        print_state(current_state)
        step += 1
        
        if is_goal(current_state):
            print("Đã tìm thất Goal")
            return path
        
        actions = ["RIGHT", "DOWN", "LEFT", "UP"]

        for action in reversed(actions):
            new_state = move(current_state, action)
            if new_state is not None:
                if state_to_tuple(new_state) not in visited:
                    stack.append((new_state, path + [action]))

    return None
print("Bắt đầu chạy")
answer = dfs(initial_state)
print("Đường đi chi tiết:")
print(answer)