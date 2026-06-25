import customtkinter as ctk
import random
import heapq
import math 
from copy import deepcopy
from collections import deque
# Cấu hình giao diện chung
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

def find_robot(state):
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val == 'x' or val == 'x1':
                return i, j
    return None

def is_goal(state):
    for row in state:
        for cell in row:
            cell_str = str(cell)           
            if '1' in cell_str: 
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
        
        new_state[r][c] = '1' if state[r][c] == 'x1' else '0'
        
        # Di chuyển
        nr, nc = r, c
        if action == "UP":    nr -= 1
        elif action == "DOWN":  nr += 1
        elif action == "LEFT":  nc -= 1
        elif action == "RIGHT": nc += 1
        
        # GHI ĐÈ ROBOT VÀO Ô MỚI 
        is_dust = str(new_state[nr][nc]) == '1' or new_state[nr][nc] == 1
        new_state[nr][nc] = 'x1' if is_dust else 'x'
            
    return new_state
# Thuật toán +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Thuật toán leo đồi ngẫu nhiên 
def stochastic_hill_climbing(start_state):
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)
        
    def get_value(state):
        return -heuristic(state)

    # 1. Current_State = Start
    current_state = start_state
    path = [current_state]
    reached = {state_to_tuple(current_state)} # Chặn vòng lặp vô hạn

    # 2. TRONG KHI (đúng):
    while True:
        # Nếu Current_State == Goal: TRẢ VỀ Current_State
        if is_goal(current_state):
            return path

        # Sinh tất cả các trạng thái lân cận của Current_State
        actions = get_actions(current_state)
        current_value = get_value(current_state)
        
        # Lọc ra tập Better_Neighbors = {Neighbor | Value(Neighbor) > Value(Current_State)}
        better_neighbors = []
        for action in actions:
            child = result_state(current_state, action)
            child_tuple = state_to_tuple(child)
            
            if child_tuple not in reached and get_value(child) > current_value:
                better_neighbors.append(child)
                
        # NẾU Better_Neighbors RỖNG:
        if not better_neighbors:
            # TRẢ VỀ Current_State (Dừng vì đã đạt cực đại cục bộ)
            return path
            
        # NGƯỢC LẠI:
        else:
            # Next_State = Chọn ngẫu nhiên một trạng thái từ tập Better_Neighbors
            next_state = random.choice(better_neighbors)
            
            # Current_State = Next_State (Quay lại đầu vòng lặp với trạng thái mới)
            current_state = next_state
            path.append(current_state)
            reached.add(state_to_tuple(current_state))
# Thuật toán leo đồi độc nhất 
def steepest_ascent_hill_climbing(start_state):
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)
        
    def get_value(state):        
        return -heuristic(state)

    # 1. Current_State = Start
    current_state = start_state
    path = [current_state]
    reached = {state_to_tuple(current_state)} # Tránh vòng lặp vô tận

    # 2. TRONG KHI (đúng):
    while True:
        # Nếu Current_State == Goal: TRẢ VỀ Current_State
        if is_goal(current_state):
            return path

       
        actions = get_actions(current_state)
        neighbors = []
        
        for action in actions:
            child = result_state(current_state, action)
            child_tuple = state_to_tuple(child)
            if child_tuple not in reached:
                neighbors.append(child)
                
        # Nếu không còn trạng thái lân cận nào chưa đi qua, dừng lại
        if not neighbors:
            return path
            
        # Chọn ra trạng thái lân cận tốt nhất là Best_Neighbor
        # Ta dùng hàm max() dựa trên giá trị get_value của từng neighbor
        best_neighbor = max(neighbors, key=get_value)
        
        # NẾU Value(Best_Neighbor) > Value(Current_State):
        if get_value(best_neighbor) > get_value(current_state):
            current_state = best_neighbor
            path.append(current_state)
            reached.add(state_to_tuple(current_state))
            # (Quay lại đầu vòng lặp với trạng thái mới nhờ vòng lặp while True)
        else:
            # NGƯỢC LẠI: TRẢ VỀ Current_State (Dừng vì đã đạt cực đại cục bộ)
            return path
