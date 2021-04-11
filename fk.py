#!/usr/bin/python3.6
# Import PuLP modeler functions
from pulp import *
import sys
import pprint

from get_km2 import *

# All rows, columns and values within a Sudoku take values from 1 to 9

tmp=get_km()
pprint.pprint(tmp)

seen = {}

for v in range(1,10):
    for r in range(1,10):
        for c in range(1,10):
            for (i,j) in tmp[(r,c)]:
                if (v,r,c,i,j) in seen:
                    print("seen")
                else:
                    seen[ (v,i,j,r,c) ] = 1
                    print("not seen")

#print("%d %d %d %d" % (r,c,i,j) )
