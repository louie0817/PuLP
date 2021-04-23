#!/usr/bin/python3.6
# Import PuLP modeler functions
from pulp import *
import sys
import pprint

from get_km3 import *

# All rows, columns and values within a Sudoku take values from 1 to 9

tmp=get_km()
pprint.pprint(tmp)

