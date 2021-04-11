
grid = [[1] * 9 for i in range(9)]

def get_km():
    result = {}
    for i in range(1,10):
        for j in range(1,10):
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
            result[(i,j)] = [ i for i in solutionMoves if i[0] >=1 and i[1] >=1 ]
            
     
    return result
