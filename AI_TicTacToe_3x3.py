import pygame
import random
import math
from math import inf as infinity
import sys
import os

"""

TicTacToe
Made with pygame

"""

pygame.font.init()

Width, Height = 770,770
Win = pygame.display.set_mode((Width, Height))


Cross = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cross.png")), (Width//3, Height//3))
Circle = pygame.transform.scale(pygame.image.load(os.path.join("assets", "circle.png")), (Width//3, Height//3))

Bg = (0,0,0)
Clock = pygame.time.Clock()

AI = 1
Human = -1

FPS = 80

def fill(surface, color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

def create_board():
    new_board = [[0 for i in range(3)] for j in range(3)]
    return new_board

def

def print_board(board):
    #print(board)
    for row in board:
        print(row)

def draw_board(Win):
    for i in range(1,3): #Draw vertical lines
        pygame.draw.line(Win, (255,255,255), (Width*(i/3),0), (Width*(i/3), Height), 1)

    for j in range(1,3): #Draw horizontal lines
        pygame.draw.line(Win, (255,255,255), (0,Width*(j/3)), (Width, Width*(j/3)), 1)


def redraw_window(Win):

    Win.fill(Bg)
    draw_board(Win)
    pygame.display.update()

board = create_board()

def main():
    global board
    #turn = random.choice([-1,1])
    turn = 1
    run = True
    green = (0,255,0,0)
    game_over = False

    while run:
        Clock.tick(FPS)
        redraw_window(Win)
        fill(Circle, green)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                print("Yes")
                if pygame.mouse.get_pressed()[0] and turn == Human:
                    print("Yes 2")
                    pos = pygame.mouse.get_pos()
                    if turn == Human and not game_over:
                        #print("pos", pos[0]//(Width//3), pos[1]//(Width//3))



main()
