
import pprint

grid = [[1] * 10 for i in range(10)]

def get_km():
    result = {}
    for i in range(8,9):
        for j in range(8,9):
            solutionMoves = []
            try:
                temp = grid[i + 1][j - 2]
                solutionMoves.append([i + 1, j - 2])
            except Exception:
                pass
            try:
                temp = grid[i + 2][j - 1]
                solutionMoves.append([i + 2, j - 1])
            except Exception:
                pass
            try:
                temp = grid[i + 2][j + 1]
                solutionMoves.append([i + 2, j + 1])
            except Exception:
                pass
            try:
                temp = grid[i + 1][j + 2]
                solutionMoves.append([i + 1, j + 2])
            except Exception:
                pass
            try:
                temp = grid[i - 1][j + 2]
                solutionMoves.append([i - 1, j + 2])
            except Exception:
                pass
            try:
                temp = grid[i - 2][j + 1]
                solutionMoves.append([i - 2, j + 1])
            except Exception:
                pass
            try:
                temp = grid[i - 2][j - 1]
                solutionMoves.append([i - 2, j - 1])
            except Exception:
                pass
            try:
                temp = grid[i - 1][j - 2]
                solutionMoves.append([i - 1, j - 2])
            except Exception:
                pass
            # Filter all negative values
            result[(i,j)] = [ i for i in solutionMoves if i[0] >=1 and i[1] >=1 ]
            
     
    return result
