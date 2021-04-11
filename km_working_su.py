#!/usr/bin/python3.6
# Import PuLP modeler functions
from pulp import *
import sys
import pprint
from get_km import *

# All rows, columns and values within a Sudoku take values from 1 to 9
VALS = ROWS = COLS = range(1, 10)

# The boxes list is created, with the row and column index of each square in each box
Boxes = [
    [(3 * i + k + 1, 3 * j + l + 1) for k in range(3) for l in range(3)]
    for i in range(3) for j in range(3)
]

#pprint.pprint(Boxes)
#for i in range(0,9):
#    pprint.pprint(Boxes[i])
#sys.exit(33)

# The prob variable is created to contain the problem data
prob = LpProblem("Sudoku_Problem")

# The decision variables are created
choices = LpVariable.dicts("Choice", (VALS, ROWS, COLS), cat='Binary')

# We do not define an objective function since none is needed

# A constraint ensuring that only one value can be in each square is created
for r in ROWS:
    for c in COLS:
        prob += lpSum([choices[v][r][c] for v in VALS]) == 1

# standard sudoku
# The row, column and box constraints are added for each value
for v in VALS:
    for r in ROWS:
        prob += lpSum([choices[v][r][c] for c in COLS]) == 1

    for c in COLS:
        prob += lpSum([choices[v][r][c] for r in ROWS]) == 1

    for b in Boxes:
        prob += lpSum([choices[v][r][c] for (r, c) in b]) == 1, "boxes_" + str(v) + str(b)


#fields = [line.strip() for line in fh.readlines()]

data = []
fh = open(sys.argv[1], "r")
for line in fh.readlines():
    tmp = line.strip().split(",")
    if len(tmp) == 10:
        tmp2 = [ int(tmp[x].strip()) for x in range(9)]
        data.append(tmp2)

fh.close()
#pprint.pprint(data)

#sys.exit(33)
# pre-load clues with constraints , with warmstart
for r in range(9):
    for c in range(9):
        v = data[r][c]
        if v != 0:
            #print(v, r+1, c+1)
            prob += choices[v][r+1][c+1] == 1
            #choices[v][r+1][c+1].setInitialValue(1)
            #choices[v][r+1][c+1].fixValue()

# pre-load clues with constraints , original way
#for r in range(9):
#    for c in range(9):
#        v = data[r][c]
#        if v != 0:
#            #print(v, r+1, c+1)
#            prob += choices[v][r+1][c+1] == 1
#    #print()
#
#
#[[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)],
# [(1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6)],
# [(1, 7), (1, 8), (1, 9), (2, 7), (2, 8), (2, 9), (3, 7), (3, 8), (3, 9)],
#
# [(4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3), (6, 1), (6, 2), (6, 3)],
# [(4, 4), (4, 5), (4, 6), (5, 4), (5, 5), (5, 6), (6, 4), (6, 5), (6, 6)],
# [(4, 7), (4, 8), (4, 9), (5, 7), (5, 8), (5, 9), (6, 7), (6, 8), (6, 9)],
#
# [(7, 1), (7, 2), (7, 3), (8, 1), (8, 2), (8, 3), (9, 1), (9, 2), (9, 3)],
# [(7, 4), (7, 5), (7, 6), (8, 4), (8, 5), (8, 6), (9, 4), (9, 5), (9, 6)],
# [(7, 7), (7, 8), (7, 9), (8, 7), (8, 8), (8, 9), (9, 7), (9, 8), (9, 9)]]

#for i in range(0,9):
#    print("doing i = " + str(i))
#    for j in range(0,9):
#        print("doing j = " + str(j))
#        for (r,c) in [ Boxes[j][i] ]:
#           print(r,c)
##sys.exit(33)

# more constraints
# need to add rXcX cannot contain same digit
#for v in VALS:
#    for i in range(0,9):
#        prob += lpSum( [ choices[v][r][c] for (r,c) in [ Boxes[j][i] ] ] for j in range(0,9) ) == 1, "rxcx_" + str(v) + str(i)

#
#main diagonals corner to corner
for v in VALS:
    # main diag tl2br
    prob += lpSum( [choices[v][r][r] for r in range(9,0,-1) ]) == 1, "tl2br" + str(v)
    # main diag bl2tr
    prob += lpSum( [choices[v][r][10-r] for r in range(9,0,-1) ]) == 1, "bl2tr" + str(v)

# call diagonal sum constraints per designer direction(start,expected sum value)
def f2lr(val,total):
    # 2_1_2_lr
    global prob
    prob += lpSum( [ choices[v][r][c] * v for v in VALS for (r,c) in zip( range(val,10) , range(1,10-val+1) ) ]) == total, "f2lr" + str(val) + str(total)


def t2ll(val,total):
    global prob
    prob += lpSum( [ choices[v][r][c] * v for v in VALS for (r,c) in zip( range(1,val+1), range(val,0,-1) ) ]) == total, "t2ll" + str(val) + str(total)


def b2tr(val,total):
    global prob
    prob += lpSum( [ choices[v][r][c] * v for v in VALS for (r,c) in zip( range(9,val-1,-1), range(val,10) ) ]) == total, "b2tr" + str(val) + str(total)


def r2tl(val,total):
    global prob
    prob += lpSum( [ choices[v][r][c] * v for v in VALS for (r,c) in zip( range(val,0,-1), range(9,9-val,-1) ) ]) == total, "r2tl" + str(val) + str(total)

#for v in range(1,10):
#    for x in range(2,9):

