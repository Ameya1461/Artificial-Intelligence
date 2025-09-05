import time
from ctypes import util

import utils
from csp import CSP


def select_unassigned_variable(csp, assignment):
    # Static Variable Ordering
    for variable in csp.variables:
        if variable not in assignment:
            return variable


def order_domain_values(csp, var, assignment):
    # domains are ordered 1-9
    return csp.domains[var]


def is_consistent(csp, var, value, assignment):
    for neighbour in csp.constraints[var]:
        if neighbour in assignment and assignment[neighbour] == value:
            return False
    return True


def backtracking_search(csp):
    # entrypoint of recursive backtracking
    return backtrack(csp, {})


def backtrack(csp, assignment):
    # Increment the counter for each generated node
    csp.nodes_generated += 1

    # Assignment is complete when all variables are assigned
    if len(assignment) == len(csp.variables):
        return assignment

    var = select_unassigned_variable(csp, assignment)

    for value in order_domain_values(csp, var, assignment):
        # check is all the contraints corresponding to the variable are satisfied
        if is_consistent(csp, var, value, assignment):
            assignment[var] = value
            result = backtrack(csp, assignment)
            if result is not None:
                return result
            del assignment[var]

    return None  # Failure


def solve_sudoku_csp_backtrack(grid):
    variables = utils.get_variables()
    domains = utils.get_domains(grid)
    constraints = utils.get_constraints()

    csp = CSP(variables, domains, constraints)
    start_time = time.time()
    solution = backtracking_search(csp)
    end_time = time.time()
    search_time = end_time - start_time

    if solution:
        is_solved = True
        grid = utils.assignment_to_grid(solution)
    else:
        is_solved = False

    return (
        is_solved,
        grid,
        csp.nodes_generated,
        search_time,
    )
