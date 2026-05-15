import random
class VacuumAgent:
    def __init__(self, start_x, start_y, grid_width, grid_height):
        self.x = start_x
        self.y = start_y
        self.width = grid_width
        self.height = grid_height

        self.model = [[None for _ in range(grid_height)] for _ in range(grid_width)]
    def update_state(self, current_status):
        self.model[self.x][self.y] = current_status
    
    def choose_action(self, current_status):
        self.update_state(current_status)


        if current_status == "Dirty":
            return "Suck"
        
        possible_moves = []
        
        if self.y > 0:
            possible_moves.append(("Up", self.x, self.y - 1))
        if self.y < self.height - 1:
            possible_moves.append(("DOWN", self.x, self.y +1))
        if self.x > 0:
            possible_moves.append(("LEFT", self.x - 1, self.y))
        if self.x < self.width - 1 :
            possible_moves.append(("RIGHT", self.x + 1, self.y))

        best_moves = []
        for move, nx, ny in possible_moves:
            if self.model[nx][ny] != "Clean":
                best_moves.append(move)

        if len(best_moves) == 0:
            best_moves = [move[0] for move in possible_moves]

        chosen_move = random.choice(best_moves)

        if chosen_move == "Up": self.y -= 1
        elif chosen_move == "Down": self.y += 1
        elif chosen_move == "Left": self.x -= 1
        elif chosen_move == "Right": self.x += 1
        return chosen_move
if __name__ == "__main__":
    world = [
        ["Dirty", "Clean", "Dirty"],
        ["Clean", "Dirty", "Clean"],
        ["Dirty", "Clean", "Dirty"]
    ]
    agent = VacuumAgent(start_x=0, start_y=0, grid_width=3, grid_height=3)
    print("Bat dau hut bui")
    for step in range(10):
        current_status = world[agent.x][agent.y]
        
        print(f"\n[Bước {step+1}] Robot đang ở vị trí ({agent.x}, {agent.y}). Trạng thái ô: {current_status}")
        
        action = agent.choose_action(current_status)
        print(f"-> Robot quyết định hành động: {action}")

        if action == "Suck":
            world[agent.x][agent.y] = "Clean"
