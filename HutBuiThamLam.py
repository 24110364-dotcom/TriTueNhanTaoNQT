import heapq
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
            val = state[i][j]
            if val == 'x' or val == 'x1':
                return i, j
    return None

def is_goal(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 1 or state[i][j] == 'x1':
                return False
    return True

def heuristic(state):
    """
    Hàm h(n): Đếm số ô bẩn còn lại. 
    Càng ít ô bẩn thì h(n) càng nhỏ (càng gần Goal).
    """
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == 1 or state[i][j] == 'x1':
                count += 1
    return count

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
        # Trả lại ô cũ: nếu đang là x1 (robot+bẩn) thì thành 1, nếu x thì thành 0
        new_state[r][c] = 1 if state[r][c] == 'x1' else 0
        # Di chuyển
        nr, nc = r, c
        if action == "UP":    nr -= 1
        elif action == "DOWN":  nr += 1
        elif action == "LEFT":  nc -= 1
        elif action == "RIGHT": nc += 1
        # Ghi đè robot vào ô mới
        new_state[nr][nc] = 'x1' if new_state[nr][nc] == 1 else 'x'
            
    return new_state

def greedy_search(start_state):
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)
    count = 0 
    frontier = []
    h_start = heuristic(start_state)
    
    heapq.heappush(frontier, (h_start, count, start_state, [start_state]))
    reached = set()
    while frontier:
        h_val, _, current_state, path = heapq.heappop(frontier)
        if is_goal(current_state):
            return path
        curr_tuple = state_to_tuple(current_state)
        if curr_tuple in reached:
            continue
        reached.add(curr_tuple)
        for action in get_actions(current_state):
            child = result_state(current_state, action)
            child_tuple = state_to_tuple(child)
            if child_tuple not in reached:
                h_m = heuristic(child) # Tính h(m)
                count += 1
                heapq.heappush(frontier, (h_m, count, child, path + [child]))
    return None
solution_path = greedy_search(initial_state)

if solution_path:
    print(f"SUCCESS: Đã tìm thấy đường đi với Greedy Search!")
    for i, step in enumerate(solution_path):
        print(f"Bước {i}:")
        print_state(step)
else:
    print("\nFAILURE: Không tìm thấy đường đi.")