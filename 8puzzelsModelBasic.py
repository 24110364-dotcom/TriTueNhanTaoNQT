from collections import deque

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def find_blank(state):
    return state.index(0)


def move_up(state):
    idx = find_blank(state)
    if idx < 3: return None
    new_state = list(state)
    new_state[idx], new_state[idx-3] = new_state[idx-3], new_state[idx]
    return tuple(new_state)

def move_down(state):
    idx = find_blank(state)
    if idx > 5: return None
    new_state = list(state)
    new_state[idx], new_state[idx+3] = new_state[idx+3], new_state[idx]
    return tuple(new_state)

def move_left(state):
    idx = find_blank(state)
    if idx % 3 == 0: return None
    new_state = list(state)
    new_state[idx], new_state[idx-1] = new_state[idx-1], new_state[idx]
    return tuple(new_state)

def move_right(state):
    idx = find_blank(state)
    if idx % 3 == 2: return None
    new_state = list(state)
    new_state[idx], new_state[idx+1] = new_state[idx+1], new_state[idx]
    return tuple(new_state)


def print_matrix(state):
    for i in range(0, 9, 3):
        print(state[i], state[i+1], state[i+2])
    print("-" * 10)

# Model-based Agent Solver
def solve_8_puzzle(start_state):
    queue = deque([(start_state, [])])
    
    model_visited = set()
    model_visited.add(start_state)
    
    while queue:
        current_state, path = queue.popleft()
        
        if current_state == GOAL:
            return path
            
        
        moves = [
            (move_up, "Up"),
            (move_down, "Down"),
            (move_left, "Left"),
            (move_right, "Right")
        ]
        
        for move_func, move_name in moves:
            next_state = move_func(current_state)
            
            
            if next_state and next_state not in model_visited:
                model_visited.add(next_state)
                queue.append((next_state, path + [move_name]))
                
    return None


if __name__ == "__main__":
    
    start = (1, 2, 3, 4, 0, 6, 7, 5, 8)
    
    print("Trạng thái ban đầu:")
    print_matrix(start)
    
    steps = solve_8_puzzle(start)
    
    if steps:
        print(f"Tìm thấy đường đi với {len(steps)} bước:")
        print(" -> ".join(steps))
    else:
        print("Không tìm thấy lời giải!")