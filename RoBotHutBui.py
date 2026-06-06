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
        # Định nghĩa giống bài trước: Ít bụi hơn -> Heuristic nhỏ -> Value (-Heuristic) cao hơn
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
        """
        Hàm tìm kiếm đệ quy (DFS) giới hạn bởi threshold.
        g: Chi phí đường đi (số bước từ start_state đến current)
        """
        current = path[-1]
        h = heuristic(current) # Hàm đếm số ô bụi còn lại
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
    # Vì là Stack nên ta dùng List và dùng hàm pop() để lấy phần tử cuối cùng ra trước
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
        
    # Các hành động di chuyển hợp lệ trong map 3x3
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
    # Đích là khi tập hợp các vị trí có bụi trống trơn
    (r, c), dirt_positions = state2
    return len(dirt_positions) == 0
def recursive_dls2(state2, limit, local_explored):
    if is_goal2(state2):
        return [state2]
    if limit <= 0:
        # Thay vì trả về chuỗi, ta dùng tuple đặc biệt để không bị lỗi so sánh
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
    """Hàm ảo thuật: Dịch chuyển danh sách Tiếp cận 2 về Ma trận Tiếp cận 1 cho UI chạy"""
    if not path_states2: return None
    matrix_path = []
    for state2 in path_states2:
        (r, c), dirt_positions = state2
        # Tạo một ma trận 3x3 trống
        matrix = [[0 for _ in range(3)] for _ in range(3)]
        # Đổ bụi vào ma trận
        for (dr, dc) in dirt_positions:
            matrix[dr][dc] = 1
        # Đặt robot vào ma trận
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
    # Với bàn cờ 3x3, limit tầm 15-20 là đủ. Để sâu quá máy sẽ treo.
    while depth <= 20: 
        print(f"Đang tìm ở độ sâu (limit): {depth}")
        # Mỗi lần tăng độ sâu, ta reset lại danh sách explored_in_path
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
    stack.append((state, [state]))   # (trạng thái, đường đi)

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
    queue.append((state, [state]))   # (trạng thái, đường đi)

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
# Thuật toán local beam
def local_beam_search(start_state, k=3):
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)
        
    def get_value(state):
        # Càng ít bụi -> Heuristic càng nhỏ -> Value (-Heuristic) càng cao
        return -heuristic(state)

    # 1. Khởi tạo: Current_State_set chứa trạng thái bắt đầu ban đầu
    # (Vì bài toán chỉ có 1 start_state cố định, ta đưa nó vào làm gốc của chùm)
    current_state_set = [start_state]
    
    # Để hiển thị được lộ trình robot chạy trên giao diện, ta cần lưu vết đường đi.
    # Ta lưu kèm đường đi của từng nhánh dưới dạng: (trạng thái_hiện_tại, [danh_sách_các_bước_đã_qua])
    beam = [(start_state, [start_state])]
    
    reached = {state_to_tuple(start_state)} # Chặn trùng lặp trạng thái giữa các chùm

    # 2. TRONG KHI (đúng):
    while True:
        # Kiểm tra nếu chùm bị rỗng (không còn đường đi nào), thuật toán dừng
        if not beam:
            return [start_state]

        # Neighbor_States = rỗng
        all_candidates = []

        # 2.1. SINH TRẠNG THÁI LÂN CẬN: VỚI MỖI State trong Current_State_set
        for current_state, path in beam:
            # Sinh tất cả các trạng thái lân cận của State
            actions = get_actions(current_state)
            for action in actions:
                child = result_state(current_state, action)
                child_tuple = state_to_tuple(child)
                
                if child_tuple not in reached:
                    # Thêm các trạng thái lân cận này vào danh sách ứng viên (gồm trạng thái con và đường đi tích lũy)
                    all_candidates.append((child, path + [child]))

        # Nếu không sinh thêm được bất kỳ trạng thái mới nào, dừng lại và trả về nhánh tốt nhất hiện tại
        if not all_candidates:
            best_remaining = max(beam, key=lambda x: get_value(x[0]))
            return best_remaining[1]

        # 2.2. KIỂM TRA ĐÍCH: VỚI MỖI Neighbor trong Neighbor_States
        for child, path in all_candidates:
            # NẾU Neighbor == Goal: TRẢ VỀ Neighbor / Tìm thấy đích, dừng ngay lập tức toàn bộ thuật toán
            if is_goal(child):
                return path

        # 2.3. LỰA CHỌN CHÙM (NẾU CHƯA TÌM THẤY ĐÍCH):
        # Sắp xếp Neighbor_States theo thứ tự giá trị hàm mục tiêu h tốt dần (Value cao dần)
        all_candidates.sort(key=lambda x: get_value(x[0]), reverse=True)

        # Cập nhật reached để chặn trùng cho các vòng sau
        for child, _ in all_candidates[:k]:
            reached.add(state_to_tuple(child))

        # Current_State_set = Lấy k trạng thái tốt nhất từ Neighbor_States đã sắp xếp
        beam = all_candidates[:k]

