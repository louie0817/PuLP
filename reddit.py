#!/usr/bin/python3.6
# Import PuLP modeler functions
from pulp import *


prob = LpProblem("Example_Problem", LpMinimize )

A = LpVariable("NUM_A", lowBound=0, upBound=8, cat="Integer")
B = LpVariable("NUM_B", lowBound=0, upBound=10, cat="Integer")

RATE_A=4
RATE_B=3

SHIFT=8

PAY_A=RATE_A * SHIFT
PAY_B=RATE_B * SHIFT

OUTPUT_A=25 * SHIFT
OUTPUT_B=15 * SHIFT


#objective
prob += ( ( PAY_A * A + ( OUTPUT_A * A * 0.02 * 4.0) ) + ( PAY_B * B + ( OUTPUT_B * 0.05 * 2.0) ) )

#constraint
prob += (A * OUTPUT_A + B * OUTPUT_B) >= 1800

prob.solve()

prob.writeLP("debug")

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    if ( v.varValue != 0 ):
        print(v.name, "=", v.varValue)

