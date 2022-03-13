#!/usr/bin/python3.6
# Import PuLP modeler functions
from pulp import *

import numpy as np

import sys
import pprint

# Create the 'prob' variable to contain the problem data

fh = open(sys.argv[1], "r")
teams = [line.strip() for line in fh.readlines()]
fh.close()
tcount=len(teams)

fh = open(sys.argv[2], "r")
fields = [line.strip() for line in fh.readlines()]
fh.close()
fieldct=len(fields)

weekct=int(sys.argv[3]);

home=[]
home = [0 for i in range(tcount)] 
away=[]
away = [0 for i in range(tcount)] 


FIELDS=range(fieldct)
WEEKS = range(weekct)
TEAMS_A = TEAMS_H = range(tcount)

prob = LpProblem("Example_Problem")
weeks = LpVariable.dicts("w", ( WEEKS , FIELDS , TEAMS_A , TEAMS_H ),lowBound=0, upBound=1, cat="Binary")

total_games = tcount * weekct / 2
# correct
if ((tcount * weekct) % 2) == 0:
    prob += lpSum([weeks[w] for w in WEEKS]) == tcount * weekct / 2, "total games in season"
else:
    print("odd number of total games calculated, remove this check once script accounts for this")
    sys.exit(1)

if tcount % 2 != 0:
    print("team count is odd, remove this check once script accounts for this")
    #sys.exit(1)

# GAMES
total_game_upper = total_game_lower= int(weekct/2)
if weekct % 2 == 1:
    total_game_upper += 1

print("tgs upper: " + str(total_game_upper))
print("tgs lower: " + str(total_game_lower))

# FIELDS
total_field_upper = total_field_lower= int(weekct/fieldct)
total_field_upper += 1

print("tfu upper: " + str(total_field_upper))
print("tfu lower: " + str(total_field_lower))

# TODO total home games across all weeks
prob += ( lpSum([weeks[w][f][h] for w in WEEKS for f in FIELDS for h in TEAMS_H]) ) == total_games

# TODO total away games
#prob += ( lpSum([weeks[w][f][h][a] for w in WEEKS for f in FIELDS for a in TEAMS_A for h in TEAMS_H]) ) == total_games

#sys.exit(33)
#home and away counts = elastic from total_game_split
# TODO ideal is plus/minus 1
for h in range(tcount):
    prob += ( lpSum([weeks[w][f][h] for w in WEEKS for f in FIELDS]) ) <= total_game_upper
    prob += ( lpSum([weeks[w][f][h] for w in WEEKS for f in FIELDS]) ) >= total_game_lower

#ec_LHS=LpAffineExpression(lpSum([weeks[w][h] for w in WEEKS for h in TEAMS_H]))
#constraint_1 = LpConstraint(name='homegames', e=ec_LHS, sense=0 , rhs=total_game_split )
#elasticProblem_1 = constraint_1.makeElasticSubProblem(penalty=0, proportionFreeBoundList = [ 0, 1 ])
#elasticProblem_1 = constraint_1.makeElasticSubProblem(penalty=0, proportionFreeBound = .5)
#prob.extend(elasticProblem_1)


# for any given week
#in a given week, each team must be home or away
# so the sum of its row and its columns must be 1
# TODO not valid if odd number of teams.
for w in range(weekct):
    for x in range(tcount):
        prob += ( lpSum([weeks[w][f][x][a] for f in FIELDS for a in TEAMS_A]) + lpSum([weeks[w][f][h][x] for f in FIELDS for h in TEAMS_H]) ) == 1

# teams cannot play themselves
#prob += lpSum( [ weeks[w][x][x] for w in WEEKS for x in TEAMS_H ] )  == 0 , "cannot play themselves"

# no team plays another more than once
#if weekct >= (tcount/2):
for i in range(tcount):
    for j in range(tcount):
        prob += ( lpSum([weeks[w][f][i][j] for w in WEEKS for f in FIELDS]) + lpSum([weeks[w][f][j][i] for w in WEEKS for f in FIELDS]) ) <= 1, "perteam_" + str(i) + "_" + str(j)

# field constraints
# field constraints
# field constraints

#  one field usage per week
for w in range(weekct):
    for f in range(fieldct):
        prob += lpSum([weeks[w][f][h][a] for h in TEAMS_H for a in TEAMS_A]) <= 1 , "fieldperweek_" + str(w) + str(f)

# constraints field usage per team -- elastic from total_game_split
# ideal is plus/minus 1
##LOU for f in range(fieldct):
##LOU     for x in range(tcount):
##LOU    prob += ( lpSum([weeks[w][f][x][a] for w in WEEKS for a in TEAMS_A]) + lpSum([weeks[w][f][h][x] for w in WEEKS for h in TEAMS_H]) ) >= int(sys.argv[4]), "lower_field_per_team_" + str(f) + str(x)
##LOU         prob += ( lpSum([weeks[w][f][x][a] for w in WEEKS for a in TEAMS_A]) + lpSum([weeks[w][f][h][x] for w in WEEKS for h in TEAMS_H]) ) <= int(sys.argv[5]), "upper_field_per_team_" + str(f) + str(x)

# field constraints
# field constraints
# field constraints

# The problem is solved using PuLP's choice of Solver
prob.solve()

print(prob.status)
#sys.exit(33)

prob.writeLP("debug")


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
fieldspread=[[0 for f in range(fieldct)] for t in range(tcount)]

print("counts")
for w in range(weekct):
    print()
    disp=w+1
    print("week " + str(disp) )
    for f in range(fieldct):
        for h in range(tcount):
            for a in range(tcount):
                if int(value(weeks[w][f][h][a])) == 1:
                    home[h]+=1
                    away[a]+=1
                    fieldspread[a][f] += 1
                    fieldspread[h][f] += 1
                    print(teams[a] + " at " + teams[h] + " on field " + fields[f] )

pprint.pprint(fieldspread)
#sys.exit(33)

print()
print("tgs upper: " + str(total_game_upper))
print("tgs lower: " + str(total_game_lower))
for x in range(tcount):
    print(str(home[x]) + " homes games for team " + teams[x]);
    print(str(away[x]) + " away games for team " + teams[x]);
    print()