# Thuật toán leo đồi đơn giản
def simple_hill_climbing(start_state):
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)
        
    def get_value(state):
        
        return -heuristic(state)

    # 1. Current_State = Start
    current_state = start_state
    path = [current_state]
    reached = {state_to_tuple(current_state)} # Chặn vòng lặp vô hạn

    # 2. TRONG KHI (đúng):
    while True:
        # Nếu Current_State == Goal: TRẢ VỀ Current_State
        if is_goal(current_state):
            return path

        # Sinh các trạng thái lân cận của Current_State
        actions = get_actions(current_state)
        found_better = False
        
        current_value = get_value(current_state)

        for action in actions:
            child = result_state(current_state, action)
            child_tuple = state_to_tuple(child)
            
            if child_tuple in reached:
                continue
                
            
            if get_value(child) > current_value:
                current_state = child
                path.append(current_state)
                reached.add(child_tuple)
                found_better = True
                
                
                break 
        
        # Nếu ĐÃ DUYỆT HẾT lân cận mà không có ai tốt hơn:
        if not found_better:
            return path
# Thuật toán IDA*
def ida_star(start_state):
    def search(path, g, threshold):
        
        current = path[-1]
        h = heuristic(current) 
        f = g + h
        
        # Nếu chi phí vượt ngưỡng, cắt nhánh và trả về f để cập nhật threshold mới
        if f > threshold:
            return f, None
        if is_goal(current):
            return True, path
        
        minimum = float('inf')
        for action in get_actions(current):
            child = result_state(current, action)
            if child not in path: # Tránh vòng lặp trên cùng một nhánh
                path.append(child)
                
                # Chi phí g của trạng thái con = chi phí cha (g) + 1 bước di chuyển
                res, val = search(path, g + 1, threshold)
                
                if res is True:
                    return True, val
                if res < minimum:
                    minimum = res
                path.pop() # Backtrack
        return minimum, None

    # Khởi tạo threshold ban đầu bằng f(start) = g(start) + h(start) = 0 + h(start)
    threshold = heuristic(start_state)
    path = [start_state]
    
    while True:
        # Ban đầu tại start_state thì g = 0
        res, val = search(path, 0, threshold)
        if res is True:
            return val # Trả về danh sách các ma trận trạng thái
        if res == float('inf'):
            return None # Không tìm thấy đường đi
        threshold = res # Tăng ngưỡng threshold lên mức tối thiểu tiếp theo
# Thuật toán tham lam 
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
# Thuật toán DFS2
def dfs2(initial_state2):
    # Stack chứa tuple: (trạng_thái_hiện_tại, danh_sách_trạng_thái_đã_đi_qua)
    stack = [(initial_state2, [initial_state2])]
    # Tập hợp các trạng thái đã duyệt để tránh robot đi vòng quanh vô tận
    explored = {initial_state2}
    
    while stack:
        current_state2, path = stack.pop()
        
        # Kiểm tra đích
        if is_goal2(current_state2):
            return path
            
        # Duyệt các hành động kế tiếp
        for action in get_actions2(current_state2):
            child = result_state2(current_state2, action)
            
            if child not in explored:
                explored.add(child)
                # Đẩy trạng thái mới và đường đi vào Stack
                stack.append((child, path + [child]))
                
    return None
# Thuật toán BFS2
def bfs2(initial_state2):
    # Hàng đợi chứa tuple: (trạng_thái_hiện_tại, danh_sách_trạng_thái_đã_đi_qua)
    queue = deque([(initial_state2, [initial_state2])])
    # Tập hợp các trạng thái đã duyệt để tránh lặp vô tận
    explored = {initial_state2}
    
    while queue:
        current_state2, path = queue.popleft()
        
        # Kiểm tra đích
        if is_goal2(current_state2):
            return path
            
        # Duyệt các hành động kế tiếp
        for action in get_actions2(current_state2):
            child = result_state2(current_state2, action)
            
            if child not in explored:
                explored.add(child)
                # Lưu lại đường đi mới dẫn đến trạng thái child
                queue.append((child, path + [child]))
                
    return None # Trả về None nếu không tìm thấy đường
# Thuật toán IDS2
def get_actions2(state2):
    # state2 có dạng: ((r, c), frozenset({(r1, c1), (r2, c2), ...}))
    (r, c), dirt_positions = state2
    actions = []
    
    # Nếu tại vị trí robot đứng có bụi thì phải HÚT trước
    if (r, c) in dirt_positions:
        return ["SUCK"]
        
    
    if r > 0: actions.append("UP")
    if r < 2: actions.append("DOWN")
    if c > 0: actions.append("LEFT")
    if c < 2: actions.append("RIGHT")
    return actions

def result_state2(state2, action):
    (r, c), dirt_positions = state2
    
    if action == "SUCK":
        # Tạo tập hợp bụi mới đã loại bỏ vị trí hiện tại của robot
        new_dirts = frozenset(dirt_positions - {(r, c)})
        return ((r, c), new_dirts)
        
    elif action == "UP":    return ((r - 1, c), dirt_positions)
    elif action == "DOWN":  return ((r + 1, c), dirt_positions)
    elif action == "LEFT":  return ((r, c - 1), dirt_positions)
    elif action == "RIGHT": return ((r, c + 1), dirt_positions)
    return state2

