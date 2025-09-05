import csv

ALGORITHMS = {
    1: "Brute force search",
    2: "CSP back-tracking search",
    3: "CSP with forward-checking and MRV heuristics",
    4: "TEST",
}


def check_args(args):
    is_valid_args = False
    if len(args) == 3:
        mode = args[1]
        try:
            mode = int(mode)
            if mode in [1, 2, 3, 4]:
                filename = args[2]
                try:
                    grid = grid_from_csv(filename)

                    if len(grid) == 9 and len(grid[0]) == 9:
                        is_valid_args = True
                except Exception:
                    pass
        except Exception:
            pass

    if not is_valid_args:
        print("ERROR: Not enough/too many/illegal input arguments.")

    return is_valid_args


def print_report(
    mode, input_grid, solution_grid, csv_filename, search_time, nodes, is_solved
):
    print("Hujare, Ameya, A20545367 solution:")
    print(f"Input File: {csv_filename}")
    print(f"Algorithm: {ALGORITHMS[mode]}\n")
    print("Input puzzle:\n")
    print_grid(input_grid)
    print()
    print(f"Number of search tree nodes generated: {nodes}")
    print(f"Search time: {search_time:.5f} seconds\n")
    if is_solved:
        print("Solved puzzle:\n")
        print_grid(solution_grid)
    else:
        print("ERROR: Sudoku puzzle has no solution.")


def get_domains(grid):
    variables = get_variables()
    domains = {}
    for var in variables:
        i, j = var
        if grid[i][j] == "X":
            domains[var] = list(range(1, 10))
        else:
            domains[var] = {int(grid[i][j])}

    return domains


def get_variables():
    return [(i, j) for i in range(9) for j in range(9)]


def get_constraints():
    variables = get_variables()
    constraints = {}
    for var in variables:
        i, j = var
        row_constraints = [(i, c) for c in range(9) if j != c]
        col_constraints = [(r, j) for r in range(9) if i != r]
        sub_i, sub_j = i // 3, j // 3
        box_constraints = []
        for r in range(sub_i * 3, (sub_i + 1) * 3):
            for c in range(sub_j * 3, (sub_j + 1) * 3):
                if (r, c) != (i, j):
                    box_constraints.append((r, c))

        constraints[var] = list(
            set(row_constraints + col_constraints + box_constraints)
        )
    return constraints


def assignment_to_grid(solution):
    grid = [[0] * 9 for i in range(9)]
    for var, value in solution.items():
        i, j = var
        grid[i][j] = value
    return grid


def print_grid(grid):
    for row in grid:
        print(" ".join(str(e) for e in row))


def grid_from_csv(filename):
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        grid = [[e for e in row] for row in reader]
    return grid


def is_valid_placement(grid, row, col, num):
    return (
        not any(num == grid[row][i] for i in range(9) if i != col)
        and not any(num == grid[i][col] for i in range(9) if i != row)
        and not any(
            num == grid[i][j]
            for i in range(3 * (row // 3), 3 * (row // 3) + 3)
            for j in range(3 * (col // 3), 3 * (col // 3) + 3)
            if (i != row) and (j != col)
        )
    )


def test_sudoku(grid):
    for row in range(9):
        for col in range(9):
            num = grid[row][col]
            if not is_valid_placement(grid, row, col, num):
                return False
    return True
