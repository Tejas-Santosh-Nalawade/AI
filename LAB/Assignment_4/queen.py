def solve_n_queens(n):
    solutions = []
    board = [-1] * n   # board[col] = row where queen is placed

    def is_safe(col, row):
        for c in range(col):
            r = board[c]
            # Same row OR same diagonal
            if r == row or abs(r - row) == abs(c - col):
                return False
        return True

    def backtrack(col):
        if col == n:
            # All queens placed — record solution
            solutions.append(board[:])
            return
        for row in range(n):
            if is_safe(col, row):
                board[col] = row       # Place queen
                backtrack(col + 1)     # Recurse
                board[col] = -1        # Backtrack

    backtrack(0)
    return solutions

# --- Run and Display ---
n = 4
solutions = solve_n_queens(n)
print(f"Total solutions for {n}-Queens: {len(solutions)}\n")

for idx, sol in enumerate(solutions):
    print(f"Solution {idx + 1}:")
    for row in range(n):
        line = ""
        for col in range(n):
            line += " Q " if sol[col] == row else " . "
        print(line)
    print()