def is_goal2(state2):
    
    (r, c), dirt_positions = state2
    return len(dirt_positions) == 0
def recursive_dls2(state2, limit, local_explored):
    if is_goal2(state2):
        return [state2]
    if limit <= 0:
        
        return "cutoff" 
        
    cutoff_occurred = False
    local_explored.add(state2)
    
    for action in get_actions2(state2):
        child = result_state2(state2, action)
        if child not in local_explored:
            result = recursive_dls2(child, limit - 1, local_explored.copy())
            if result == "cutoff":
                cutoff_occurred = True
            elif result is not None:
                return [state2] + result
                
    if cutoff_occurred:
        return "cutoff"
    return None

def ids2(initial_state2):
    depth = 0
    while depth <= 20:
        result = recursive_dls2(initial_state2, depth, set())
        if result != "cutoff":
            return result
        depth += 1
    return None

def convert_path_to_matrices(path_states2):
   
    if not path_states2: return None
    matrix_path = []
    for state2 in path_states2:
        (r, c), dirt_positions = state2
        
        matrix = [[0 for _ in range(3)] for _ in range(3)]
        
        for (dr, dc) in dirt_positions:
            matrix[dr][dc] = 1
        
        matrix[r][c] = 'x1' if matrix[r][c] == 1 else 'x'
        matrix_path.append(matrix)
    return matrix_path

# Thuật toán A*
def heuristic(state):
    
    return sum(row.count(1) + row.count('x1') for row in state)
def a_star_search(start_state):
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)

    #  Khởi tạo tập FRONTIER = {Start} với f(Start) = g(Start) + h(Start) = 0 + h(Start)
    count = 0
    start_h = heuristic(start_state)
    
    frontier = [(start_h, count, start_state, 0, [start_state])]
    
    # Khởi tạo tập REACHED = {}
    
    reached = {state_to_tuple(start_state): 0}
    
    
    frontier_map = {state_to_tuple(start_state): 0}

    #TRONG KHI (FRONTIER không rỗng):
    while frontier:
        
        f_n, _, n, g_n, path = heapq.heappop(frontier)
        n_tuple = state_to_tuple(n)

        
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
# Thuật toán IDS1
def recursive_dls(state, limit, explored_in_path):
    if is_goal(state):
        return [state]
    if limit <= 0:
        return "cutoff"
    
    cutoff_occurred = False
    
    # Biến trạng thái hiện tại thành tuple để kiểm tra lặp
    state_tuple = tuple(tuple(row) for row in state)
    explored_in_path.add(state_tuple)

    for action in get_actions(state):
        child = result_state(state, action)
        child_tuple = tuple(tuple(row) for row in child)
        
        # CHỈ ĐI TIẾP nếu ô này chưa nằm trong đường đi hiện tại (tránh đi lùi)
        if child_tuple not in explored_in_path:
            result = recursive_dls(child, limit - 1, explored_in_path.copy())
            
            if result == "cutoff":
                cutoff_occurred = True
            elif result is not None:
                return [state] + result
    
    if cutoff_occurred:
        return "cutoff"
    return None

def ids(state):
    depth = 0
    
    while depth <= 20: 
        print(f"Đang tìm ở độ sâu (limit): {depth}")
        
        result = recursive_dls(state, depth, set())
        
        if result != "cutoff":
            return result
        depth += 1
    return None
# Thuật toán DFS1
def dfs(state):

    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)

    stack = []
    stack.append((state, [state]))  

    explored = set()

    while stack:
        current_state, path = stack.pop()   # LIFO

        if is_goal(current_state):
            return path

        state_tuple = state_to_tuple(current_state)

        if state_tuple in explored:
            continue

        explored.add(state_tuple)

        for action in reversed(get_actions(current_state)):
            child = result_state(current_state, action)

            if state_to_tuple(child) not in explored:
                stack.append((child, path + [child]))

    return None
# Thuật toán BFS1
def bfs(state):

    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)

    queue = deque()
    queue.append((state, [state]))   

    explored = set()

    while queue:
        current_state, path = queue.popleft()

        if is_goal(current_state):
            return path

        state_tuple = state_to_tuple(current_state)

        if state_tuple in explored:
            continue

        explored.add(state_tuple)

        for action in get_actions(current_state):
            child = result_state(current_state, action)

            if state_to_tuple(child) not in explored:
                queue.append((child, path + [child]))

    return None
