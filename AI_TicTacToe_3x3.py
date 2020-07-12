import pygame
import random
import math
from math import inf as infinity
import sys
import os
import time

"""

TicTacToe
Made with pygame.
You (you have circles) play against an AI (it has crosses).
For the AI I used Minimax algorithm.
The player who begins is selected randomly

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
AI_wins = False
Player_wins = False
No_one = False

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


def check_game(board, player):

    for row in board:
        if row[0] == row[1] == row[2] == player:
            print("player", player, "wins")
            if player == 1:
                AI_wins = True
            if player == -1:
                Player_wins = True
            return True

    for col in range(len(board)):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(player) == len(check) and check[0] != 0:
            print("player", player, "wins")
            if player == 1:
                AI_wins = True
            if player == -1:
                Player_wins = True
            return True

    diags = []
    for indx in range(len(board)):
        diags.append(board[indx][indx])
    if diags.count(player) == len(diags) and diags[0] != 0:
        print("player", player, "wins")
        if player == 1:
            AI_wins = True
        if player == -1:
            Player_wins = True
        return True

    diags_2 = []
    for indx, rev_indx in enumerate(reversed(range(len(board)))):
        diags_2.append(board[indx][rev_indx])
    if diags_2.count(player) == len(diags_2) and diags_2[0] != 0:
        print("player", player, "wins")
        if player == 1:
            AI_wins = True
        if player == -1:
            Player_wins = True
        return True

    if len(empty_cells(board)) == 0:
        print("No winner")
        No_one = True
        return True


def empty_cells(board):
    empty_cells = []
    for y,row in enumerate(board):
        for x,case in enumerate(row):
            if case == 0:
                empty_cells.append([x,y])

    return empty_cells

def valid_locations(board,x,y,player):
    if [x,y] in empty_cells(board):
        print("good")
        board[y][x] = player
        return True

def is_terminal_node(board):
    return check_game(board, 1) or check_game(board,-1)

def evaluate(board):
    score = 0
    if check_game(board, 1):
        score += 10
    elif check_game(board, -1):
        score -= 10

    for row in board:
            for j in range(len(row)):
                if row.count(j) == 1:
                    score += 2*j + 2
            for i in range(len(row)):
                if row.count(i) == -1:
                    score -= j + 3

    return score

def end(board):
    score = 0
    if check_game(board, -1):
        score -= 5
        return score
    elif check_game(board, 1):
        score += 5
        return score
    else:
        score = 0
        return score



def minimax(board, depth, alpha, beta, player):
    terminal_node = is_terminal_node(board)
    print("depth in minimax", depth)
    if player == 1:
        best = [-1,-1,-infinity]
    else:
        best = [-1, -1, infinity]

    if depth <= 0 or terminal_node:
        score = end(board)
        return [-1, -1,score]

    for cell in empty_cells(board):
        x,y = cell[0], cell[1]
        board[y][x] = player
        info = minimax(board, depth-1, alpha, beta, -player)
        board[y][x] = 0
        info[0], info[1] = x,y

        if player == 1:
            if info[2] > best[2]:
                best = info
            alpha = max(alpha, best[2])
            if alpha >= beta:
                break
        else:
            if info[2] < best[2]:
                best = info
            beta = min(beta,best[2])
            if alpha >= beta:
                break

    return best

def ai_turn(board, alpha, beta):
    depth = len(empty_cells(board))
    terminal_node = is_terminal_node(board)

    if depth == 0 or terminal_node:
        return

    if depth == 9:
        if [1,1] in empty_cells(board):
            x,y = 1,1
        else:
            x = random.choice([0,1,2])
            y = random.choice([0,1,2])
    else:
        print("depth", depth)
        info = minimax(board, depth, alpha, beta,1)
        x,y = info[0], info[1]

    valid_locations(board,x,y,1)
    #time.sleep()


def print_board(board):
    #print(board)
    for row in board:
        print(row)

def reset_board(board):
    for x, row in enumerate(board):
        for y in range(len(row)):
            board[y][x] = 0


def draw_board(Win):
    for i in range(1,3): #Draw vertical lines
        pygame.draw.line(Win, (255,255,255), (Width*(i/3),0), (Width*(i/3), Height), 1)

    for j in range(1,3): #Draw horizontal lines
        pygame.draw.line(Win, (255,255,255), (0,Width*(j/3)), (Width, Width*(j/3)), 1)

def draw_pieces(Win, board):
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] == -1:
                Win.blit(Circle, (x*(Width//3), y*(Width//3)))
            elif board[y][x] == 1:
                Win.blit(Cross, (x*(Width//3), y*(Width//3)))

def print_result(board, Win, player):
    Font = pygame.font.SysFont("monospace", 75)
    Yellow = (255,255,0)
    Play_again = Font.render("Play gain ? Press space bar", 1, Yellow)
    AI_wins = Font.render("AI wins. Play again ? Press space bar", 1,Yellow)
    Player_wins = Font.render("Player wins. Play again ? Press space bar", 1,Yellow)

    if AI_wins:
        Win.blit(AI_wins, ((Width/2 - AI_wins.get_width()), Height/2))
    elif Player_wins:
        Win.blit(Player_wins, (Width/2, Height/2))
    if No_one:
        Win.blit(Play_again, (Width/2, Height/2))


def redraw_window(Win, board, player):

    Win.fill(Bg)
    draw_board(Win)
    draw_pieces(Win,board)
    print_result(board, Win,player)
    pygame.display.update()

board = create_board()

def main():
    global board
    turn = random.choice([-1,1])
    run = True
    green = (0,255,0,0)
    game_over = False
    depth = len(empty_cells(board))

    while run:
        Clock.tick(FPS)
        redraw_window(Win, board, turn)
        fill(Circle, green)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    reset_board(board)
                    turn = random.choice([-1,1])
                    game_over = False
                    if AI_wins:
                        AI_wins = False
                    elif Player_wins:
                        Player_wins = False
                    else:
                        No_one = False

            if event.type == pygame.MOUSEBUTTONDOWN and turn == Human and not game_over:
                print("Yes")
                if pygame.mouse.get_pressed()[0] and turn == Human and not game_over:
                    print("Yes 2")
                    pos = pygame.mouse.get_pos()
                    if turn == Human and not game_over:
                        print("pos", pos[0]//(Width//3), pos[1]//(Width//3))
                        #board[pos[1]//(Width//3)][pos[0]//(Width//3)] = 1
                        #print(empty_cells(board))
                        if valid_locations(board,pos[0]//(Width//3), pos[1]//(Width//3),turn):
                            if check_game(board, -1):
                                print("stop")
                                game_over = True
                            turn = AI
                            print("Gooooood")
                            print_board(board)
                            print(empty_cells(board))


        if turn == AI and not game_over:
            """
            #select randomly
            random_pos = random.randint(0,len(empty_cells(board))-1)
            x,y = empty_cells(board)[random_pos]
            """
            if [1,1] in empty_cells(board): #If the middle cell is available, use it.
                x,y = [1,1]
                board[y][x] = AI
            else:
                alpha = -infinity
                beta = infinity
                ai_turn(board,alpha, beta)
            if check_game(board, 1):
                game_over = True
            turn = Human

main()
