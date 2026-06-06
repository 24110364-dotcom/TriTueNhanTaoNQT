from collections import deque
GOAL = "123804765"

START_1 = "123084765"
START_2 = "123840765"

initial_belief_state = (START_1, START_2)
def get_row_col(index):
    return index // 3, index % 3

def move_blank(state, direction):
    idx = state.index('0')
    r, c = get_row_col(idx)

    if direction == 'UP': r_new, c_new = r - 1, c
    elif direction == 'DOWN': r_new, c_new = r + 1, c
    elif direction == 'LEFT': r_new, c_new = r, c - 1
    elif direction == 'RIGHT': r_new, c_new = r, c + 1

    if 0 <= r_new < 3 and 0 <= c_new < 3 :
        idx_new = r_new * 3 + c_new
        state_list = list(state)
        state_list[idx], state_list[idx_new] = state_list[idx_new], state_list[idx]
        return "".join(state_list)
    return state

def solve_sensorless_search():
    queue = deque([(initial_belief_state, [])])
    visited = set()
    visited.add(initial_belief_state)

    while queue:
        current_belief, path = queue.popleft()
        if current_belief[0] == GOAL and current_belief[1] == GOAL:
            return path
        for action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            next_s1 = current_belief[0] if current_belief[0] == GOAL else move_blank(current_belief[0], action)
            next_s2 = current_belief[1] if current_belief[1] == GOAL else move_blank(current_belief[1], action)
            
            next_belief = (next_s1, next_s2)
            if next_belief not in visited:
                visited.add(next_belief)
                queue.append((next_belief, path + [action]))

    return None
solution = solve_sensorless_search()

print("--- KẾT QUẢ TÌM KIẾM KHÔNG NHÌN THẤY ---")
print(f"Trạng thái xuất phát 1: {START_1}")
print(f"Trạng thái xuất phát 2: {START_2}")
print(f"Trạng thái Đích cần đạt: {GOAL}\n")

if solution:
    print(f"Tìm thấy chuỗi hành động thành công ({len(solution)} bước):")
    print(" -> ".join(solution))
else:
    print("Không tìm thấy chuỗi hành động nào thỏa mãn!")