# Thuật toán simulate annealing
def simulated_annealing(start_state):
    def state_to_tuple(s):
        return tuple(tuple(row) for row in s)
        
    def get_value(state):
        # Ít bụi -> Heuristic nhỏ -> Value (-Heuristic) cao
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
            # Vì delta_E âm và T dương nên delta_E / T sẽ âm -> math.exp sẽ ra một số từ 0 đến 1
            probability = math.exp(delta_E / T)
            
            # Bốc một số ngẫu nhiên từ 0 đến 1, nếu nhỏ hơn xác suất quy định thì chấp nhận "đi lùi"
            if random.random() < probability:
                current_state = next_state
                path.append(current_state)
                reached.add(state_to_tuple(current_state))
                
        # Làm nguội nhiệt độ sau mỗi vòng lặp
        T = T * alpha
        
    return path
#----------------------------------------------------------------------------------------
class RobotVacuumUI(ctk.CTk):
    def get_path_labels(self, path_states):
        """Dịch danh sách các trạng thái thành danh sách hành động (UP, SUCK,...)"""
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
        """Hàm phụ để tìm vị trí robot trong một ma trận bất kỳ"""
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

        # Chia danh sách thành 2 nhóm rõ ràng
        algorithms = [
            "BFS", "BFS2",
            "DFS", "DFS2",
            "UCS", "IDS2",
            "A* Search", "IDA*",
            "IDS", "Tham Lam",
            "Leo Đồi", "Leo Đồi Cao",
            "Leo Đồi Ngẫu Nhiên", "Local Beam",
            "Luyện Kim" 
        ]
