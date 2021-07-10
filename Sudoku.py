from sys import exit
import pygame
from tkinter import *
from tkinter import messagebox

pygame.init()
from SudokuSolver import *

# creating scrceen and necessities
pygame.display.set_caption('Sudoku')
size = width, height = 600, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 30
Ix = 0  # Indecies for the current square ################################
Iy = 0
squaresize = (width/9, (height-100)/9)  # size of each square on the board
offset = ((width/9)/2, ((height-100)/9)/2) # used to get to the center of a square

# defining the colors
black = (0, 0, 0)
gray = (200,200,200)
white = (255, 255, 255)
red=(255,0,0)
blue = (0, 0, 180)
purple = (255, 100, 0)
textColor=[blue,black,red]

# defining the text
font_obj = pygame.font.SysFont('arial', 22)
font_obj_2 = pygame.font.SysFont('arial', 35)
text_1 = font_obj.render(
    'Use directions for transitions and num keys for input.', True, black)
text_2 = font_obj.render(
    'Reset the board using R, press U to solve autotically.', True, black)
text_3 = font_obj.render(
    'Generate new grid using N. *it may take a second', True, black)

# defining the highlight rectangle
highlight_rect = pygame.Surface(squaresize)
highlight_rect.set_alpha(50)
pygame.draw.rect(highlight_rect, blue, highlight_rect.get_rect(), 10)

def highlight():
    screen.blit(highlight_rect, (Ix*squaresize[0], Iy*squaresize[1]))

def displayGrid():
    for y in range(9):
        for x in range(9):
            if grid[y][x] != 0:
                txt = font_obj_2.render(f'{grid[y][x]}', True, textColor[state[y][x]] )
                text_rect_obj = txt.get_rect()
                text_rect_obj.center = (
                    (x*squaresize[0])+offset[0], (y*squaresize[1])+offset[1])
                screen.blit(txt, text_rect_obj)
# display a message box when the game is finished
def finished():
    Tk().wm_withdraw() #to hide the main window
    messagebox.showinfo('congrats','Yaay you won')

# main loop
while True:
    clock.tick(FPS)
    screen.fill(white)  # resetting the screen each tick
    # drawing the basic board
    for i in range(10):
        pygame.draw.line(screen,gray, (0, i*((height-100)/9)),(width, i*((height-100)/9)),2)  # horizontal
        if i != 0:  # skipping the first line on the left for symmetry
            pygame.draw.line(screen,gray, (i*(width/9), 0),(i*(width/9), height-100),2)  # vertical
    for i in range(0,10,3):
        pygame.draw.line(screen, purple , (0, i*((height-100)/9)),(width, i*((height-100)/9)), 4)  # horizontal
        if i != 0:  # skipping the first line on the left for symmetry
            pygame.draw.line(screen, purple, (i*(width/9), 0),(i*(width/9), height-100), 4 )  # vertical
    
    # display text
    screen.blit(text_1, (10, height-90))
    screen.blit(text_2, (10, height-60))
    screen.blit(text_3, (10, height-30))

    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if Iy > 0:
                    Iy -= 1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if Iy < 8:
                    Iy += 1
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if Ix > 0:
                    Ix -= 1
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if Ix < 8:
                    Ix += 1
            elif event.unicode.isnumeric() and event.mod in [0,4096]:  # num of no modifier ex: shift is 0 but for me it's 4096
                num = int(event.unicode)
                if num != 0 and Ogrid[Iy][Ix] == 0:
                    if isvalid(grid, Iy, Ix, num):
                        grid[Iy][Ix] = num
                        state[Iy][Ix] = 1
                        if grid==solution:finished()
                    else:
                        grid[Iy][Ix] = num
                        state[Iy][Ix] = 2
            elif event.key == pygame.K_BACKSPACE:
                grid[Iy][Ix]=Ogrid[Iy][Ix]
                state[Iy][Ix] = 0
                checkall(grid)
            elif event.key== pygame.K_u:
                Ogrid=grid=solution
            elif event.key==pygame.K_r:
                grid=[x[:] for x in Ogrid]  
                state=[[1 if i==0 else 0 for i in x ] for x in grid]
            elif event.key==pygame.K_n:
                Ogrid=generateGrid()
                grid=[x[:] for x in Ogrid] 
                state=[[1 if i==0 else 0 for i in x ] for x in grid]
                g=solve([x[:] for x in Ogrid],perf_counter())
                solution=next(g)
    displayGrid()
    highlight()
    pygame.display.update()
