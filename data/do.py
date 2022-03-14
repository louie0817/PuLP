#!/usr/bin/python3.6
# Import PuLP modeler functions
from pulp import *

#import numpy as np

import sys
from pprint import pprint
from itertools import product

# Create the 'prob' variable to contain the problem data

with open(sys.argv[1], "r") as fh:
    teams = [line.strip() for line in fh.readlines()]
tcount=len(teams)

with open(sys.argv[2], "r") as fh:
    fieldo = [line.strip() for line in fh.readlines()]
fieldoct=len(fieldo)

with open(sys.argv[3], "r") as fh:
    times = [line.strip() for line in fh.readlines()]
timesct=len(times)

fields=[]
for f,t in product(fieldo,times):
    #print(f"{f}_{t}")
    fields.append(f"{f}_{t}")
fieldct=len(fields)
gamect=fieldct

weekct=int(sys.argv[4]);

weekly1=tcount/2
weekly2=fieldoct * timesct
weekly3=fieldct
if weekly1 != weekly2 or weekly2 != weekly3:
    print(f"ERROR calculated games per week differs from teams/2")
    exit(1)

print(f"week ct {weekct}")
print(f"fields only {fieldoct}")
print(f"times only {timesct}")

print(f"team count {tcount}")
print(f"fields {fieldct}")
print(f"game ct {gamect}")
print(f"weekly1 ct {weekly1}")
print(f"weekly2 ct {weekly2}")
print(f"weekly3 ct {weekly3}")




home=[]
home = [0 for i in range(tcount)] 
away=[]
away = [0 for i in range(tcount)] 

field_alloc=dict()
time_alloc=dict()

fh = open(sys.argv[7], "r")
week_names = [line.strip() for line in fh.readlines()]
fh.close()

week_name_ct=len(week_names)
if weekct != week_name_ct:
    print(f"ERROR count of week names {week_name_ct} differs from week arg {weekct}")
    exit(1)


FIELDSO=range(fieldoct)
TIMES=range(timesct)
WEEKS = range(weekct)
TEAMS_A = TEAMS_H = range(tcount)

FIELDS=range(fieldct)

prob = LpProblem("Example_Problem")
weeks = LpVariable.dicts("w", ( WEEKS , FIELDSO, TIMES , TEAMS_A , TEAMS_H ),lowBound=0, upBound=1, cat="Binary")

total_games = tcount * weekct / 2
# correct
if ((tcount * weekct) % 2) == 0:
    prob += lpSum([weeks[w] for w in WEEKS]) == total_games , "total games in season"
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
print()
print()
print()

#lou
# FIELDS
total_field_upper = total_field_lower = int(weekct/fieldoct)
print(f"tfu total: {total_field_upper}")
total_field_upper += int(sys.argv[5])
#total_field_lower -= int(sys.argv[5])
print("tfu upper: " + str(total_field_upper))
print("tfu lower: " + str(total_field_lower))

# TIMES
total_times_upper = total_times_lower= int(weekct/timesct)
#total_times_upper += int(sys.argv[6])
#total_times_lower -= int(sys.argv[6])


print("ttu upper: " + str(total_times_upper))
print("ttu lower: " + str(total_times_lower))


# TODO total home games across all weeks
#DUP prob += ( lpSum([weeks[w][f][t][h][a] for w in WEEKS for f in FIELDSO for t in TIMES for h in TEAMS_H for a in TEAMS_A]) ) == total_games, "total_games_2"

#home and away counts = elastic from total_game_split
# TODO ideal is plus/minus 1
for h in range(tcount):
    prob += ( lpSum([weeks[w][f][t][h] for w in WEEKS for f in FIELDSO for t in TIMES]) ) <= total_game_upper
    prob += ( lpSum([weeks[w][f][t][h] for w in WEEKS for f in FIELDSO for t in TIMES]) ) >= total_game_lower
    pass

