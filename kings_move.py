
grid = [[1] * 10 for i in range(10)]

move_offsets=[ (-1,-1), (-1,0), (-1,1) , (0,-1), (0,1), (1,-1), (1,0), (1,1) ]

def get_kingsmove():
    result = {}
    for i in range(1,10):
        for j in range(1,10):
            solutionMoves = []
            for (x,y) in move_offsets:
                try:
                    temp = grid[i+x][j + y]
                    solutionMoves.append([ i+x, j+y ])
                except:
                    pass
            # Filter all negative values
            result[(i,j)] = [ i for i in solutionMoves if i[0] >=1 and i[1] >=1 ]
            
     
    return result
