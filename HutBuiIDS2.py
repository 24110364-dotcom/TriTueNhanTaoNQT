from copy import deepcopy

# Trạng thái ban đầu: 'x' là robot, 1 là bụi, 0 là sạch
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
            if state[i][j] == 'x' or (isinstance(state[i][j], str) and 'x' in state[i][j]):
                return i, j
    return None

def is_goal(state):
   
    for i in range(3):
        for j in range(3):
            if state[i][j] == 1 or state[i][j] == 'x1':
                return False
    return True

def get_actions(state):
    r, c = find_robot(state)
    actions = []
    
    
    if state[r][c] == 'x1':
        actions.append("SUCK")
    
   
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
        #  Trả lại trạng thái ô cũ khi robot rời đi
        if state[r][c] == 'x1':
            new_state[r][c] = 1  
        else:
            new_state[r][c] = 0  
            
        # Xác định vị trí mới
        new_r, new_c = r, c
        if action == "UP":    new_r -= 1
        elif action == "DOWN":  new_r += 1
        elif action == "LEFT":  new_c -= 1
        elif action == "RIGHT": new_c += 1
        
        # Đặt robot vào ô mới
        if new_state[new_r][new_c] == 1:
            new_state[new_r][new_c] = 'x1' # Robot đè lên bụi
        else:
            new_state[new_r][new_c] = 'x'  # Robot đè lên ô trống
            
    return new_state



def recursive_dls(state, limit):
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
            
    return "cutoff" if cutoff_occurred else None

def ids(state):
    depth = 0
    
    start_node = deepcopy(state)
    r, c = 0, 0 
    for i in range(3):
        for j in range(3):
            if start_node[i][j] == 'x': r, c = i, j
    if start_node[r][c] == 'x' and initial_state[r][c] == 1: 
        start_node[r][c] = 'x1'

    while True:
        print(f"Đang tìm ở độ sâu (limit): {depth}")
        result = recursive_dls(start_node, depth)
        if result != "cutoff":
            return result
        depth += 1
        if depth > 20: 
            return None

# Chạy chương trình
solution = ids(initial_state)

if solution:
    print("\nSUCCESS: Đã tìm thấy đường đi!")
    for i, step in enumerate(solution):
        print(f"Bước {i}:")
        print_state(step)
else:
    print("\nFAILURE: Không tìm thấy đường đi.")