import pygame
import random
import math
from math import inf as infinity
import sys
import os

pygame.font.init()

Width, Height = 750,750
Win = pygame.display.set_mode((Width, Height))


Cross = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cross.png")), (Width//3, Height//3))
Cirlce = pygame.transform.scale(pygame.image.load(os.path.join("assets", "circle.png")), (Width//3, Height//3))

Bg = (0,0,0)
Clock = pygame.time.Clock()

FPS = 80

AI = 1
Human = -1

def create_board():
    new_board = [[0 for i in range(3)] for j in range(3)]
    return new_board

def print_board(board):
    #print(board)
    for row in board:
        print(row)


board = create_board()
print_board(board)
