
import sys
import pprint

def get_km(row,column, grid):
    i,j = row, column
    solutionMoves = []
    try:
        temp = grid[i + 1][j - 2]
        solutionMoves.append([i + 1, j - 2])
    except:
        pass
    try:
        temp = grid[i + 2][j - 1]
        solutionMoves.append([i + 2, j - 1])
    except:
        pass
    try:
        temp = grid[i + 2][j + 1]
        solutionMoves.append([i + 2, j + 1])
    except:
        pass
    try:
       temp = grid[i + 1][j + 2]
       solutionMoves.append([i + 1, j + 2])
    except:
        pass
    try:
        temp = grid[i - 1][j + 2]
        solutionMoves.append([i - 1, j + 2])
    except:
        pass
    try:
        temp = grid[i - 2][j + 1]
        solutionMoves.append([i - 2, j + 1])
    except:
        pass
    try:
        temp = grid[i - 2][j - 1]
        solutionMoves.append([i - 2, j - 1])
    except:
        pass
    try:
        temp = grid[i - 1][j - 2]
        solutionMoves.append([i - 1, j - 2])
    except:
        pass

    # Filter all negative values
    temp = ( tuple(i) for i in solutionMoves if i[0] >=1 and i[1] >=1 )
    return temp
    #allPossibleMoves = ["".join([chess_map_from_index_to_alpha[i[1]], str(i[0] + 1)]) for i in temp]
    #allPossibleMoves.sort()
    #return allPossibleMoves
