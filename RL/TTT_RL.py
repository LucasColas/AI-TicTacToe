import pygame
import sys
import os
import random

pygame.init()

Width, Height = 770,770

Win = pygame.display.set_mode((Width, Height))

Bg = (0,0,0)

Cross = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "cross.png")), (Width//3, Height//3))
Circle = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "circle.png")), (Width//3, Height//3))

clock = pygame.time.Clock()



def fill(surface, color):
    w,h = surface.get_size()
    r,g,b,_ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x,y))[3]
            surface.set_at((x,y), pygame.Color(r,g,b,a))



def check_game(board, player):

    for row in board:
        if row[0] == row[1] == row[2] == player:
            print(player, "gagne")
            return True

    for col in range(len(board)):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(player) == len(check) and check[0] != 0:
            print(player, "gagne")

            return True

    diags = []
    for indx in range(len(board)):
        diags.append(board[indx][indx])
    if diags.count(player) == len(diags) and diags[0] != 0:
        print(player, "gagne")
        return True

    diags_2 = []
    for indx, rev_indx in enumerate(reversed(range(len(board)))):
        print(indx, rev_indx)
        diags_2.append(board[indx][rev_indx])
    if diags_2.count(player) == len(diags_2) and diags_2[0] != 0:
        print(player, "gagne")
        return True

    if len(empty_cells(board)) == 0:
        print("personne ne gagne")
        return True


def create_board():
    new_board = [[0 for i in range(3)] for j in range(3)]
    return new_board

def empty_cells(board):
    empty_cells = []
    for y, row in enumerate(board):
        for x,case in enumerate(row):
            if case == 0:
                empty_cells.append([x,y])
    return empty_cells

def valid_locations(board,x,y):
    if [x,y] in empty_cells(board):
        return True
    else:
        return False

def set_locations(game_board,x,y,player):
    if valid_locations(game_board,x,y):
        game_board[y][x] = player
        return True
    else:
        return False

def draw_board(Win):
    for i in range(1,3):
        pygame.draw.line(Win, (255,255,255), (Width*(i/3), 0), (Width*(i/3), Height), 1)

    for j in range(1,3):
        pygame.draw.line(Win, (255,255,255), (0, Width*(j/3)), (Width, Width*(j/3)), 1)

def draw_pieces(Win, board):
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] == -1:
                Win.blit(Circle, (x*(Width//3), y*(Width//3)))
            elif board[y][x] == 1:
                Win.blit(Cross, (x*(Width//3), y*(Width//3)))


def reset_board(game_board):
    for x,row in enumerate(game_board):
        for y in range(len(row)):
            game_board[y][x] = 0


def redraw_window(Win, board):
    Win.fill(Bg)
    draw_board(Win)
    draw_pieces(Win, board)
    pygame.display.update()

def main():
    start = [-1,1]
    player = random.choice(start)
    run = True
    game_over = False
    game_board = create_board()
    FPS = 120
    green = (0,255,0,0)
    while run:

        fill(Circle, green)
        clock.tick(FPS)
        redraw_window(Win, game_board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    reset_board(game_board)
                    game_over = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                if set_locations(game_board, pos[0]//(Width//3), pos[1]//(Width//3), player):
                    if check_game(game_board, player):
                        print("over")
                        game_over = True
                    if player == -1:
                        player = 1
                    else:
                        player = -1



main()
