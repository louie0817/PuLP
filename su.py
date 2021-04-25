#!/usr/bin/python3.6
# Import PuLP modeler functions
from pulp import *
import re
import sys
import pprint
from get_km2 import *

import argparse

parser = argparse.ArgumentParser(description='Process some options.')
parser.add_argument('--magic', dest='magic', action='store_true')
parser.add_argument('--diagtop', dest='diagtop', action='store_true')
parser.add_argument('--diagbot', dest='diagbot', action='store_true')
parser.add_argument('--km_diff', dest='km_diff', action='store_true')
parser.add_argument('--km_parity', dest='km_parity', action='store_true')
parser.add_argument('--stop', dest='stop', action='store_true')
parser.add_argument('--tries', dest='tries', nargs=1, default=1 )
parser.add_argument('--rxcx', dest='rxcx', action='store_true')
parser.add_argument('--l2lr', dest='l2lr', action='append', nargs=2)
parser.add_argument('--t2ll', dest='t2ll', action='append', nargs=2)
parser.add_argument('--b2tr', dest='b2tr', action='append', nargs=2)
parser.add_argument('--r2tl', dest='r2tl', action='append', nargs=2)
parser.add_argument('input_file', nargs=1)
args = parser.parse_args()


if args.stop:
    TRIES=1
else:
    TRIES=3

if args.tries:
    TRIES=args.tries


#pprint.pprint(args)
#sys.exit(33)

# All rows, columns and values within a Sudoku take values from 1 to 9
VALS = ROWS = COLS = range(1, 10)

# The boxes list is created, with the row and column index of each square in each box
Boxes = [
    [(3 * i + k + 1, 3 * j + l + 1) for k in range(3) for l in range(3)]
    for i in range(3) for j in range(3)
]

pprint.pprint(Boxes)
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


#data = []
#fh = open(args.input_file[0], "r")
#for line in fh.readlines():
#    if line.startswith("#"):
#       continue
#    tmp = line.strip().split(",")
#    if len(tmp) == 10:
#        tmp2 = [ int(tmp[x].strip()) for x in range(9)]
#        data.append(tmp2)

    # do stuff

cages = dict()
arrows = dict()
data  = []
#cage_pat=re.compile('^(?P<lou>[A-Z])(?P<var>\d{1,2})')
#arrow_pat=re.compile('^(??<loua>[a-z])(?P<vara>\d{0,1})')

cage_pat=re.compile('^([A-Z])(\d{1,2})')
arrow_pat=re.compile('^([a-z])(T|\d)')

fh = open(args.input_file[0], "r")
lineno=0
for line in fh.readlines():
    if line.startswith("#"):
       continue
    tmp = line.strip().split(",")
    if len(tmp) == 10:
        lineno=lineno+1
        tmp2=[]
        for x in range(9):
            cell=tmp[x].strip()
            print("working on ", cell)
            cagefind =cage_pat.match(cell)
            arrowfind=arrow_pat.match(cell)
            pprint.pprint(arrowfind)
            if cagefind is not None:
                cage=cagefind.group(1)
                total=cagefind.group(2)
                if cage not in cages:
                    cages[cage]=dict()
                    cages[cage]['val']=total
                    cages[cage]['list']=[]
                cages[cage]['list'].append( (lineno,x+1) )
                tmp2.append(0)
            elif arrowfind is not None:
                arrow=arrowfind.group(1)
                total=arrowfind.group(2)
                try:
                    itot=int(total)
                except:
                    print("caught Exception")
                    itot=0
 
                if arrow not in arrows:
                    arrows[arrow]=dict()
                    arrows[arrow]['list']=dict()
                    if itot in range(1,10):
                        arrows[arrow]['list'][itot]=[]
                if total == 'T':
                    arrows[arrow]['totalcell']=(lineno,x+1)
                if itot in range(1,10) :
                    print(itot)
                    if itot not in arrows[arrow]['list']:
                        arrows[arrow]['list'][itot]=[]
                    arrows[arrow]['list'][itot].append( (lineno,x+1) )
                tmp2.append(0)
            else:
                tmp2.append(int(cell))
        data.append(tmp2)

# a1 , a1 , a1 ,   aT , a2 , 0 ,   0 , 0 , 0 ,

fh.close()
#pprint.pprint(data)
#pprint.pprint(cages)
#pprint.pprint(arrows)
#sys.exit(33)

# cages dict looks like this
#{'A': {'list': [(1, 1), (1, 2), (1, 3), (2, 3)], 'val': '25'},
#'B': {'list': [(9, 7), (9, 8), (9, 9)], 'val': '13'}}

