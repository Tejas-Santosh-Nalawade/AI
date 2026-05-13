import java.util.*;
import java.util.function.Function;

public class PuzzleAStar {
    
    // ANSI Color Codes
    public static final String CYAN = "\033[36m";
    public static final String YELLOW = "\033[33m";
    public static final String GREEN = "\033[32m";
    public static final String RED = "\033[31m";
    public static final String RESET = "\033[0m";

    static final List<Integer> goal_state = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 0);
    
    static class MovePair {
        char direction;
        int offset;
        MovePair(char direction, int offset) {
            this.direction = direction;
            this.offset = offset;
        }
    }

    static final MovePair[] moves = {
        new MovePair('U', -3), new MovePair('D', 3), 
        new MovePair('L', -1), new MovePair('R', 1)
    };

    static class PuzzleState implements Comparable<PuzzleState> {
        List<Integer> board;
        PuzzleState parent;
        char move;
        int depth;
        int cost;

        public PuzzleState(List<Integer> board, PuzzleState parent, char move, int depth, int cost) {
            this.board = board;
            this.parent = parent;
            this.move = move;
            this.depth = depth;
            this.cost = cost;
        }

        @Override
        public int compareTo(PuzzleState other) {
            return Integer.compare(this.cost, other.cost);
        }
    }

    public static void print_board(List<Integer> board) {
        System.out.println("+---+---+---+");
        for (int row = 0; row < 9; row += 3) {
            StringBuilder row_visual = new StringBuilder("|");
            for (int i = 0; i < 3; i++) {
                int tile = board.get(row + i);
                if (tile == 0) {
                    row_visual.append(" ").append(CYAN).append(" ").append(RESET).append(" |");
                } else {
                    row_visual.append(" ").append(YELLOW).append(tile).append(RESET).append(" |");
                }
            }
            System.out.println(row_visual.toString());
            System.out.println("+---+---+---+");
        }
    }

    public static int misplaced_tiles(List<Integer> board) {
        int count = 0;
        for (int i = 0; i < 9; i++) {
            if (board.get(i) != 0 && !board.get(i).equals(goal_state.get(i))) {
                count++;
            }
        }
        return count;
    }

    public static int manhattan_distance(List<Integer> board) {
        int distance = 0;
        for (int i = 0; i < 9; i++) {
            if (board.get(i) != 0) {
                int x1 = i / 3, y1 = i % 3;
                int x2 = (board.get(i) - 1) / 3, y2 = (board.get(i) - 1) % 3;
                distance += Math.abs(x1 - x2) + Math.abs(y1 - y2);
            }
        }
        return distance;
    }

    public static int combined_heuristic(List<Integer> board) {
        return misplaced_tiles(board) + manhattan_distance(board);
    }

    static Function<List<Integer>, Integer> selected_heuristic = PuzzleAStar::manhattan_distance;

    public static Function<List<Integer>, Integer> select_heuristic() {
        Scanner scanner = new Scanner(System.in);
        System.out.println(CYAN + "\n╔═══════════════════════════════════════════════════╗");
        System.out.println("║          8-PUZZLE A* ALGORITHM SELECTOR           ║");
        System.out.println("╚═══════════════════════════════════════════════════╝\n" + RESET);
        
        System.out.println(YELLOW + "Choose a Heuristic Function:\n" + RESET);
        System.out.println("  1. " + GREEN + "Misplaced Tiles (h1)" + RESET);
        System.out.println("     └─ Counts tiles not in goal position");
        System.out.println("     └─ Less informed, faster computation\n");
        
        System.out.println("  2. " + GREEN + "Manhattan Distance (h2)" + RESET);
        System.out.println("     └─ Sum of distances to goal positions");
        System.out.println("     └─ More informed, optimal solution\n");
        
        System.out.println("  3. " + GREEN + "Combined Heuristic (h1 + h2)" + RESET);
        System.out.println("     └─ Uses both heuristics together");
        System.out.println("     └─ Most aggressive, fewest nodes expanded\n");
        
        while (true) {
            System.out.print(YELLOW + "Enter your choice (1-3): " + RESET);
            try {
                int choice = Integer.parseInt(scanner.nextLine());
                if (choice == 1) {
                    System.out.println(GREEN + "\n✓ Selected: Misplaced Tiles Heuristic\n" + RESET);
                    return PuzzleAStar::misplaced_tiles;
                } else if (choice == 2) {
                    System.out.println(GREEN + "\n✓ Selected: Manhattan Distance Heuristic\n" + RESET);
                    return PuzzleAStar::manhattan_distance;
                } else if (choice == 3) {
                    System.out.println(GREEN + "\n✓ Selected: Combined Heuristic\n" + RESET);
                    return PuzzleAStar::combined_heuristic;
                } else {
                    System.out.println(RED + "Invalid choice! Please enter 1, 2, or 3." + RESET);
                }
            } catch (NumberFormatException e) {
                System.out.println(RED + "Invalid input! Please enter a number (1-3)." + RESET);
            }
        }
    }

    public static List<Integer> move_tile(List<Integer> board, char move, int blank_pos, int offset) {
        List<Integer> new_board = new ArrayList<>(board);
        int new_blank_pos = blank_pos + offset;
        Collections.swap(new_board, blank_pos, new_blank_pos);
        return new_board;
    }

    public static PuzzleState a_star(List<Integer> start_state) {
        PriorityQueue<PuzzleState> open_list = new PriorityQueue<>();
        Set<List<Integer>> closed_list = new HashSet<>();

        open_list.add(new PuzzleState(start_state, null, '\0', 0, selected_heuristic.apply(start_state)));

        while (!open_list.isEmpty()) {
            PuzzleState current_state = open_list.poll();

            if (current_state.board.equals(goal_state)) {
                return current_state;
            }

            closed_list.add(current_state.board);
            int blank_pos = current_state.board.indexOf(0);

            for (MovePair m : moves) {
                if (m.direction == 'U' && blank_pos < 3) continue;
                if (m.direction == 'D' && blank_pos > 5) continue;
                if (m.direction == 'L' && blank_pos % 3 == 0) continue;
                if (m.direction == 'R' && blank_pos % 3 == 2) continue;

                List<Integer> new_board = move_tile(current_state.board, m.direction, blank_pos, m.offset);

                if (closed_list.contains(new_board)) continue;

                int new_depth = current_state.depth + 1;
                int new_cost = new_depth + selected_heuristic.apply(new_board);
                
                PuzzleState new_state = new PuzzleState(new_board, current_state, m.direction, new_depth, new_cost);
                open_list.add(new_state);
            }
        }
        return null;
    }

    public static void print_solution(PuzzleState solution) {
        List<PuzzleState> path = new ArrayList<>();
        PuzzleState current = solution;
        while (current != null) {
            path.add(current);
            current = current.parent;
        }
        Collections.reverse(path);

        System.out.println("\nTotal moves: " + (path.size() - 1));
        System.out.println("Nodes expanded: " + path.size() + "\n");

        for (int i = 0; i < path.size(); i++) {
            if (path.get(i).move != '\0') {
                System.out.println("Step " + i + ": Move " + path.get(i).move);
            } else {
                System.out.println("Step " + i + ": Initial State");
            }
            print_board(path.get(i).board);
            System.out.println();
        }
    }

    public static void main(String[] args) {
        selected_heuristic = select_heuristic();
        List<Integer> initial_state = Arrays.asList(1, 2, 3, 4, 0, 5, 6, 7, 8);

        PuzzleState solution = a_star(initial_state);

        if (solution != null) {
            System.out.println(GREEN + "\n✓ Solution Found!" + RESET);
            print_solution(solution);
        } else {
            System.out.println(RED + "\n✗ No Solution Exists" + RESET);
        }
    }
}