# Thuật toán UCS
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
    if state[r_start][c_start] == 1: 
        start_node[r_start][c_start] = 'x1'

    frontier = []
    
    heapq.heappush(frontier, (0, count, start_node, [start_node]))
    
    explored = set()

    while frontier:
        
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
# Thuật toán And Or
def and_or_graph_search(start_state):
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)

    def or_search(state, path):
        if is_goal(state):
            return [] 
            
        curr_tuple = state_to_tuple(state)
        if curr_tuple in path:
            return "failure" # Tránh lặp trạng thái trên nhánh
            
        for action in get_actions(state):
            
            child = result_state(state, action)
            result_states = [child] 
            
           
            plan = and_search(result_states, path | {curr_tuple})
            
            if plan != "failure":
                
                return [child] + plan
        return "failure"

    def and_search(states, path):
        
        plans = []
        for s in states:
            plan_s = or_search(s, path)
            if plan_s == "failure":
                return "failure"
            plans.extend(plan_s)
        return plans

   
    res = or_search(start_state, set())
    if res == "failure":
        return None
    return [start_state] + res
# Thuật toán local beam
def local_beam_search(start_state, k=3):
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)
        
    def get_value(state):
        
        return -heuristic(state)

    
    current_state_set = [start_state]
    
    
    beam = [(start_state, [start_state])]
    
    reached = {state_to_tuple(start_state)}

    
    while True:
       
        if not beam:
            return [start_state]

        
        all_candidates = []

       
        for current_state, path in beam:
            # Sinh tất cả các trạng thái lân cận của State
            actions = get_actions(current_state)
            for action in actions:
                child = result_state(current_state, action)
                child_tuple = state_to_tuple(child)
                
                if child_tuple not in reached:
                    
                    all_candidates.append((child, path + [child]))

        
        if not all_candidates:
            best_remaining = max(beam, key=lambda x: get_value(x[0]))
            return best_remaining[1]

        
        for child, path in all_candidates:
            
            if is_goal(child):
                return path

        
        all_candidates.sort(key=lambda x: get_value(x[0]), reverse=True)

        
        for child, _ in all_candidates[:k]:
            reached.add(state_to_tuple(child))

        
        beam = all_candidates[:k]

# Thuật toán simulate annealing
def simulated_annealing(start_state):
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)
        
    def get_value(state):
        
        return -heuristic(state)

    # Khai báo các tham số cho quá trình giảm nhiệt (Luyện kim)
    T = 100.0          # Nhiệt độ ban đầu (Initial Temperature)
    alpha = 0.95        # Tốc độ làm nguội (Cooling Rate)
    T_min = 0.01        # Nhiệt độ tối thiểu để dừng
    
    current_state = start_state
    path = [current_state]
    reached = {state_to_tuple(current_state)} # Chặn trùng lặp

    while T > T_min:
        if is_goal(current_state):
            return path

        # Sinh tất cả các trạng thái lân cận của Current_State
        actions = get_actions(current_state)
        neighbors = []
        for action in actions:
            child = result_state(current_state, action)
            child_tuple = state_to_tuple(child)
            if child_tuple not in reached:
                neighbors.append(child)
                
        # Nếu không còn lối đi nào mới, dừng thuật toán
        if not neighbors:
            return path
            
        # Chọn NGẪU NHIÊN một trạng thái lân cận (Next_State) để xem xét
        next_state = random.choice(neighbors)
        
        # Tính toán độ chênh lệch chất lượng giữa trạng thái mới và cũ
        # delta_E = Value(Next_State) - Value(Current_State)
        delta_E = get_value(next_state) - get_value(current_state)
        
        # NẾU trạng thái mới tốt hơn (delta_E > 0): CHẤP NHẬN NGAY
        if delta_E > 0:
            current_state = next_state
            path.append(current_state)
            reached.add(state_to_tuple(current_state))
        # NGƯỢC LẠI (trạng thái mới tệ hơn): CHẤP NHẬN VỚI XÁC SUẤT e^(delta_E / T)
        else:
            
            probability = math.exp(delta_E / T)
            
            # Bốc một số ngẫu nhiên từ 0 đến 1, nếu nhỏ hơn xác suất quy định thì chấp nhận "đi lùi"
            if random.random() < probability:
                current_state = next_state
                path.append(current_state)
                reached.add(state_to_tuple(current_state))
                
        # Làm nguội nhiệt độ sau mỗi vòng lặp
        T = T * alpha
        
    return path