#ec_LHS=LpAffineExpression(lpSum([weeks[w][h] for w in WEEKS for h in TEAMS_H]))
#constraint_1 = LpConstraint(name='homegames', e=ec_LHS, sense=0 , rhs=total_game_split )
#elasticProblem_1 = constraint_1.makeElasticSubProblem(penalty=0, proportionFreeBoundList = [ 0, 1 ])
#elasticProblem_1 = constraint_1.makeElasticSubProblem(penalty=0, proportionFreeBound = .5)
#prob.extend(elasticProblem_1)


# FOR ANY GIVEN WEEK

# in a given week, each team must be home or away
# so the sum of its home/away row and its columns must be 1
# TODO not valid if odd number of teams.
for w in range(weekct):
    for x in range(tcount):
        prob += ( lpSum([weeks[w][f][t][x][a] for f in FIELDSO for t in TIMES for a in TEAMS_A]) + lpSum([weeks[w][f][t][h][x] for f in FIELDSO for t in TIMES for h in TEAMS_H]) ) == 1, f"team_games_per_week_{w}_{x}"
        pass

# total fields must be weekly1/fieldso 6/3=2
for w in range(weekct):
    for f in range(fieldoct):
        prob += ( lpSum([weeks[w][f][t][h] for t in TIMES for h in TEAMS_H ]) ) == (weekly1/fieldoct), f"per_week_field_{w}_{f}"
        pass

# total times must be weekly1/times 6/2=3
for w in range(weekct):
    for t in range(timesct):
        prob += ( lpSum([weeks[w][f][t][h] for f in FIELDSO for h in TEAMS_H ]) ) == (weekly1/timesct), f"per_week_time_{w}_{t}"

# each field x time tuple, once per week
for w in range(weekct):
    for f in range(fieldoct):
        for t in range(timesct):
            prob += ( lpSum([weeks[w][f][t][h] for h in TEAMS_H ]) ) == 1 , f"per_week_field_and_time_tuple_{w}_{f}_{t}"


# teams cannot play themselves
#prob += lpSum( [ weeks[w][x][x] for w in WEEKS for x in TEAMS_H ] )  == 0 , "cannot play themselves"

# no team plays another more than once
#if weekct >= (tcount/2):
for i in range(tcount):
    for j in range(tcount):
        prob += ( lpSum([weeks[w][f][t][i][j] for w in WEEKS for f in FIELDSO for t in TIMES]) + lpSum([weeks[w][f][t][j][i] for w in WEEKS for f in FIELDSO for t in TIMES]) ) <= 1, f"perteam_{i}_{j}"
        pass

# field constraints
# field constraints
# field constraints

#  one field usage per week
for w in range(weekct):
    for f in range(fieldoct):
        #LOU  prob += lpSum([weeks[w][f][t][h][a] for h in TEAMS_H for a in TEAMS_A]) <= 1 , "fieldperweek_" + str(w) + str(f) + str(t)
        #prob += lpSum([weeks[w][f][t][h][a] for t in TIMES for h in TEAMS_H for a in TEAMS_A]) <= 4 , "fieldperweek_" + str(w) + str(f)
        pass

#  one field usage per week
for w in range(weekct):
    for t in range(timesct):
        #lou prob += lpSum([weeks[w][f][t][h][a] for h in TEAMS_H for a in TEAMS_A]) <= 1 , "fieldperweek_" + str(w) + str(f) + str(t)
        #prob += lpSum([weeks[w][f][t][h][a] for f in FIELDSO for h in TEAMS_H for a in TEAMS_A]) == 5 , "timesperweek_" + str(w) + str(t)
        pass

