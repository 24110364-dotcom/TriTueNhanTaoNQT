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
    
    for row in state:
        if 1 in row:
            return False
    return True

def move(state, direction):
    x, y = find_robot(state)
    nx, ny = x, y
    if direction == "UP": nx -= 1
    elif direction == "DOWN": nx += 1
    elif direction == "LEFT": ny -= 1
    elif direction == "RIGHT": ny += 1
    
    if 0 <= nx < 3 and 0 <= ny < 3:
        new_state = deepcopy(state)
        new_state[x][y] = state[x][y] if state[x][y] != 'x' else 0 
        new_state[nx][ny] = 'x'
        return new_state
    return None

def suck(state):
    x, y = find_robot(state)
   
    if state[x][y] == 'x' and any(1 in row for row in state):
        new_state = deepcopy(state)
        return new_state 
    return None

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def bfs_approach_1(initial):
    if is_goal(initial):
        return []

    
    queue = [(initial, [])] 
    visited = {state_to_tuple(initial)}
    
    step = 0
    while queue:
        current_state, path = queue.pop(0) 
        step += 1
        
       
        actions = ["SUCK", "UP", "DOWN", "LEFT", "RIGHT"]

        for action in actions:
            new_state = None
            if action == "SUCK":
                x, y = find_robot(current_state)
                continue 
            else:
                new_state = move(current_state, action)

            if new_state is not None:
                state_key = state_to_tuple(new_state)

                if state_key not in visited:
                    if is_goal(new_state):
                        print(f"Tìm thấy đích tại bước {step}!")
                        print_state(new_state)
                        return path + [action]
                    
                    visited.add(state_key)
                    queue.append((new_state, path + [action]))
                    
    return None


print("Đang chạy BFS Tiếp cận 1...")
result = bfs_approach_1(initial_state)
print("ĐƯỜNG ĐI:", result)