# Thuật toán không nhìn thấy 
def sensorless_search(start_state):
    current = start_state
    path = [current]
    fixed_actions = [
        "LEFT", "LEFT", "UP", "UP", "SUCK",
        "RIGHT", "SUCK", "RIGHT", "SUCK",
        "DOWN", "SUCK", "LEFT", "SUCK", "LEFT", "SUCK",
        "DOWN", "SUCK", "RIGHT", "SUCK", "RIGHT", "SUCK"
    ]
    for action in fixed_actions:
        if is_goal(current):
            break
        current = result_state(current, action)
        path.append(current)
    return path 

# Thuật toán nhìn thấy một phần
def partial_sensing_search(start_state):
    
    current = start_state
    path = [current]
    def state_to_tuple(s): return tuple(tuple(row) for row in s)
    reached = {state_to_tuple(current)}
    
    while not is_goal(current):
        actions = get_actions(current)
        next_step = None
        
        
        for action in actions:
            child = result_state(current, action)
            if state_to_tuple(child) not in reached:
                next_step = child
                break
                
        if next_step is None and actions:
           
            next_step = result_state(current, actions[0])
            
        if next_step is None:
            break
            
        current = next_step
        path.append(current)
        reached.add(state_to_tuple(current))
        
        if len(path) > 50: # Giới hạn chặn lặp vô hạn do thiếu tầm nhìn toàn cục
            break
    return path
