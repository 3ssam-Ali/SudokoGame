# import numpy as np
def isvalid(grid,x,y,n):
    #check the vertical and horizontal
    for i in range(9):
        if i!=x and grid[i][y]==n:
            return False
        if i!=y and grid[x][i]==n:
            return False
    #check the surroundings
    #get the coordinates for the current square
    sx=3*(x//3)
    sy=3*(y//3)
    for dx in range(3) :
        for dy in range(3) :
            if grid[sx+dx][sy+dy]==n: return False
    return True

# solve with yield will act as a generator for solutions 
# conputaion will only continue when needed
def solve(grid):
    for x in range(9):
        for y in range(9):
            if grid[x][y]==0:
                for i in range(1,10):
                    if isvalid(grid,x,y,i):
                        grid[x][y]=i
                        yield from solve(grid)
                        grid[x][y]=0
                else:
                    return
    yield grid 


if __name__ == "__main__":
    # grid=[
    #     [0,0,0,0,0,0,0,0,2],
    #     [1,0,0,0,0,3,0,0,0],
    #     [0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0],
    #     [0,0,5,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,9,0,0],
    #     [0,0,0,0,0,2,0,0,0],
    #     [0,4,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,4,0,0,0]
    # ]
    grid=[
        [3, 5, 4, 0, 6, 7, 8, 9, 2],
        [1, 2, 6, 8, 9, 3, 4, 5, 7],
        [7, 8, 9, 2, 4, 5, 1, 3, 6],
        [2, 1, 3, 4, 5, 9, 6, 7, 8],
        [4, 9, 5, 6, 7, 8, 2, 1, 3],
        [6, 7, 8, 3, 2, 1, 9, 4, 5],
        [5, 3, 1, 9, 8, 2, 7, 6, 4],
        [8, 4, 7, 5, 1, 6, 3, 2, 9],
        [9, 6, 2, 7, 3, 4, 5, 8, 1]
        ]
    s= solve(grid)
    # print(np.matrix(next(s)))
    print(*next(s),sep='\n')
