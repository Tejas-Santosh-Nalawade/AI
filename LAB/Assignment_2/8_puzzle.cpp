#include <bits/stdc++.h>
using namespace std;


const std::vector<int> goal_state = {1, 2, 3, 4, 5, 6, 7, 8, 0};
const std::vector<std::pair<char, int>> moves = {
    {'U', -3}, {'D', 3}, {'L', -1}, {'R', 1}
};

struct PuzzleState {
    std::vector<int> board;
    std::shared_ptr<PuzzleState> parent;
    char move;
    int depth;
    int cost;

    PuzzleState(std::vector<int> b, std::shared_ptr<PuzzleState> p, char m, int d, int c)
        : board(b), parent(p), move(m), depth(d), cost(c) {}
};

// Custom comparator for the priority queue (Min-Heap)
struct CompareState {
    bool operator()(const std::shared_ptr<PuzzleState>& a, const std::shared_ptr<PuzzleState>& b) const {
        return a->cost > b->cost;
    }
};

// Custom hash for unordered_set
struct VectorHash {
    size_t operator()(const std::vector<int>& v) const {
        std::hash<int> hasher;
        size_t seed = 0;
        for (int i : v) {
            seed ^= hasher(i) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        }
        return seed;
    }
};

void print_board(const std::vector<int>& board) {
    std::cout << "+---+---+---+\n";
    for (int row = 0; row < 9; row += 3) {
        std::string row_visual = "|";
        for (int i = 0; i < 3; ++i) {
            int tile = board[row + i];
            if (tile == 0) {
                row_visual += " " + " |";
            } else {
                row_visual += " "  + std::to_string(tile) + " |";
            }
        }
        std::cout << row_visual << "\n";
        std::cout << "+---+---+---+\n";
    }
}

int misplaced_tiles(const std::vector<int>& board) {
    int count = 0;
    for (int i = 0; i < 9; ++i) {
        if (board[i] != 0 && board[i] != goal_state[i]) count++;
    }
    return count;
}

int manhattan_distance(const std::vector<int>& board) {
    int distance = 0;
    for (int i = 0; i < 9; ++i) {
        if (board[i] != 0) {
            int x1 = i / 3, y1 = i % 3;
            int x2 = (board[i] - 1) / 3, y2 = (board[i] - 1) % 3;
            distance += std::abs(x1 - x2) + std::abs(y1 - y2);
        }
    }
    return distance;
}

int combined_heuristic(const std::vector<int>& board) {
    return misplaced_tiles(board) + manhattan_distance(board);
}

std::function<int(const std::vector<int>&)> selected_heuristic = manhattan_distance;

std::function<int(const std::vector<int>&)> select_heuristic() {
    std::cout << "\n╔═══════════════════════════════════════════════════╗\n";
    std::cout << "║          8-PUZZLE A* ALGORITHM SELECTOR           ║\n";
    std::cout << "╚═══════════════════════════════════════════════════╝\n\n" ;
    
    std::cout << "Choose a Heuristic Function:\n\n" ;
    std::cout << "  1. "  << "Misplaced Tiles (h1)\n" ;
    std::cout << "     └─ Counts tiles not in goal position\n";
    std::cout << "     └─ Less informed, faster computation\n\n";
    
    std::cout << "  2. " << "Manhattan Distance (h2)\n" ;
    std::cout << "     └─ Sum of distances to goal positions\n";
    std::cout << "     └─ More informed, optimal solution\n\n";
    
    std::cout << "  3. " << "Combined Heuristic (h1 + h2)\n" ;
    std::cout << "     └─ Uses both heuristics together\n";
    std::cout << "     └─ Most aggressive, fewest nodes expanded\n\n";
    
    while (true) {
        std::cout << "Enter your choice (1-3): " ;
        std::string choice_str;
        std::cin >> choice_str;
        try {
            int choice = std::stoi(choice_str);
            if (choice == 1) {
                std::cout << "\n✓ Selected: Misplaced Tiles Heuristic\n\n" ;
                return misplaced_tiles;
            } else if (choice == 2) {
                std::cout  << "\n✓ Selected: Manhattan Distance Heuristic\n\n" ;
                return manhattan_distance;
            } else if (choice == 3) {
                std::cout  << "\n✓ Selected: Combined Heuristic\n\n" ;
                return combined_heuristic;
            } else {
                std::cout  << "Invalid choice! Please enter 1, 2, or 3.\n" ;
            }
        } catch (...) {
            std::cout  << "Invalid input! Please enter a number (1-3).\n" ;
        }
    }
}

std::vector<int> move_tile(const std::vector<int>& board, char move_char, int blank_pos, int offset) {
    std::vector<int> new_board = board;
    int new_blank_pos = blank_pos + offset;
    std::swap(new_board[blank_pos], new_board[new_blank_pos]);
    return new_board;
}

std::shared_ptr<PuzzleState> a_star(const std::vector<int>& start_state) {
    std::priority_queue<std::shared_ptr<PuzzleState>, std::vector<std::shared_ptr<PuzzleState>>, CompareState> open_list;
    std::unordered_set<std::vector<int>, VectorHash> closed_list;

    open_list.push(std::make_shared<PuzzleState>(start_state, nullptr, '\0', 0, selected_heuristic(start_state)));

    while (!open_list.empty()) {
        auto current_state = open_list.top();
        open_list.pop();

        if (current_state->board == goal_state) {
            return current_state;
        }

        closed_list.insert(current_state->board);
        
        int blank_pos = std::distance(current_state->board.begin(), std::find(current_state->board.begin(), current_state->board.end(), 0));

        for (const auto& move_pair : moves) {
            char move = move_pair.first;
            int offset = move_pair.second;

            if (move == 'U' && blank_pos < 3) continue;
            if (move == 'D' && blank_pos > 5) continue;
            if (move == 'L' && blank_pos % 3 == 0) continue;
            if (move == 'R' && blank_pos % 3 == 2) continue;

            std::vector<int> new_board = move_tile(current_state->board, move, blank_pos, offset);

            if (closed_list.find(new_board) != closed_list.end()) continue;

            int new_depth = current_state->depth + 1;
            int new_cost = new_depth + selected_heuristic(new_board);
            
            auto new_state = std::make_shared<PuzzleState>(new_board, current_state, move, new_depth, new_cost);
            open_list.push(new_state);
        }
    }
    return nullptr;
}

void print_solution(std::shared_ptr<PuzzleState> solution) {
    std::vector<std::shared_ptr<PuzzleState>> path;
    auto current = solution;
    while (current != nullptr) {
        path.push_back(current);
        current = current->parent;
    }
    std::reverse(path.begin(), path.end());

    std::cout << "\nTotal moves: " << path.size() - 1 << "\n";
    std::cout << "Nodes expanded: " << path.size() << "\n\n";

    for (size_t i = 0; i < path.size(); ++i) {
        if (path[i]->move != '\0') {
            std::cout << "Step " << i << ": Move " << path[i]->move << "\n";
        } else {
            std::cout << "Step " << i << ": Initial State\n";
        }
        print_board(path[i]->board);
        std::cout << "\n";
    }
}

int main() {
    selected_heuristic = select_heuristic();
    std::vector<int> initial_state = {1, 2, 3, 4, 0, 5, 6, 7, 8};

    auto solution = a_star(initial_state);

    if (solution) {
        std::cout << GREEN << "\n✓ Solution Found!\n" << RESET;
        print_solution(solution);
    } else {
        std::cout << RED << "\n✗ No Solution Exists\n" << RESET;
    }
    return 0;
}