#----------------------------------------------------------------------------------------
class RobotVacuumUI(ctk.CTk):
    def get_path_labels(self, path_states):       
        labels = []
        for i in range(len(path_states) - 1):
            current = path_states[i]
            next_s = path_states[i+1]
            
            r1, c1 = self.find_robot_in_state(current)
            r2, c2 = self.find_robot_in_state(next_s)
            
            if r1 == r2 and c1 == c2:
                labels.append("SUCK")
            elif r2 < r1: labels.append("UP")
            elif r2 > r1: labels.append("DOWN")
            elif c2 < c1: labels.append("LEFT")
            elif c2 > c1: labels.append("RIGHT")
        return " -> ".join(labels)

    def find_robot_in_state(self, state):        
        for i in range(3):
            for j in range(3):
                if state[i][j] in ['x', 'x1']:
                    return i, j
        return 0, 0
    def __init__(self):
        super().__init__()

        self.title("AI Vacuum Cleaner Simulator - Pro Version")
        self.geometry("1000x650")

        # --- DỮ LIỆU ---
        self.grid_size = 3
        self.robot_pos = [0, 1]
        self.grid_data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]] # 1 là bẩn, 0 là sạch
        self.cells = {} # Lưu các widget ô vuông

        self.setup_ui()
        self.reset_board()

    def setup_ui(self):
        # Chia layout chính thành 2 cột: Sidebar (Trái) và Workspace (Phải)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= SIDEBAR (Điều khiển) =================
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.sidebar, text="THUẬT TOÁN", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # Chia danh sách thành 2 nhóm 
        algorithms = [
            "BFS", "BFS2",
            "DFS", "DFS2",
            "UCS", "IDS2",
            "A* Search", "IDA*",
            "IDS", "Tham Lam",
            "Leo Đồi", "Leo Đồi Cao",
            "Leo Đồi Ngẫu Nhiên", "Local Beam",
            "Luyện Kim", "AND-OR",
            "Không Nhìn Thấy", "Nhìn 1 Phần"
        ]
    # Tạo một khung chứa riêng cho các nút thuật toán để dùng grid
        algo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        algo_frame.pack(pady=5)

        for index, algo in enumerate(algorithms):
    
            row_idx = index // 2
            col_idx = index % 2
    
            btn = ctk.CTkButton(
                algo_frame, 
                text=algo, 
                width=100, 
                command=lambda a=algo: self.run_algorithm(a)
            )
    
            btn.grid(row=row_idx, column=col_idx, padx=5, pady=5)
        
        
        # Cài đặt vị trí
        ctk.CTkLabel(self.sidebar, text="Vị trí Robot (R, C):").pack()
        self.entry_pos = ctk.CTkEntry(self.sidebar, placeholder_text="Ví dụ: 0,1")
        self.entry_pos.pack(pady=5, padx=20)
        
        ctk.CTkButton(self.sidebar, text="Cập nhật Robot", fg_color="green", command=self.update_robot_manual).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Reset Map (Random)", fg_color="transparent", border_width=2, command=self.reset_board).pack(pady=20)

        # ================= WORKSPACE (Hiển thị) =================
        self.workspace = ctk.CTkFrame(self)
        self.workspace.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Khu vực Grid (Bàn cờ)
        self.grid_frame = ctk.CTkFrame(self.workspace, fg_color="transparent")
        self.grid_frame.pack(pady=20)
        self.render_grid()

        # Khu vực Log & Thống kê
        self.info_frame = ctk.CTkFrame(self.workspace)
        self.info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.stats_label = ctk.CTkLabel(self.info_frame, text="Trạng thái: Sẵn sàng | Path Cost: 0", font=("Arial", 14))
        self.stats_label.pack(pady=10)

        self.log_box = ctk.CTkTextbox(self.info_frame, height=150)
        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_box.insert("0.0", "Hệ thống đã khởi động...\nChọn một thuật toán để bắt đầu.")

    def render_grid(self):
        # Xóa grid cũ
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                color = "#E74C3C" if self.grid_data[r][c] == 1 else "#2ECC71" # Đỏ nếu bẩn, xanh nếu sạch
                text = "💩" if self.grid_data[r][c] == 1 else ""
                
                # Nếu là vị trí robot
                if [r, c] == self.robot_pos:
                    cell = ctk.CTkLabel(self.grid_frame, text="🤖", width=100, height=100, fg_color="#3498DB", corner_radius=10)
                else:
                    cell = ctk.CTkLabel(self.grid_frame, text=text, width=100, height=100, fg_color=color, corner_radius=10)
                
                cell.grid(row=r, column=c, padx=5, pady=5)

    def reset_board(self):
        # Tạo map ngẫu nhiên
        self.grid_data = [[random.choice([0, 1]) for _ in range(3)] for _ in range(3)]
        self.render_grid()
        self.log_message("Đã làm mới bản đồ.")

    def update_robot_manual(self):
        try:
            val = self.entry_pos.get().split(",")
            self.robot_pos = [int(val[0]), int(val[1])]
            self.render_grid()
        except:
            self.log_message("Lỗi: Nhập vị trí sai định dạng!")

    def log_message(self, msg):
        self.log_box.insert("end", f"\n> {msg}")
        self.log_box.see("end")
    def format_map_to_string(self, matrix_state):
        
        lines = []
        for row in matrix_state:
            row_chars = []
            for cell in row:
                if cell == 'x' or str(cell).startswith('x'): 
                    row_chars.append(" R ")  # Robot
                elif cell == 1 or cell == '1':
                    row_chars.append(" * ")  # Bụi
                else:
                    row_chars.append(" _ ")  # Ô trống
            lines.append("[" + "".join(row_chars) + "]")
        return "\n".join(lines)
    
    def get_action_details(self, path_states):
        
        if not path_states or len(path_states) < 2:
            return [], ""
            
        log_steps = []
        action_names = []
        
        # Hàm tìm vị trí robot trong ma trận
        def find_robot(matrix):
            for r in range(len(matrix)):
                for c in range(len(matrix[r])):
                    if str(matrix[r][c]).startswith('x'):
                        return r, c
            return 0, 0

        
        def count_dust(matrix):
            return sum(1 for row in matrix for cell in row if '1' in str(cell))

        for i in range(len(path_states) - 1):
            curr_state = path_states[i]
            next_state = path_states[i+1]
            
            r_curr, c_curr = find_robot(curr_state)
            r_next, c_next = find_robot(next_state)
            dust_curr = count_dust(curr_state)
            dust_next = count_dust(next_state)
            
           
            if dust_next < dust_curr:
                log_steps.append(f"Hut Bui tai: {r_curr} {c_curr}")
                action_names.append("SUCK")
           
            else:
                if r_next < r_curr:
                    log_steps.append(f"Move UP: {r_next} {c_next}")
                    action_names.append("UP")
                elif r_next > r_curr:
                    log_steps.append(f"Move DOWN: {r_next} {c_next}")
                    action_names.append("DOWN")
                elif c_next < c_curr:
                    log_steps.append(f"Move LEFT: {r_next} {c_next}")
                    action_names.append("LEFT")
                elif c_next > c_curr:
                    log_steps.append(f"Move RIGHT: {r_next} {c_next}")
                    action_names.append("RIGHT")
                    
        return log_steps, " ".join(action_names)

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def run_algorithm(self, algo_name):
        self.stats_label.configure(text=f"Đang tính toán {algo_name}...")
        self.log_message(f"Đang chạy {algo_name}...")
        
        
        current_map = []
        for r_idx in range(len(self.grid_data)):
            row = []
            for c_idx in range(len(self.grid_data[r_idx])):
                # Ép toàn bộ ô về chuỗi '1' hoặc '0' để tránh lỗi so sánh Số vs Chữ
                row.append(str(self.grid_data[r_idx][c_idx]))
            current_map.append(row)
            
       
        r, c = self.robot_pos
        if current_map[r][c] == '1':
            current_map[r][c] = 'x1'
        else:
            current_map[r][c] = 'x'
            
        path_states = None
        cost = 0
        
        
        if algo_name == "UCS":
            self.log_message("UCS đang chạy...")
            self.update() 
            
            
            path_states, cost = ucs(current_map)
            
        elif algo_name == "BFS":
            
            result = bfs(current_map) 
            if isinstance(result, tuple): 
                path_states, cost = result
            else: 
                path_states = result
                cost = len(path_states) - 1 if path_states else 0
                
        elif algo_name == "DFS":
            self.log_message("DFS đang chạy...")
            self.update() 
            
            path_states = dfs(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
        elif algo_name == "A* Search":
            self.log_message("A* Search đang chạy...")
            self.update()
            
            
            path_states, cost = a_star_search(current_map)
            
        elif algo_name == "IDS": 
            self.log_message("IDS đang tính toán...")
            self.update() 
            
            
            path_states = ids(current_map) 
            
            
            cost = len(path_states) - 1 if path_states else 0

        elif algo_name == "BFS2":
            self.log_message("BFS2 đang chạy...")
            self.update()
            
            
            r_start, c_start = self.robot_pos
            dirt_set = set()
            for r in range(3):
                for c in range(3):
                    if self.grid_data[r][c] == 1:
                        dirt_set.add((r, c))
            initial_state2 = ((r_start, c_start), frozenset(dirt_set))
            
           
            path_states2 = bfs2(initial_state2)
            
            
            path_states = convert_path_to_matrices(path_states2)
            cost = len(path_states) - 1 if path_states else 0
            
        elif algo_name == "DFS2":
            self.log_message("DFS2 đang chạy...")
            self.update()
            
            
            r_start, c_start = self.robot_pos
            dirt_set = set()
            for r in range(3):
                for c in range(3):
                    if self.grid_data[r][c] == 1:
                        dirt_set.add((r, c))
            initial_state2 = ((r_start, c_start), frozenset(dirt_set))
            
            
            path_states2 = dfs2(initial_state2)
            
            
            path_states = convert_path_to_matrices(path_states2)
            cost = len(path_states) - 1 if path_states else 0
            
        elif algo_name == "IDS2":
            self.log_message("IDS2 đang chạy...")
            self.update()
    
    
            r_start, c_start = self.robot_pos
            dirt_set = set()
            for r in range(3):
                for c in range(3):
                    if self.grid_data[r][c] == 1:
                        dirt_set.add((r, c))
            initial_state2 = ((r_start, c_start), frozenset(dirt_set))
    
    
            path_states2 = ids2(initial_state2)
    
    
            path_states = convert_path_to_matrices(path_states2)
            cost = len(path_states) - 1 if path_states else 0
            
        elif algo_name == "IDA*":
            self.log_message("IDA* đang chạy...")
            self.update()
            
            
            path_states = ida_star(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
        elif algo_name == "Tham Lam":
            self.log_message("Tham Lam đang chạy...")
            self.update()
            
            
            path_states = greedy_search(current_map)
            cost = len(path_states) - 1 if path_states else 0

        elif algo_name == "Leo Đồi":
            self.log_message("Leo Đồi đơn giản đang chạy...")
            self.update()
            
            
            path_states = simple_hill_climbing(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
            
            if path_states and not is_goal(path_states[-1]):
                self.log_message("> CẢNH BÁO: Thuật toán bị kẹt ở cực đại cục bộ (Local Maximum) nên dừng lại!")
        
        elif algo_name == "Leo Đồi Cao":
            self.log_message("Leo Đồi dốc nhất đang chạy...")
            self.update()
            
            
            path_states = steepest_ascent_hill_climbing(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
           
            if path_states and not is_goal(path_states[-1]):
                self.log_message("> CẢNH BÁO: Thuật toán bị kẹt ở cực đại cục bộ (Local Maximum) nên dừng lại!")
        
        elif algo_name == "Leo Đồi Ngẫu Nhiên":
            self.log_message("Leo Đồi ngẫu nhiên đang chạy...")
            self.update()
            
            
            path_states = stochastic_hill_climbing(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
           
            if path_states and not is_goal(path_states[-1]):
                self.log_message("> CẢNH BÁO: Thuật toán bị kẹt ở cực đại cục bộ (Local Maximum)!")
        
        elif algo_name == "Local Beam":
            self.log_message("Local Beam Search (k=3) đang chạy...")
            self.update()
            
            
            path_states = local_beam_search(current_map, k=3)
            cost = len(path_states) - 1 if path_states else 0
            
            
            if path_states and not is_goal(path_states[-1]):
                self.log_message("> CẢNH BÁO: Thuật toán dừng lại do tất cả các chùm đều rơi vào cực đại cục bộ!")

        elif algo_name == "Luyện Kim":
            self.log_message("Mô phỏng luyện kim đang chạy...")
            self.update()
            
            
            path_states = simulated_annealing(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
            
            if path_states and not is_goal(path_states[-1]):
                self.log_message("> CẢNH BÁO: Thuật toán dừng lại do đã nguội nhiệt độ mà chưa tìm thấy đích!")

        elif algo_name == "AND-OR":
            self.log_message("AND-OR Graph Search đang chạy...")
            self.update()
            
            
            path_states = and_or_graph_search(current_map)
            cost = len(path_states) - 1 if path_states else 0

        elif algo_name == "Không Nhìn Thấy":
            self.log_message("Tìm kiếm không nhìn thấy (Sensorless) đang chạy chuỗi hành động cố định...")
            self.update()
            path_states = sensorless_search(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
        elif algo_name == "Nhìn 1 Phần":
            self.log_message("Tìm kiếm nhìn thấy một phần (Partial Sensing) đang dò đường...")
            self.update()
            path_states = partial_sensing_search(current_map)
            cost = len(path_states) - 1 if path_states else 0

        
            
        # --- ĐOẠN HIỂN THỊ TỪNG BƯỚC ---
        if path_states and len(path_states) > 1:
            
            log_steps, best_path_str = self.get_action_details(path_states)
            
           
            cost = len(path_states) - 1
            nodes_visited = len(path_states) 
            
            
            self.log_message(f"--- Khoi chay {algo_name} ---")
            self.log_message("Duong di tim thay:")
            self.log_message(best_path_str)
            
            
            try:
                self.lbl_best_path_content.config(text=best_path_str if best_path_str else "Đang đứng tại đích!")
            except AttributeError:
                pass

            # HÀM ĐIỀU KHIỂN CHẠY TỪNG BƯỚC ĐỆ QUY LỒNG BÊN TRONG
            def run_step(step_idx):
                if step_idx < len(log_steps):
                    
                    self.log_message(log_steps[step_idx])
                    
                    
                    next_matrix = path_states[step_idx + 1]
                    
                    
                    for r_idx, row in enumerate(next_matrix):
                        for c_idx, cell in enumerate(row):
                            cell_str = str(cell)
                            
                            
                            if 'x' in cell_str:
                                self.robot_pos = [r_idx, c_idx]
                                
                                self.grid_data[r_idx][c_idx] = 1 if '1' in cell_str else 0
                            else:
                                
                                self.grid_data[r_idx][c_idx] = 1 if cell_str == '1' or cell == 1 else 0
                    
                    
                    self.render_grid() 
                    
                    
                    self.stats_label.configure(text=f"Thuật toán: {algo_name} | Path Cost: {step_idx + 1} | Nodes: {step_idx + 2}")
                    
                    self.update()
                    
                    
                    self.after(500, lambda: run_step(step_idx + 1))
                else:
                    self.log_message("=== ĐA HOÀN THÀNH NHIỆM VỤ ===")
                    self.stats_label.configure(text=f"Thuật toán: {algo_name} | Path Cost: {cost} | Nodes: {nodes_visited}")
            
            
            run_step(0)
            
        else:
            self.log_message("> Không tìm thấy đường đi hoặc thuật toán bị kẹt!")
            self.stats_label.configure(text=f"Thuật toán: {algo_name} | Path Cost: Đơ | Nodes: Đơ")
            try:
                self.lbl_best_path_content.config(text="FAIL")
            except AttributeError:
                pass

    def animate_solution(self, path_states):
        """Hàm xử lý chuyển động từng bước một"""
        for state in path_states:
            
            for r in range(3):
                for c in range(3):
                    val = state[r][c]
                    
                    if val == 'x': 
                        
                        self.grid_data[r][c] = 0
                        self.robot_pos = [r, c]
                    elif val == 'x1':
                        
                        self.grid_data[r][c] = 1
                        self.robot_pos = [r, c]
                    else:
                        
                        self.grid_data[r][c] = val
            
            
            self.render_grid()
            
            self.update() 
            
            self.after(400) 
            
        self.log_message("Robot đã hoàn thành lộ trình dọn dẹp!")

if __name__ == "__main__":
    app = RobotVacuumUI()
    app.mainloop()