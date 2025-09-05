class CSP:
    # Class for representing the sudoku puzzle as CSP
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.nodes_generated = 0
