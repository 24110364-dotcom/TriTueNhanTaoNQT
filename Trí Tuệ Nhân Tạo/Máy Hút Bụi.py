import random
m, n = 3, 3 
environment = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]

def possible_move(x, y):
    move = []
    if x > 0:
        move.append("up")
    if x < m - 1:
        move.append("down")
    if y > 0:
        move.append("left")
    if y < n - 1:
        move.append("right")
    return move

def run_agent(steps=10):
    x, y = random.randint(0, m-1), random.randint(0, n-1)
    
    print("môi trường ban đầu:")
    for row in environment: print(row)

    for i in range(steps):
        state_value = environment[x][y]
        moves = possible_move(x, y)
        
        print(f"Bước {i+1}: Tại ({x}, {y}), Trạng thái = {state_value}")
        
        
        if state_value == 1:
            print(" Bẩn => Đang hút")
            environment[x][y] = 0
            action = random.choice(moves)
            print(f" Sau khi hút, di chuyển ngẫu nhiên sang: {action}")
        else:
            action = random.choice(moves)
            print(f" Ô sạch, di chuyển ngẫu nhiên sang: {action}")

        if action == "up": x -= 1
        elif action == "down": x += 1
        elif action == "left": y -= 1
        elif action == "right": y += 1
        

    print("Môi trường sau mô phỏng:")
    for row in environment: print(row)

if __name__ == "__main__":
    run_agent()