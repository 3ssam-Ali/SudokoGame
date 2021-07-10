# import numpy as np
from time import perf_counter, process_time
import random
import itertools

def isvalid(grid, y, x, n):  # checks if n can be put in those x,y
    # check the vertical and horizontal
    for i in range(9):
        if i != y and grid[i][x] == n:
            return False
        if i != x and grid[y][i] == n:
            return False
    # check the surroundings
    # get the coordinates for the current square
    sy = 3*(y//3)
    sx = 3*(x//3)
    for dy in range(3):
        for dx in range(3):
            if sy+dy != y and sx+dx != x:
                if grid[sy+dy][sx+dx] == n:
                    return False
    return True

# solve with yield will act as a generator for solutions
# conputaion will only continue when needed
def solve(grid,timer):
    number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if perf_counter()-timer>0.5: return False
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                # good for making the numbers in the solution random
                random.shuffle(number_list)
                for i in number_list:
                    if isvalid(grid, y, x, i):
                        grid[y][x] = i
                        yield from solve(grid,timer)
                        if perf_counter()-timer>0.5: return False
                        grid[y][x] = 0
                return
    yield [[entry for entry in row] for row in grid]


def checkall(g):  # maybe there is somthing better?
    for y in range(9):
        for x in range(9):
            if g[y][x] != 0 and state[y][x] != 0:
                state[y][x] = 1 if isvalid(g, y, x, g[y][x]) else 2


def checkGrid(grid):  # chicks if there is any empty cells
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == 0:
                return False

def set_board(cp, solution, required):  # removes some blocks and adds back untill satisfied
    time=perf_counter()
    empty = 0  # max should be around 66 the remaining is 15
    # first we remove random blocks
    while empty < 81-required:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        if cp[y][x] != 0:
            cp[y][x] = cp[8-y][8-x] = 0
            empty += 2
    # we add some blocks back untill we get unique solution
    count = 81-empty
    while True:
        s = solve([x[:] for x in cp],time)
        solved = [*itertools.islice(s, 2)]
        if len(solved)== 0 :return False
        if len(solved) == 1: break
    # we add more elements to make the solution unique
        diffPos = [(y, x) for y in range(9) for x in range(9) if solved[0][y][x] != solved[1][y][x]]
        y, x = random.choice(diffPos)
        cp[y][x] = solution[y][x]
        cp[8-y][8-x] = solution[8-y][8-x]
        count += 2
    # make sure the number of elements is the required num
    if count < required:
        zeroPos = [(y, x) for y in range(9) for x in range(9) if cp[y][x] == 0]
        while count <= required:
            y, x = random.choice(zeroPos)
            zeroPos.remove((y,x))
            cp[y][x] = solution[y][x]
            count+=1
    return cp


def generateGrid():
    g = [[0]*9 for x in range(9)]
    # creates a solution and shuffle the rows
    while True:
        time=perf_counter()
        solution = next(solve(g,time))
        seperated_rows = [solution[:3], solution[3:6], solution[6:9]]
        for row in seperated_rows:
            random.shuffle(row)
        random.shuffle(seperated_rows)
        shuffled = [row for block in seperated_rows for row in block]
        # remove random blocks
        cp = [x[:] for x in shuffled]
        required = random.randint(17, 30)  # how many blocks should remain
        grid = set_board(cp, shuffled, required)
        if grid!= False: break
    return grid

Ogrid=generateGrid()
grid=[x[:] for x in Ogrid] #makes a copy for the player
state=[[1 if i==0 else 0 for i in x ] for x in grid] # 0:original 1:valid move 2:invalid
generator=solve([x[:] for x in Ogrid],perf_counter())
solution=next(generator)


if __name__ == "__main__":
    pass