if bool(cages):
    for cage in cages:
        total=int(cages[cage]['val'])
        prob += lpSum( [ choices[v][r][c] * v for v in VALS for (r,c) in cages[cage]['list'] ]  )  == total, "cage_" + cage
        # all cells in cages must be unique
        for v in VALS:
            prob += lpSum([choices[v][r][c] for (r, c) in cages[cage]['list']] ) <= 1, "cages_" + cage + str(v)
    
    
{'a': {'list': {1: [(4, 4)], 2: [(4, 2), (5, 2), (6, 2)]}, 'totalcell': (3, 3)},
 'b': {'list': {1: [(8, 4), (8, 5), (8, 6)], 2: [(6, 4)]}, 'totalcell': (7, 3)},
 'c': {'list': {1: [(4, 8), (5, 8), (6, 8)], 2: [(6, 6)]}, 'totalcell': (7, 7)},
 'd': {'list': {1: [(2, 4), (2, 5), (2, 6)], 2: [(4, 6)]}, 'totalcell': (3, 7)}}
if bool(arrows):
    for arrow in arrows:
        (i,j)=arrows[arrow]['totalcell']
        for path in arrows[arrow]['list']:
            prob += (lpSum( [ choices[v][r][c] * v for v in VALS for (r,c) in arrows[arrow]['list'][path] ]  ) - lpSum( [ choices[v][i][j] * v for v in VALS ] )) == 0, "arrow_" + arrow + "_" + str(path)


# pre-load clues with constraints , with warmstart
for r in range(9):
    for c in range(9):
        v = data[r][c]
        if v != 0:
            #print(v, r+1, c+1)
            #prob += choices[v][r+1][c+1] == 1
            choices[v][r+1][c+1].setInitialValue(1)
            choices[v][r+1][c+1].fixValue()

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

## more constraints
## need to add rXcX cannot contain same digit
if args.rxcx:
    for v in VALS:
        for i in range(0,9):
            prob += lpSum( [ choices[v][r][c] for (r,c) in [ Boxes[j][i] ] ] for j in range(0,9) ) == 1, "rxcx_" + str(v) + str(i)

#
#main diagonals corner to corner
if args.diagtop:
    for v in VALS:
        # main diag tl2br
        prob += lpSum( [choices[v][r][r] for r in range(9,0,-1) ]) == 1, "tl2br" + str(v)

if args.diagbot:
    for v in VALS:
        # main diag bl2tr
        prob += lpSum( [choices[v][r][10-r] for r in range(9,0,-1) ]) == 1, "bl2tr" + str(v)

# call diagonal sum constraints per designer direction(start,expected sum value)
def l2lr(val,total):
    # left to lower right
    global prob
    prob += lpSum( [ choices[v][r][c] * v for v in VALS for (r,c) in zip( range(val,10) , range(1,10-val+1) ) ]) == total, "l2lr" + str(val) + str(total)


def t2ll(val,total):
    # top to lower left
    global prob
    prob += lpSum( [ choices[v][r][c] * v for v in VALS for (r,c) in zip( range(1,val+1), range(val,0,-1) ) ]) == total, "t2ll" + str(val) + str(total)


def b2tr(val,total):
    # bottom to top right
    global prob
    prob += lpSum( [ choices[v][r][c] * v for v in VALS for (r,c) in zip( range(9,val-1,-1), range(val,10) ) ]) == total, "b2tr" + str(val) + str(total)


def r2tl(val,total):
    # right to lower left
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
def magic_square(box):

#[[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)],

    b=Boxes[box]

    global prob

    # two diagonals
    prob += lpSum(  [ v * choices[v][r][c] for v in VALS for (r,c) in [ b[0], b[4], b[8] ] ]) == 15, "magic_tl2br_diag" + str(box)
    prob += lpSum(  [ v * choices[v][r][c] for v in VALS for (r,c) in [ b[6], b[4], b[2] ] ]) == 15, "magic_bl2tr_diag" + str(box)

    # rows
    prob += lpSum(  [ v * choices[v][r][c] for v in VALS for (r,c) in [ b[0], b[1], b[2] ] ]) == 15, "magic_box_row" + str(box) + str(1)
    prob += lpSum(  [ v * choices[v][r][c] for v in VALS for (r,c) in [ b[3], b[4], b[5] ] ]) == 15, "magic_box_row" + str(box) + str(2)
    prob += lpSum(  [ v * choices[v][r][c] for v in VALS for (r,c) in [ b[6], b[7], b[8] ] ]) == 15, "magic_box_row" + str(box) + str(3)

    # cols
    prob += lpSum(  [ v * choices[v][r][c] for v in VALS for (r,c) in [ b[0], b[3], b[6] ] ]) == 15, "magic_box_col" + str(box) + str(1)
    prob += lpSum(  [ v * choices[v][r][c] for v in VALS for (r,c) in [ b[1], b[4], b[7] ] ]) == 15, "magic_box_col" + str(box) + str(2)
    prob += lpSum(  [ v * choices[v][r][c] for v in VALS for (r,c) in [ b[2], b[5], b[8] ] ]) == 15, "magic_box_col" + str(box) + str(3)

