import csv
import sys
import time

import utils
from brute_force import solve_sudoku_brute_force
from csp_backtrack import solve_sudoku_csp_backtrack
from csp_fc_mrv import solve_sudoku_csp_forward_checking_mrv

ALGORITHMS = {
    1: "Brute force search",
    2: "CSP back-tracking search",
    3: "CSP with forward-checking and MRV heuristics",
    4: "TEST",
}


def solve_sudoku(mode, grid):
    start_time = time.time()

    if mode == 1:
        output = solve_sudoku_brute_force(grid)
    elif mode == 2:
        output = solve_sudoku_csp_backtrack(grid)
    elif mode == 3:
        output = solve_sudoku_csp_forward_checking_mrv(grid)

    is_solved, grid, n_nodes, search_time = output
    end_time = time.time()
    search_time = end_time - start_time

    return is_solved, grid, n_nodes, search_time


if __name__ == "__main__":
    args = sys.argv
    valid_args = utils.check_args(args)

    if valid_args:
        mode = int(args[1])
        filename = args[2]
        puzzle_grid = utils.grid_from_csv(filename)
        input_puzzle_grid = puzzle_grid.copy()

        if mode in [1, 2, 3]:
            is_solved, solution, n_nodes, total_time = solve_sudoku(mode, puzzle_grid)
            # ==================== Changed ===============================
            with open(f"{filename.split('.')[0]}_solution.csv", "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(solution)
            # ==================== Changed ===============================
            utils.print_report(
                mode,
                input_puzzle_grid,
                solution,
                filename,
                total_time,
                n_nodes,
                is_solved,
            )

        else:
            valid_sudoku = utils.test_sudoku(puzzle_grid)
            print("Hujare, Ameya, A20545367 solution:")
            print(f"Input File: {filename}")
            print(f"Algorithm: {ALGORITHMS[mode]}\n")
            print("Input puzzle:\n")
            utils.print_grid(puzzle_grid)
            print()
            if valid_sudoku:
                print("This is a valid, solved, Sudoku puzzle.")
            else:
                print("ERROR: This is NOT a solved Sudoku puzzle.")
