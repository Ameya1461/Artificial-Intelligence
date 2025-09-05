import time

import utils
from csp import CSP


def select_unassigned_variable(csp, assignment):
    # Minimum-Remaining-Values (MRV) Variable Ordering Heuristic
    min_remaining_values = 9
    best_var = None
    for var, domain in csp.domains.items():
        if var not in assignment:
            # select variable with minimum values in the domain
            # all known values will be placed first
            if len(domain) < min_remaining_values:
                min_remaining_values = len(domain)
                best_var = var
    return best_var


def order_domain_values(csp, var, assignment):
    # domains are ordered 1-9
    return csp.domains[var]


def is_consistent(csp, var, value, assignment):
    for constrained_var in csp.constraints[var]:
        if constrained_var in assignment and assignment[constrained_var] == value:
            return False
    return True


def inference(csp, var, assignment):
    value = assignment[var]
    inferences = {}
    for constr_var in csp.constraints[var]:
        if constr_var not in assignment:
            try:
                csp.domains[constr_var].remove(value)
                inferences[constr_var] = value
            except:
                pass
            if len(csp.domains[constr_var]) == 0:
                return None
    return inferences


def backtracking_search(csp):
    # entrypoint of recursive backtracking
    return backtrack(csp, {})


def backtrack(csp, assignment):
    # Increment the counter for each generated node
    csp.nodes_generated += 1

    # Assignment is complete when all variables are assigned
    if len(assignment) == len(csp.domains):
        return assignment

    var = select_unassigned_variable(csp, assignment)

    for value in order_domain_values(csp, var, assignment):
        # check if all the contraints corresponding to the variable are satisfied
        if is_consistent(csp, var, value, assignment):
            assignment[var] = value
            inferences = inference(csp, var, assignment)
            if inferences is not None:
                result = backtrack(csp, assignment)
                if result is not None:
                    return result
                for variable, removed_value in inferences.items():
                    csp.domains[variable].append(removed_value)
            del assignment[var]

    return None  # Failure


def solve_sudoku_csp_forward_checking_mrv(grid):
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
