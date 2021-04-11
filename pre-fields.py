#!/usr/bin/python3.6
# Import PuLP modeler functions
from pulp import *

import numpy as np

import pprint

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Example_Problem")

tcount=4;
weekct=3;

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


WEEKS = range(weekct)
TEAMS_A = TEAMS_H = range(tcount)
F=range(3)

weeks = LpVariable.dicts("w", ( WEEKS , TEAMS_A , TEAMS_H ), cat="Binary")

total_games = tcount * weekct / 2
if ((tcount * weekct) % 2) == 0:
    prob += lpSum([weeks[w] for w in WEEKS]) == tcount * weekct / 2, "total games in season"
else:
    print("odd number of total games calculated, remove this check once script accounts for this")
    sys.exit(1)

if tcount % 2 != 0:
    print("team count is odd, remove this check once script accounts for this")
    sys.exit(1)

total_game_upper = total_game_lower= int(weekct/2)
if weekct % 2 == 1:
    total_game_upper += 1

print("tgs upper: " + str(total_game_upper))
print("tgs lower: " + str(total_game_lower))
#home and away counts = elastic from total_game_split
# TODO ideal is plus/minus 1
for h in range(tcount):
    prob += ( lpSum([weeks[w][h] for w in WEEKS]) ) <= total_game_upper
for h in range(tcount):
    prob += ( lpSum([weeks[w][h] for w in WEEKS]) ) >= total_game_lower
#ec_LHS=LpAffineExpression(lpSum([weeks[w][h] for w in WEEKS for h in TEAMS_H]))
#constraint_1 = LpConstraint(name='homegames', e=ec_LHS, sense=0 , rhs=total_game_split )
#elasticProblem_1 = constraint_1.makeElasticSubProblem(penalty=0, proportionFreeBoundList = [ 0, 1 ])
#elasticProblem_1 = constraint_1.makeElasticSubProblem(penalty=0, proportionFreeBound = .5)
#prob.extend(elasticProblem_1)

# TODO total home games
prob += ( lpSum([weeks[w][h] for w in WEEKS for h in TEAMS_H]) ) == total_games

# TODO total away games
prob += ( lpSum([weeks[w][h][a] for w in WEEKS for a in TEAMS_A for h in TEAMS_H]) ) == total_games

# for any given week
#in a given week, each team must be home or away
# so the sum of its row and its columns must be 1
# TODO not valid if odd number of teams.
for w in range(weekct):
    for x in range(tcount):
        prob += ( lpSum([weeks[w][x][a] for a in TEAMS_A]) + lpSum([weeks[w][h][x] for h in TEAMS_H]) ) == 1

# teams cannot play themselves
prob += lpSum( [ weeks[w][x][x] for w in WEEKS for x in TEAMS_H ] )  == 0 , "cannot play themselves"

# no team plays another more than once
#if weekct >= (tcount/2):
for i in range(tcount):
    for j in range(tcount):
        prob += ( lpSum([weeks[w][i][j] for w in WEEKS]) + lpSum([weeks[w][j][i] for w in WEEKS]) ) <= 1, "perteam_" + str(i) + "_" + str(j)

# The problem is solved using PuLP's choice of Solver
prob.solve()

prob.writeLP("foo")

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
    print("week " + str(w))
    for h in range(tcount):
        for a in range(tcount):
            if int(value(weeks[w][h][a])) == 1:
                home[h]+=1
                away[a]+=1
                print(teams[a] + " at " + teams[h])


print()
print("tgs upper: " + str(total_game_upper))
print("tgs lower: " + str(total_game_lower))
for x in range(tcount):
    print(str(home[x]) + " homes games for team " + teams[x]);
    print(str(away[x]) + " away games for team " + teams[x]);
    print()


fieldct=4;
slotct=2;
playct=fieldct*slotct;

FIELDS=range(fieldct)
SLOTS=range(slotct)
PLAYOPS=range(playct)

#usage = LpProblem("Example_Problem")
#assign = LpVariable.dicts("games", ( GAMES , PLAYOPS ), lowBound=3, upBound=3, cat=LpInteger)
