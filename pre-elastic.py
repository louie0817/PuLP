#!/usr/bin/python3.6
# Import PuLP modeler functions
from pulp import *

import numpy as np

import pprint

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Example_Problem")

tcount=12;
weekct=8;
fieldct=4;
slotct=2;

teams = [
"louie",
"noah",
"ted",
"zip",
"cofresi",
"marcus",
"berger",
"ken",
"gabe",
"blake",
"JJ",
"Henry",
"McCue",
"dean",
]

home=[]
home = [0 for i in range(tcount)] 
away=[]
away = [0 for i in range(tcount)] 

playct=fieldct*slotct;

FIELDS=range(fieldct)
SLOTS=range(slotct)
PLAYOPS=range(playct)

WEEKS = range(weekct)
TEAMS_A = TEAMS_H = range(tcount)

weeks = LpVariable.dicts("w", ( WEEKS , TEAMS_A , TEAMS_H ), cat="Binary")

#homegames = LpVariable.dicts("home", ( TEAMS_H ), cat="Integer")
#awaygames = LpVariable.dicts("away", ( TEAMS_A ), cat="Integer")

total_games = tcount * weekct / 2
if ((tcount * weekct) % 2) == 0:
    prob += lpSum([weeks[w] for w in WEEKS]) == tcount * weekct / 2, "total games in season"
else:
    print("odd number of total games calculated, remove this check once script accounts for this")
    sys.exit(1)

if tcount % 2 != 0:
    print("team count is odd, remove this check once script accounts for this")
    sys.exit(1)


#home and away counts = elastic from weekct/2
# TODO ideal is plus/minus 1
for h in range(tcount):
    prob += ( lpSum([weeks[w][h] for w in WEEKS]) ) == int(weekct/2)

# TODO total home games
#prob += ( lpSum([weeks[w][h] for w in WEEKS for h in TEAMS_H]) ) == total_games

# TODO total away games
#prob += ( lpSum([weeks[w][h][a] for w in WEEKS for a in TEAMS_A for h in TEAMS_H]) ) == total_games

# given week
#in a given week, each team must be home or away
# so the sum of its row and its columns must be 1
for w in range(weekct):
    for x in range(tcount):
        prob += ( lpSum([weeks[w][x][a] for a in TEAMS_A]) + lpSum([weeks[w][h][x] for h in TEAMS_H]) ) == 1

for w in range(weekct):
    for h in range(tcount):
        # dont need this constraint, see given week above.
        #prob += lpSum([weeks[w][h][a] for a in TEAMS_A]) <= 1
        prob += weeks[w][h][h] == 0
    #for a in range(tcount):
        # dont need this constraint, see given week above.
        #prob += lpSum([weeks[w][h][a] for h in TEAMS_H]) <= 1

# no team plays another more than once
for h in range(tcount):
    for a in range(tcount):
        prob += lpSum([weeks[w][h][a] for w in WEEKS]) <= 1

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
#for v in prob.variables():
#    if ( v.varValue != 0 ):
#        print(v.name, "=", v.varValue)

#print()
#for w in range(weekct):
#    for h in range(tcount):
#        for a in range(tcount):
#            print( str(int(value(weeks[w][h][a]))) + " ", end='')
#        print()
#    print("+-------+\n\n")
#
print("counts")
for w in range(weekct):
    for h in range(tcount):
        for a in range(tcount):
            if int(value(weeks[w][h][a])) == 1:
                home[h]+=1
                away[a]+=1
                #print(teams[a] + " at " + teams[h])

print()
for x in range(tcount):
    print(str(home[x]) + " homes games for team " + teams[x]);
    print(str(away[x]) + " away games for team " + teams[x]);
    print()


