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

def find_robot(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] in ['x', 'x1']: return i, j
    return None

def is_goal(state):
    for row in state:
        if 1 in row or 'x1' in row: return False
    return True

def heuristic(state):
    
    return sum(row.count(1) + row.count('x1') for row in state)

def get_actions(state):
    r, c = find_robot(state)
    actions = []
    if state[r][c] == 'x1': actions.append("SUCK")
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
        new_state[r][c] = 1 if state[r][c] == 'x1' else 0
        nr, nc = r, c
        if action == "UP": nr -= 1
        elif action == "DOWN": nr += 1
        elif action == "LEFT": nc -= 1
        elif action == "RIGHT": nc += 1
        new_state[nr][nc] = 'x1' if new_state[nr][nc] == 1 else 'x'
    return new_state

# --- THUẬT TOÁN A* 
def a_star_search(start_state):
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)

    #  Khởi tạo tập FRONTIER = {Start} với f(Start) = g(Start) + h(Start) = 0 + h(Start)
    count = 0
    start_h = heuristic(start_state)
    # Lưu dạng: (f_value, count, current_state, g_cost, path)
    frontier = [(start_h, count, start_state, 0, [start_state])]
    
    # Khởi tạo tập REACHED = {}
    # Lưu dưới dạng {state_tuple: g_cost} để dễ kiểm tra điều kiện ii, iii
    reached = {state_to_tuple(start_state): 0}
    
    
    frontier_map = {state_to_tuple(start_state): 0}

    #TRONG KHI (FRONTIER không rỗng):
    while frontier:
        # a. Chọn trạng thái n từ FRONTIER có giá trị f(n) nhỏ nhất
        f_n, _, n, g_n, path = heapq.heappop(frontier)
        n_tuple = state_to_tuple(n)

        #  NẾU n == Goal: TRẢ VỀ "Thành công" và truy xuất lại đường đi
        if is_goal(n):
            return path, g_n

        

        #  Với mỗi trạng thái m kề với n:
        for action in get_actions(n):
            m = result_state(n, action)
            m_tuple = state_to_tuple(m)
            
            # Tính toán chi phí thực tế mới: g_new(m) = g(n) + cost(n, m)
            # Giả sử cost mỗi bước (di chuyển/hút) đều bằng 1
            g_new_m = g_n + 1
            
            #  NẾU m đã nằm trong REACHED:
            if m_tuple in reached:
                # NẾU g_new(m) >= g(m) hiện tại: Bỏ qua (tệ hơn)
                if g_new_m >= reached[m_tuple]:
                    continue
                # NGƯỢC LẠI: Xóa m khỏi REACHED và cập nhật lại (ở bước iv)
                del reached[m_tuple]

            # . NẾU m đã nằm trong FRONTIER:
            if m_tuple in frontier_map:
                # NẾU g_new(m) < g(m) hiện tại: Cập nhật lại (ở bước iv)
                if g_new_m < frontier_map[m_tuple]:
                    pass
                else:
                    continue

            #  NẾU m chưa có mặt trong FRONTIER và REACHED (hoặc đã bị xóa/cần cập nhật)
            if m_tuple not in reached:
                reached[m_tuple] = g_new_m
                frontier_map[m_tuple] = g_new_m
                h_m = heuristic(m)
                f_m = g_new_m + h_m
                count += 1
                heapq.heappush(frontier, (f_m, count, m, g_new_m, path + [m]))

    
    return None, 0


solution, total_cost = a_star_search(initial_state)

if solution:
    print(f"SUCCESS: Đã tìm thấy đường đi với A*!")
    print(f"Tổng số bước (g): {total_cost}")
    for i, step in enumerate(solution):
        print(f"Bước {i}:")
        for row in step: print(row)
        print()
else:
    print("FAILURE")