##outer grey band > orthogonal neighbor
#for x in range(2,9):
#    prob += lpSum( [ v * choices[v][1][x] for v in VALS  ]) >= lpSum( [ v * choices[v][2][x] for v in VALS  ])  , "top_" + str(x)
#    prob += lpSum( [ v * choices[v][9][x] for v in VALS  ]) >= lpSum( [ v * choices[v][8][x] for v in VALS  ])  , "bot_" + str(x)
#    prob += lpSum( [ v * choices[v][x][1] for v in VALS  ]) >= lpSum( [ v * choices[v][x][2] for v in VALS  ])  , "left_" + str(x)
#    prob += lpSum( [ v * choices[v][x][9] for v in VALS  ]) >= lpSum( [ v * choices[v][x][8] for v in VALS  ])  , "right_" + str(x)

#magic square
# two diagonals
prob += lpSum(  [ v * choices[v][x][x] for v in VALS for x in range(4,7) ] ) == 15, "magic_tl2br_diag"
prob += lpSum(  [ v * choices[v][r][c] for v in VALS for (r,c) in zip(range(6,3,-1),range(4,7)) ] ) == 15, "magic_bl2tr_diag"
# rows and columns
for x in range(4,7):
    prob += lpSum(  [ v * choices[v][x][c] for v in VALS for c in range(4,7) ] ) == 15, "magic_row_" + str(x)
    prob += lpSum(  [ v * choices[v][r][x] for v in VALS for r in range(4,7) ] ) == 15, "magic_col_" + str(x)


def look_3_in(val,t=None,b=None,l=None,r=None):
    global prob
    if t is not None:
        x=str(t)
        prob += lpSum( [ choices[val][r][t] for r in range(1,4)  ]) == 1 , "l3in_t" + str(x) + str(val)
    elif b is not None:
        x=str(b)
        prob += lpSum( [ choices[val][r][b] for r in range(9,6,-1)  ]) == 1 , "l3in_b" + str(x) + str(val)
    elif l is not None:
        x=str(l)
        prob += lpSum( [ choices[val][l][c] for c in range(1,4)  ]) == 1 , "l3in_l" + str(x) + str(val)
    elif r is not None:
        x=str(r)
        prob += lpSum( [ choices[val][r][c] for c in range(9,6,-1)  ]) == 1 , "l3in_r" + str(x) + str(val)

#look_3_in(4,t=2)
#look_3_in(2,t=4)
#look_3_in(6,t=5)
#look_3_in(1,t=6)
#look_3_in(9,t=8)
#
#look_3_in(2,l=1)
#look_3_in(9,l=2)
#look_3_in(8,l=4)
#look_3_in(6,l=5)
#look_3_in(2,l=6)
#look_3_in(5,l=8)
#
#look_3_in(3,b=2)
#look_3_in(7,b=4)
#look_3_in(1,b=5)
#look_3_in(9,b=6)
#look_3_in(4,b=8)
#
#look_3_in(1,r=1)
#look_3_in(7,r=2)
#look_3_in(7,r=4)
#look_3_in(3,r=5)
#look_3_in(6,r=6)
#look_3_in(3,r=8)


# call diagonal sum constraints per designer direction(start,expected sum value)
#f2lr(5,42)
#f2lr(7,12)
#f2lr(8,15)
#t2ll(6,17)
#b2tr(4,41)
#b2tr(7,8)
#r2tl(3,20)
#r2tl(7,22)

grid = [[1] * 9 for i in range(9)]
# setup knight moves
for v in VALS:
    for r in ROWS:
        for c in COLS:
            tmp=get_km(r,c,grid)
            for (i,j) in tmp:
                prob += lpSum( [choices[v][i][j]] + [choices[v][r][c]]) <= 1 , 'km_v%1d_r%1d_c%1d_i%1d_j%1d'%( v, r, c, i, j)

# The problem data is written to an .lp file
prob.writeLP("Sudoku.lp")

# A file called sudokuout.txt is created/overwritten for writing to
sudokuout = open('sudokuout.txt','w')

#grid = [[1] * 9 for i in range(9)]
## setup knight moves
#for r in ROWS:
#    for c in COLS:
#        tmp=get_km(r,c,grid)
#        for x in tmp:
#            prob += choices[0][r][c]  


# The problem data is written to an .lp file
prob.writeLP("Sudoku.lp")

# A file called sudokuout.txt is created/overwritten for writing to
sudokuout = open('sudokuout.txt','w')

solver=PULP_CBC_CMD(msg=False,warmStart=True)

tries=0
count=0
while tries <= 3:
    tries+=1
    prob.writeLP("Sudoku.lp")
    prob.solve(solver)
    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])
    # The solution is printed if it was deemed "optimal" i.e met the constraints
    if LpStatus[prob.status] == "Optimal":
        #prob.to_json("solve.json")
        count+=1
        # The solution is written to the sudokuout.txt file
        for r in ROWS:
            if r in [1, 4, 7]:
                sudokuout.write("+-------+-------+-------+\n")
            for c in COLS:
                for v in VALS:
                    if value(choices[v][r][c]) == 1:
                        if c in [1, 4, 7]:
                            sudokuout.write("| ")
                        sudokuout.write(str(v) + " ")
                        if c == 9:
                            sudokuout.write("|\n")
        sudokuout.write("+-------+-------+-------+\n\n")
        #sys.exit(33)
        # The constraint is added that the same solution cannot be returned again
        # stores those values that have solved this. the next run will check
        # these save cells and constrain that sum on future runs is < 81
        prob += lpSum([choices[v][r][c] for v in VALS for r in ROWS for c in COLS
                       if value(choices[v][r][c]) == 1]) <= 80, "no dups_" + str(tries)
    # If a new optimal solution cannot be found, we end the program
    else:
        break
sudokuout.close()

# The location of the solutions is give to the user
print("Success on " + str(count) + " of " + str(tries) + " tries. Solutions Written to sudokuout.txt")
