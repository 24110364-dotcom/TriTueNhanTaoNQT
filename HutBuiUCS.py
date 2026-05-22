import heapq
from copy import deepcopy

# Trạng thái ban đầu
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
        # Trả lại ô cũ
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



def ucs(state):
    costs = {"SUCK": 2, "UP": 1, "DOWN": 1, "LEFT": 1, "RIGHT": 1}
    
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)

    # Thêm một biến đếm (counter) để tránh so sánh ma trận
    count = 0 

    r_start, c_start = 0, 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == 'x': r_start, c_start = i, j
    
    start_node = deepcopy(state)
    if initial_state[r_start][c_start] == 1:
        start_node[r_start][c_start] = 'x1'

    frontier = []
    # Thêm count vào đây: (cost, count, state, path)
    heapq.heappush(frontier, (0, count, start_node, [start_node]))
    
    explored = set()

    while frontier:
        # Pop cũng phải lấy ra đủ 4 tham số
        current_cost, _, current_state, path = heapq.heappop(frontier)

        if is_goal(current_state):
            return path, current_cost

        state_tuple = state_to_tuple(current_state)
        if state_tuple in explored:
            continue
        explored.add(state_tuple)

        for action in get_actions(current_state):
            child = result_state(current_state, action)
            if state_to_tuple(child) not in explored:
                new_cost = current_cost + costs[action]
                count += 1 # Mỗi lần push thì tăng count lên
                heapq.heappush(frontier, (new_cost, count, child, path + [child]))

    return None, 0


solution_path, total_cost = ucs(initial_state)

if solution_path:
    print(f"SUCCESS: Đã tìm thấy đường đi với UCS!")
    print(f"Tổng chi phí (Total Cost): {total_cost}")
    for i, step in enumerate(solution_path):
        print(f"Bước {i}:")
        print_state(step)
else:
    print("\nFAILURE: Không tìm thấy đường đi.")