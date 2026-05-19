from copy import deepcopy
from collections import deque
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
    print("-" * 10)

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

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def move(state, direction):
    x, y = find_robot(state)
    nx, ny = x, y
    if direction == "UP": nx -= 1
    elif direction == "DOWN": nx += 1
    elif direction == "LEFT": ny -= 1
    elif direction == "RIGHT": ny += 1
    if 0 <= nx < 3 and 0 <= ny < 3:
        new_state = [row[:] for row in state]
        new_state[x][y] = 0 
        new_state[nx][ny] = 'x'
        return new_state
    return None

def suck(state):
    x, y = find_robot(state)
    new_state = [row[:] for row in state]
    return new_state

def bfs_approach_2(initial):
    node = initial
    path = []
    
    if is_goal(node):
        return path
    
    frontier = deque([(node, path)])
    reached = {state_to_tuple(node)}
    
    print(f"Bắt đầu duyệt... Trạng thái gốc S:")
    print_state(node)

    step = 0
    while frontier:
        current_state, current_path = frontier.popleft()
        step += 1
        actions = ["SUCK", "UP", "DOWN", "LEFT", "RIGHT"]
        for action in actions:
            child_state = None
            if action == "SUCK":
                child_state = deepcopy(current_state)
            
            else:
                child_state = move(current_state, action)
            
            if child_state:
                s_tuple = state_to_tuple(child_state)
                if is_goal(child_state):
                    print(f"Thành công tại bước {step}! Hành động cuối: {action}")
                    return current_path + [action]
                if s_tuple not in reached:
                    reached.add(s_tuple)
                    frontier.append((child_state, current_path + [action]))
                    
    return "Không tìm thấy đường đi"

result = bfs_approach_2(initial_state)
print("=> KẾT QUẢ ĐƯỜNG ĐI:", result)
