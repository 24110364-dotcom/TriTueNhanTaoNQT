from copy import deepcopy

# Khởi tạo trạng thái ban đầu
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
    
    print("LỖI: Không tìm thấy robot trong state:")
    print_state(state)
    return None

def is_goal(state):
    for row in state:
        if 1 in row:
            return False
    return True



def get_actions(state):
    
    r, c = find_robot(state)
    actions = ["SUCK"] # Luôn có thể thử hút
    if r > 0: actions.append("UP")
    if r < 2: actions.append("DOWN")
    if c > 0: actions.append("LEFT")
    if c < 2: actions.append("RIGHT")
    return actions

def result_state(state, action):
    new_state = deepcopy(state)
    r, c = find_robot(state) 
    
    if action == "SUCK":
        
        new_state[r][c] = 'x' 
    else:
        
        new_state[r][c] = 0
        
        
        new_r, new_c = r, c
        if action == "UP":    new_r -= 1
        elif action == "DOWN":  new_r += 1
        elif action == "LEFT":  new_c -= 1
        elif action == "RIGHT": new_c += 1
        
        
        new_state[new_r][new_c] = 'x'
        
    return new_state



def recursive_dls(state, limit):
    # 1. Kiểm tra đích (Goal-test)
    if is_goal(state):
        return [state]
    
    
    if limit <= 0:
        return "cutoff"
    
    cutoff_occurred = False
    
    
    for action in get_actions(state):
        child = result_state(state, action)
        
        
        result = recursive_dls(child, limit - 1)
        
        if result == "cutoff":
            cutoff_occurred = True
        elif result is not None:
            
            return [state] + result
            
    
    if cutoff_occurred:
        return "cutoff"
    else:
        return None

def ids(state):
    depth = 0
    while True:
        print(f"Đang tìm ở độ sâu (limit): {depth}")
        result = recursive_dls(state, depth)
        
        if result != "cutoff":
            return result
        
        depth += 1
        
        if depth > 10: 
            return None


solution = ids(initial_state)

if solution:
    print("\nSUCCESS: Đã tìm thấy đường đi!")
    for i, step in enumerate(solution):
        print(f"Bước {i}:")
        print_state(step)
else:
    print("\nFAILURE: Không tìm thấy đường đi.")