#magic_square(0)
#magic_square(1)
#magic_square(2)

#magic_square(3)
#magic_square(4)
#magic_square(5)

#magic_square(6)
#magic_square(7)
#magic_square(8)


#magic square
# two diagonals
#prob += lpSum(  [ v * choices[v][x][x] for v in VALS for x in range(4,7) ] ) == 15, "magic_tl2br_diag"
#prob += lpSum(  [ v * choices[v][r][c] for v in VALS for (r,c) in zip(range(6,3,-1),range(4,7)) ] ) == 15, "magic_bl2tr_diag"
## rows and columns
#for x in range(4,7):
#    prob += lpSum(  [ v * choices[v][x][c] for v in VALS for c in range(4,7) ] ) == 15, "magic_row_" + str(x)
#    prob += lpSum(  [ v * choices[v][r][x] for v in VALS for r in range(4,7) ] ) == 15, "magic_col_" + str(x)



def lessthan(r1,c1,r2,c2):
    global prob
    prob += lpSum(  [ v * choices[v][r1][c1] for v in VALS ] ) >= lpSum(  [ v * choices[v][r2][c2] for v in VALS ] ) -1 , "lessthan_" + str(r1) + str(c1) + str(r2) + str(c2)

#lessthan(2,8,1,8)



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

diagfuncs=[
"l2lr",
"t2ll",
"b2tr",
"r2tl",
]

for f in diagfuncs:
    me=getattr(args,f)
    if me:
        for x in me:
            eval(f)(int(x[0]),int(x[1]))

#mymod = dict([ (0 , 0), (1 , 1), (2 , 0), (3 , 1), (4 , 0), (5 , 1), (6 , 0), (7 , 1), (8 , 0), (9 , 1), ])
mymod = dict([ (0 , 0), (1 , 1), (2 , 2), (3 , 1), (4 , 2), (5 , 1), (6 , 2), (7 , 1), (8 , 2), (9 , 1), ])
km_seen={}
km_moves={}
km_moves=get_km()
#pprint.pprint(km_moves)
#sys.exit(33)

## setup knight moves, cache reciprocal cells
def parity(r,c):
    global prob
    for (i,j) in km_moves[(r,c)]:
        prob += lpSum([ mymod[v] * choices[v][i][j] for v in VALS ] + [ mymod[v] * choices[v][r][c] for v in VALS ]) == 3 , 'kmp_r%1d_c%1d_i%1d_j%1d'%( r, c, i, j)


if args.km_parity:
    for r in range(4,7):
        for c in range(4,7):
            parity(r,c)
    #parity(2,2)
    #parity(2,8)
    #parity(8,8)
    #parity(8,2)

## setup knight moves, cache reciprocal cells
if args.km_diff:
    for v in VALS:
        for r in ROWS:
            for c in COLS:
                for (i,j) in km_moves[(r,c)]:
                    #print("doing %d,%d,%d,%d,%d\n" % (v,r,c,i,j) )
                    if (v,r,c,i,j) not in km_seen:
                        prob += lpSum( [ choices[v][i][j] ] + [ choices[v][r][c] ] ) <= 1 , 'kmd_v%1d_r%1d_c%1d_i%1d_j%1d'%( v, r, c, i, j)
                        km_seen[(v,i,j,r,c)]=1

# The problem data is written to an .lp file
prob.writeLP("Sudoku.lp")

# A file called sudokuout.txt is created/overwritten for writing to
sudokuout = open('sudokuout.txt','w')

# The problem data is written to an .lp file
prob.writeLP("Sudoku.lp")

# A file called sudokuout.txt is created/overwritten for writing to
sudokuout = open('sudokuout.txt','w')

solver=PULP_CBC_CMD(msg=True,warmStart=True)

tries=0
count=0
while tries < int(TRIES):
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
        if args.stop:
            break
    else:
        break
sudokuout.close()

# The location of the solutions is give to the user
print("Success on " + str(count) + " of " + str(tries) + " tries. Solutions Written to sudokuout.txt")
