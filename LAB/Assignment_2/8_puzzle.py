import heapq
from termcolor import colored

class PuzzleState:
    def __init__(self, board,parent, move, depth,cost):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
    def __lt__(self, other):
        return self.cost < other.cost
    
def print_board(board):
    print("+---+---+---+")
    for row in range(0,9,3):
        row_visual = "|"
        for tile in board[row:row + 3]:
            if tile== 0:
                row_visual += f" {colored(' ','cyan')} |"
            else:
                row_visual += f" {colored(str(tile), 'yellow')} |"
        print(row_visual)
        print("+---+---+---+")

goal_state = [1,2,3,4,5,6,7,8,0]

moves = {
    'U': -3,
    'D': 3,
    'L':-1,
    'R':1
}


# Heuristic Function 1: Misplaced Tiles (h1)
def misplaced_tiles(board):
    """
    Counts the number of tiles that are not in their correct position.
    This heuristic is admissible but less informed than Manhattan distance.
    """
    count = 0
    for i in range(9):
        if board[i] != 0 and board[i] != goal_state[i]:
            count += 1
    return count


# Heuristic Function 2: Manhattan Distance (h2)
def manhattan_distance(board):
    """
    Calculates the sum of Manhattan distances of all tiles from their goal positions.
    This heuristic is admissible and more informed than misplaced tiles.
    """
    distance = 0
    for i in range(9):
        if board[i] != 0:
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(board[i] - 1, 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


# Heuristic Function 3: Combined Heuristic (h1 + h2)
def combined_heuristic(board):
    """
    Combines misplaced tiles and Manhattan distance.
    This provides a more aggressive heuristic estimate.
    """
    return misplaced_tiles(board) + manhattan_distance(board)


# Global variable to store selected heuristic
selected_heuristic = None

def heuristic(board):
    """Wrapper function that calls the selected heuristic"""
    if selected_heuristic is None:
        return manhattan_distance(board)
    return selected_heuristic(board)


def select_heuristic():
    """
    Interactive menu to select which heuristic algorithm to use
    """
    print(colored("\n╔═══════════════════════════════════════════════════╗", "cyan"))
    print(colored("║          8-PUZZLE A* ALGORITHM SELECTOR           ║", "cyan"))
    print(colored("╚═══════════════════════════════════════════════════╝\n", "cyan"))
    
    print(colored("Choose a Heuristic Function:\n", "yellow"))
    print("  1. " + colored("Misplaced Tiles (h1)", "green"))
    print("     └─ Counts tiles not in goal position")
    print("     └─ Less informed, faster computation\n")
    
    print("  2. " + colored("Manhattan Distance (h2)", "green"))
    print("     └─ Sum of distances to goal positions")
    print("     └─ More informed, optimal solution\n")
    
    print("  3. " + colored("Combined Heuristic (h1 + h2)", "green"))
    print("     └─ Uses both heuristics together")
    print("     └─ Most aggressive, fewest nodes expanded\n")
    
    while True:
        try:
            choice = input(colored("Enter your choice (1-3): ", "yellow"))
            choice = int(choice)
            if choice == 1:
                print(colored("\n✓ Selected: Misplaced Tiles Heuristic\n", "green"))
                return misplaced_tiles
            elif choice == 2:
                print(colored("\n✓ Selected: Manhattan Distance Heuristic\n", "green"))
                return manhattan_distance
            elif choice == 3:
                print(colored("\n✓ Selected: Combined Heuristic\n", "green"))
                return combined_heuristic
            else:
                print(colored("Invalid choice! Please enter 1, 2, or 3.", "red"))
        except ValueError:
            print(colored("Invalid input! Please enter a number (1-3).", "red"))


# Heuristic Function using Move Tile Function 

def move_tile(board, move, blank_pos):
    new_board = board[:]
    new_blank_pos = blank_pos + moves[move]
    new_board[blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[blank_pos]
    return new_board



def a_star(start_state):
    open_list= []
    closed_list = set()
    heapq.heappush(open_list,PuzzleState(start_state, None, None, 0 , heuristic(start_state)))

    while(open_list):
        current_state = heapq. heappop(open_list)

        if current_state.board == goal_state:
            return current_state
        
        closed_list.add(tuple(current_state.board))
        blank_pos = current_state.board.index(0)

        for move in moves:
            if move =='U' and blank_pos < 3:
                continue
            if move == 'D' and blank_pos > 5:
                continue
            if move == 'L' and blank_pos%3 == 0:
                continue
            if move == 'R' and blank_pos % 3 == 2:
                continue
            
            new_board = move_tile(current_state.board, move , blank_pos)

            if tuple(new_board) in closed_list:
                continue

            new_state= PuzzleState(new_board, current_state, move , current_state.depth + 1,
                                  current_state.depth + 1 + heuristic(new_board))
            heapq.heappush(open_list, new_state)

    return None


def print_solution(solution): 
    path = []
    current = solution
    while current:
        path.append(current)
        current = current.parent
    path.reverse()

    print(f"\nTotal moves: {len(path) - 1}")
    print(f"Nodes expanded: {len(path)}\n")
    
    for i, step in enumerate(path):
        if step.move:
            print(f"Step {i}: Move {step.move}")
        else:
            print(f"Step {i}: Initial State")
        print_board(step.board)
        print()

# Let user select heuristic algorithm
def main():
    global selected_heuristic
    selected_heuristic = select_heuristic()

    initial_state  = [1,2,3,4,0,5,6,7,8]

    solution = a_star(initial_state)

    if solution:
        print(colored("\n✓ Solution Found!", "green"))
        print_solution(solution)
    else:
        print(colored("\n✗ No Solution Exists", "red"))

if __name__ == "__main__":
    main()