# constraints field usage per team -- elastic from total_game_split
# ideal is plus/minus 1
for f in range(fieldoct):
    for x in range(tcount):
        prob += ( lpSum([weeks[w][f][t][x][a] for w in WEEKS for t in TIMES for a in TEAMS_A]) + lpSum([weeks[w][f][t][h][x] for w in WEEKS for t in TIMES for h in TEAMS_H]) ) >= total_field_lower, f"lower_field_per_team_{f}_{x}"
        prob += ( lpSum([weeks[w][f][t][x][a] for w in WEEKS for t in TIMES for a in TEAMS_A]) + lpSum([weeks[w][f][t][h][x] for w in WEEKS for t in TIMES for h in TEAMS_H]) ) <= total_field_upper, f"upper_field_per_team_{f}_{x}"
        pass

for t in range(timesct):
    for x in range(tcount):
        prob += ( lpSum([weeks[w][f][t][x][a] for w in WEEKS for f in FIELDSO for a in TEAMS_A]) + lpSum([weeks[w][f][t][h][x] for w in WEEKS for f in FIELDSO for h in TEAMS_H]) ) >= total_times_lower , f"lower_times_per_team_{t}_{x}"
        prob += ( lpSum([weeks[w][f][t][x][a] for w in WEEKS for f in FIELDSO for a in TEAMS_A]) + lpSum([weeks[w][f][t][h][x] for w in WEEKS for f in FIELDSO for h in TEAMS_H]) ) <= total_times_upper , f"upper_times_per_team_{t}_{x}"

# field constraints
# field constraints
# field constraints

# The problem is solved using PuLP's choice of Solver
ret=prob.solve()

print(prob.status)
#sys.exit(33)

prob.writeLP("debug")

print("return val")
print(ret)
if ret == -1:
    exit(1)

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
fieldspread=[[0 for f in range(fieldoct)] for t in range(tcount)]

csv = open(sys.argv[8],"w")
csv.write(f"Date,Start Time,Field,Home Team,Away Team\n")
print("counts")
for w in range(weekct):
    print()
    name=week_names[w]
    print("LOU week " + name )
    for f in range(fieldoct):
        for t in range(timesct):
            for h in range(tcount):
                for a in range(tcount):
                    if int(value(weeks[w][f][t][h][a])) == 1:
                        home[h]+=1
                        away[a]+=1

                        field_alloc.setdefault(h,{})
                        field_alloc.setdefault(a,{})
                        field_alloc[h].setdefault(f,0)
                        field_alloc[a].setdefault(f,0)
                        field_alloc[h][f] += 1
                        field_alloc[a][f] += 1

                        time_alloc.setdefault(h,{})
                        time_alloc.setdefault(a,{})
                        time_alloc[h].setdefault(t,0)
                        time_alloc[a].setdefault(t,0)
                        time_alloc[h][t] += 1
                        time_alloc[a][t] += 1

                        fieldspread[a][f] += 1
                        fieldspread[h][f] += 1
                        venue=fieldo[f]
                        tod=times[t]
                        home_team=teams[h]
                        away_team=teams[a]
                        print(f"{away_team} at {home_team} on field {venue} @ {tod}")
                        csv.write(f"{name},{tod},{venue},{home_team},{away_team}\n")
    csv.write("\n")

csv.close()

#for w in range(weekct):
#    for f in range(fieldoct):
#        for t in range(timesct):
#            for h in range(tcount):
#                for a in range(tcount):
#                    if int(value(weeks[w][f][t][h][a])) == 1:
#                        print(f"true w:{w} f:{f} t:{t} -- h:{h}_a:{a}")
#
#pprint(field_alloc)
#pprint(time_alloc)
#exit(33)

#pprint("fspread")
#pprint(fieldspread)

print()
print("tgs upper: " + str(total_game_upper))
print("tgs lower: " + str(total_game_lower))
for x in range(tcount):
    print(str(field_alloc[x].values()) + " field/slot allocation team " + teams[x]);
    print(str(time_alloc[x].values()) + " time/slot allocation team " + teams[x]);
    print(str(home[x]) + " home games for team " + teams[x]);
    print(str(away[x]) + " away games for team " + teams[x]);
    print()

sys.exit(33)
pprint(fieldspread)