# Tạo một khung chứa riêng cho các nút thuật toán để dùng grid
        algo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        algo_frame.pack(pady=5)

        for index, algo in enumerate(algorithms):
    # Tính toán vị trí hàng và cột (mỗi hàng có 2 nút)
            row_idx = index // 2
            col_idx = index % 2
    
            btn = ctk.CTkButton(
                algo_frame, 
                text=algo, 
                width=100, # Giảm độ rộng nút lại một chút để vừa 2 cột
                command=lambda a=algo: self.run_algorithm(a)
            )
    # Xếp nút theo dạng lưới 2 cột
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

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def run_algorithm(self, algo_name):
        self.stats_label.configure(text=f"Đang tính toán {algo_name}...")
        
        self.log_message(f"Đang chạy {algo_name}...")
        
        # Chuẩn bị dữ liệu đầu vào (Giống hệt UCS)
        current_map = deepcopy(self.grid_data)
        r, c = self.robot_pos
        if current_map[r][c] == 1:
            current_map[r][c] = 'x1'
        else:
            current_map[r][c] = 'x'
            
        path_states = None
        cost = 0
        
        # --- ĐÂY LÀ KHU VỰC KẾT NỐI 5 THUẬT TOÁN CÒN LẠI ---
        if algo_name == "UCS":
            self.log_message("UCS đang chạy...")
            self.update() # Thêm dòng này để ép giao diện cập nhật ngay lập tức
            
            # Đoạn code chuẩn của bạn giữ nguyên:
            path_states, cost = ucs(current_map)
            
        elif algo_name == "BFS":
            # Gọi hàm bfs của bạn. Nếu bfs không trả về cost, hãy tính bằng len(path)
            result = bfs(current_map) 
            if isinstance(result, tuple): # Nếu hàm trả về (path, cost)
                path_states, cost = result
            else: # Nếu hàm chỉ trả về path
                path_states = result
                cost = len(path_states) - 1 if path_states else 0
                
        elif algo_name == "DFS":
            self.log_message("DFS đang chạy...")
            self.update() # Thêm dòng này để ép giao diện mượt mà hơn
            
            path_states = dfs(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
        elif algo_name == "A* Search":
            self.log_message("A* Search đang chạy...")
            self.update()
            
            # Gọi hàm của bạn (hàm trả về 2 giá trị là path_states và cost)
            path_states, cost = a_star_search(current_map)
            
        elif algo_name == "IDS": # Hoặc "IDS" tùy theo tên nút bấm của bạn
            self.log_message("IDS đang tính toán...")
            self.update() # Ép giao diện cập nhật chữ, tránh bị đơ màn hình
            
            # GỌI HÀM ids VÀ TRUYỀN current_map VÀO
            path_states = ids(current_map) 
            
            # Tính toán cost dựa trên kết quả trả về
            cost = len(path_states) - 1 if path_states else 0

        elif algo_name == "BFS2":
            self.log_message("BFS2 đang chạy...")
            self.update()
            
            # 1. Dịch từ Ma trận giao diện sang Tuple (Tiếp cận 2)
            r_start, c_start = self.robot_pos
            dirt_set = set()
            for r in range(3):
                for c in range(3):
                    if self.grid_data[r][c] == 1:
                        dirt_set.add((r, c))
            initial_state2 = ((r_start, c_start), frozenset(dirt_set))
            
            # 2. Chạy thuật toán BFS2
            path_states2 = bfs2(initial_state2)
            
            # 3. Dịch ngược kết quả về ma trận cho giao diện chạy animation
            path_states = convert_path_to_matrices(path_states2)
            cost = len(path_states) - 1 if path_states else 0
            
        elif algo_name == "DFS2":
            self.log_message("DFS2 đang chạy...")
            self.update()
            
            # 1. Dịch từ Ma trận giao diện sang Tuple (Tiếp cận 2)
            r_start, c_start = self.robot_pos
            dirt_set = set()
            for r in range(3):
                for c in range(3):
                    if self.grid_data[r][c] == 1:
                        dirt_set.add((r, c))
            initial_state2 = ((r_start, c_start), frozenset(dirt_set))
            
            # 2. Chạy thuật toán DFS2
            path_states2 = dfs2(initial_state2)
            
            # 3. Dịch ngược kết quả về ma trận cho giao diện chạy animation
            path_states = convert_path_to_matrices(path_states2)
            cost = len(path_states) - 1 if path_states else 0
            
        elif algo_name == "IDS2":
            self.log_message("IDS2 đang chạy...")
            self.update()
    
    # -------------------------------------------------------------
    # BƯỚC TRUNG GIAN 1: Dịch từ Ma trận sang Tuple (Tiếp cận 2)
    # -------------------------------------------------------------
            r_start, c_start = self.robot_pos
            dirt_set = set()
            for r in range(3):
                for c in range(3):
                    if self.grid_data[r][c] == 1:
                        dirt_set.add((r, c))
            initial_state2 = ((r_start, c_start), frozenset(dirt_set))
    
    
            path_states2 = ids2(initial_state2)
    
    # -------------------------------------------------------------
    # BƯỚC TRUNG GIAN 2: Dịch ngược từ Tuple về Ma trận để chạy giao diện
    # -------------------------------------------------------------
            path_states = convert_path_to_matrices(path_states2)
            cost = len(path_states) - 1 if path_states else 0
            
        elif algo_name == "IDA*":
            self.log_message("IDA* đang chạy...")
            self.update()
            
            # Truyền thẳng ma trận current_map vào thuật toán
            path_states = ida_star(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
        elif algo_name == "Tham Lam":
            self.log_message("Tham Lam đang chạy...")
            self.update()
            
            # Vì hàm greedy_search của bạn xài Tiếp cận 1 (nhận ma trận)
            # nên truyền thẳng current_map vào luôn, siêu khỏe!
            path_states = greedy_search(current_map)
            cost = len(path_states) - 1 if path_states else 0

        elif algo_name == "Leo Đồi":
            self.log_message("Leo Đồi đơn giản đang chạy...")
            self.update()
            
            # Gọi hàm leo đồi vừa viết
            path_states = simple_hill_climbing(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
            # Kiểm tra xem có thực sự dọn sạch map không hay bị kẹt cục bộ
            if path_states and not is_goal(path_states[-1]):
                self.log_message("> CẢNH BÁO: Thuật toán bị kẹt ở cực đại cục bộ (Local Maximum) nên dừng lại!")
        
        elif algo_name == "Leo Đồi Cao":
            self.log_message("Leo Đồi dốc nhất đang chạy...")
            self.update()
            
            # Gọi hàm leo đồi dốc nhất vừa viết
            path_states = steepest_ascent_hill_climbing(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
            # Kiểm tra xem có thực sự dọn sạch map không hay bị kẹt cục bộ
            if path_states and not is_goal(path_states[-1]):
                self.log_message("> CẢNH BÁO: Thuật toán bị kẹt ở cực đại cục bộ (Local Maximum) nên dừng lại!")
        
        elif algo_name == "Leo Đồi Ngẫu Nhiên":
            self.log_message("Leo Đồi ngẫu nhiên đang chạy...")
            self.update()
            
            # Gọi hàm leo đồi ngẫu nhiên vừa viết
            path_states = stochastic_hill_climbing(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
            # Kiểm tra kẹt cục bộ
            if path_states and not is_goal(path_states[-1]):
                self.log_message("> CẢNH BÁO: Thuật toán bị kẹt ở cực đại cục bộ (Local Maximum)!")
        
        elif algo_name == "Local Beam":
            self.log_message("Local Beam Search (k=3) đang chạy...")
            self.update()
            
            # Gọi hàm local beam search vừa viết
            path_states = local_beam_search(current_map, k=3)
            cost = len(path_states) - 1 if path_states else 0
            
            # Kiểm tra kẹt cục bộ nếu hết chùm mà chưa sạch bụi
            if path_states and not is_goal(path_states[-1]):
                self.log_message("> CẢNH BÁO: Thuật toán dừng lại do tất cả các chùm đều rơi vào cực đại cục bộ!")

        elif algo_name == "Luyện Kim":
            self.log_message("Mô phỏng luyện kim đang chạy...")
            self.update()
            
            # Gọi hàm simulated annealing vừa viết
            path_states = simulated_annealing(current_map)
            cost = len(path_states) - 1 if path_states else 0
            
            # Kiểm tra kẹt cục bộ nếu nhiệt độ đã nguội mà chưa sạch bụi
            if path_states and not is_goal(path_states[-1]):
                self.log_message("> CẢNH BÁO: Thuật toán dừng lại do đã nguội nhiệt độ mà chưa tìm thấy đích!")

        # --- PHẦN HIỂN THỊ VÀ CHẠY ROBOT  ---
        if path_states:
            action_path = self.get_path_labels(path_states)
            self.stats_label.configure(
                text=f"Thuật toán: {algo_name} | Path Cost: {cost} | Nodes: {len(path_states)*2}"
            )
            
            self.animate_solution(path_states)
        else:
            self.log_message(f"Không tìm thấy đường đi bằng {algo_name}!")
        

    def animate_solution(self, path_states):
        """Hàm xử lý chuyển động từng bước một"""
        for state in path_states:
            # Duyệt qua ma trận trạng thái hiện tại để cập nhật vị trí Robot và bụi
            for r in range(3):
                for c in range(3):
                    val = state[r][c]
                    
                    if val == 'x': 
                        # Robot ở ô này và ô này SẠCH
                        self.grid_data[r][c] = 0
                        self.robot_pos = [r, c]
                    elif val == 'x1':
                        # Robot ở ô này và ô này đang BẨN (chưa hút)
                        self.grid_data[r][c] = 1
                        self.robot_pos = [r, c]
                    else:
                        # Ô bình thường (0 hoặc 1)
                        self.grid_data[r][c] = val
            
            # Vẽ lại giao diện
            self.render_grid()
            # Bắt buộc phải có self.update() để thấy chuyển động ngay lập tức
            self.update() 
            # Nghỉ 400ms (0.4 giây) giữa các bước cho dễ nhìn
            self.after(400) 
            
        self.log_message("Robot đã hoàn thành lộ trình dọn dẹp!")

if __name__ == "__main__":
    app = RobotVacuumUI()
    app.mainloop()