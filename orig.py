#!/usr/bin/python3.6
# Import PuLP modeler functions
from pulp import *

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Example_Problem", LpMaximize)

# Declare decision variables
var_x = LpVariable(name="x", lowBound=0, cat="Continuous")
var_y = LpVariable(name="y", cat="Integer")

# The objective function is added to 'prob' first
prob += var_x + 2 * var_y

# The constraints are added to 'prob'
prob += var_x == (-1) * var_y
prob += var_x <= 15
prob += var_x >= 1

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

