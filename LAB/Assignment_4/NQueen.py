def is_safe(board, current_row, col):
    """
    Checks if a queen can be placed at board[current_row][col].
    We only need to check the rows above the current one.
    """
    for i in range(current_row):
        if board[i] == col or abs(board[i] - col) == abs(i - current_row):
            return False
    return True

def solve_n_queens(n):
    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col      
                backtrack(row + 1)   
    solutions = []
    board = [-1] * n  
    backtrack(0)     
    return solutions

def print_solutions(solutions, n):
    for idx, sol in enumerate(solutions):
        print(f"Solution {idx + 1} (Columns: {sol}):")
        for row in range(n):
            line = ""
            for col in range(n):
                if sol[row] == col:
                    line += "Q "
                else:
                    line += ". "
            print(line)
        print()

if __name__ == "__main__":
    try:
        n = int(input("Enter the number of queens (N): "))
        if n <= 0:
            print("Please enter a positive integer greater than 0.")
        elif n == 2 or n == 3:
            print(f"For n={n}, the problem has no solution.")
        else:
            solutions = solve_n_queens(n)
            print(f"\nTotal solutions found: {len(solutions)}\n")
            print_solutions(solutions, n)
    except ValueError:
        print("Invalid input. Please enter an integer.")