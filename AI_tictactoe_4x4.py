import pygame
import sys
import os
import random
import time
from math import inf as infinity

"""
Rules :
place three noughts in a horizontal, vertical, or diagonal row
before the AI to win.
"""

pygame.font.init()

Width, Height = 750, 750

Win = pygame.display.set_mode((Width, Height))
Bg = (0,0,0)

Cross = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cross.png")), (Width//4, Height//4))
Circle = pygame.transform.scale(pygame.image.load(os.path.join("assets", "circle.png")), ((Width//4), (Height//4)))

clock = pygame.time.Clock()
FPS = 80

AI = 1
switch = True

def Create_Board():
    Game_Board = [[0 for x in range(4)] for y in range(4)]
    return Game_Board

def fill(surface, color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

class Grid():
    def __init__(self):
        self.grid = [((0, Height//4), (Width, Height//4)), ((0, (2*Height)//4), (Width, (2*Height)//4)), ((0, (3*Height)//4), (Width, (3*Height)//4)), ((Width//4, 0), (Width//4, Height)), (((2*Width)//4, 0), ((2*Width)//4, Height)), (((3*Width)//4,0), ((3*Width)//4, Height))]


        self.Cross = Cross
        self.Circle = Circle

        self.game_over = False

    def draw(self, board, window):
        for line in self.grid:
            pygame.draw.line(window, (255, 255, 255), line[0], line[1], 2)

        for x in range(len(board)):
            for y in range(len(board[x])):
                #print("y", y)
                if self.get_cell_value(board, x,y) == 1:
                    window.blit(self.Cross, (x*(Width//4),y*(Height//4)))
                elif self.get_cell_value(board, x,y) == -1:
                    window.blit(self.Circle, (x*(Width//4),y*(Height//4)))

    def get_cell_value(self,board, x,y):
        return board[y][x]

    def set_cell_value(self,board, x, y, value):
        board[y][x] = value

    def get_mouse(self, board, x, y, player):
        if self.get_cell_value(board, x,y) == 0:
            switch = True

            if player == 1:
                self.set_cell_value(board,x,y, 1)
            elif player == -1:
                self.set_cell_value(board,x, y, -1)
            #self.check(x,y, player)
            self.check_rows(board,player)
            self.check_columns(board,player)
            self.check_diagonals(board,player)
            self.check_game(board)

        else:
            switch = False

    def check_rows(self, board,player):
        for row in board:
            if row[0] == row[1] == row[2] == row[3] == player:

                if player == -1:
                    print("O wins")
                else:
                    print("X wins")
                self.game_over = True

    def check_columns(self, board, player):
        for col in range(len(board[0])):
            check = []
            for row in board:
                check.append(row[col])
            if check.count(check[0]) == len(check) and check[0] != 0:
                if player == -1:
                    print("O wins")
                else:
                    print("X wins")
                self.game_over = True

    def check_diagonals(self,board, player):
        diags = []
        for indx in range(len(board)):
            diags.append(board[indx][indx])
        if diags.count(diags[0]) == len(diags) and diags[0] != 0:
            if player == -1:
                print("O wins")
            else:
                print("X wins")
            self.game_over = True

        diags_2 = []
        for indx, rev_indx in enumerate(reversed(range(len(board)))):
            ext = board[indx][rev_indx]
            diags_2.append(ext)
        if diags_2.count(player) == len(diags_2):
            if player == -1:
                print("O wins")
            else:
                print("X wins")
            self.game_over = True


    def check_game(self, board):
        zero = []
        for row in board:
            for box in row:
                zero.append(box)
        if zero.count(0) == 0:
            print("It's over !")
            self.game_over = True
        return self.game_over

    def reset(self, board):
        for y in range(len(board)):
            for x in range(len(board[y])):
                self.set_cell_value(board,x, y, 0)

    def print_grid(self, board):
        for row in board:
            print(row)

Grid = Grid()

def get_valid_locations(board):
    valid_locations = []
    for x, row in enumerate(board):
        for y, box in enumerate(row):
            if box == 0:
                valid_locations.append([x, y])

    return valid_locations

def put_in_the_box(board,x,y, value):
    return board[y][x] == value


def eval_window(board, piece):
    score = 0
    AI_piece = AI
    opp_piece = -1
    if piece == -1:
        opp_piece = AI

    for row in board:
        for j in range(3):
            if row.count(piece) == j:
                score += 5*j + 4
    print(score)

    for i in range(2):
        for j in range(2):
            if row.count(opp_piece) == i and row.count(piece) == j:
                score -= (2*i + 2*j)
    print(score)

    for col in range(len(board)):
        column = []
        for row in board:
            column.append(row[col])
        for i in range(3):
            if column.count(piece) == i:
                score += 2*i + 4
    print(score)

    diags = []
    for pos in range(len(board)):
        diags.append(board[pos][pos])
    for i in range(3):
        if diags.count(piece) == i:
            score += 3*i+4
    print(score)

    diags_2 = []
    for idx, rev_idx in enumerate(reversed(range(len(board)))):
        diags_2.append(board[idx][rev_idx])
    for i in range(3):
        if column.count(piece) == i:
            score += 3*i+4
    print(score)

    return score


def evaluate(board):

    score = 0

    score = eval_window(board, 1)

    if check_game(board, -1):
        score -= 50

    if check_game(board, 1):
        score += 50

    return score

def check_game(board, player):
    for row in board:
        if row[0] == row[1] == row[2] == row[3] == player:
            return True

    for col in range(len(board[0])):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(player) == len(check) and check[0] != 0:
            return True

    diags = []
    for indx in range(len(board)):
        diags.append(board[indx][indx])
    if diags.count(player) == len(diags) and diags[0] != 0:
        return True

    diags_2 = []
    for indx, rev_indx in enumerate(reversed(range(len(board)))):
        ext = board[indx][rev_indx]
        diags_2.append(ext)
    if diags_2.count(player) == len(diags_2):
        return True


def game_over(board):
    return check_game(board, -1) or check_game(board, 1)


def minimax(board, depth, Player):
    valid_locations = get_valid_locations(board)
    print("minimax valid loc ",valid_locations)

    if Player == AI:
        best = [-1,-1,-infinity]
    else:
        best = [-1,-1,infinity]

    if game_over(board) or depth == 0 or len(valid_locations) == 0:
        score = evaluate(board)
        print(score)
        return [-1, -1, score]

    for box in valid_locations:
        x = box[0]
        y = box[1]
        new_board = board.copy()
        new_board[y][x] = Player
        info = minimax(board, depth-1, -AI)
        new_board[x][y] = 0
        info[0], info[1] = x,y

        if Player == AI: #Maximizing
            if info[2] > best[2]:
                best = info
        else: #Minimizing
            if info[2] < best[2]:
                best = info

    return best

def valid_move(board, x,y):
    if [x,y] in get_valid_locations(board):
        return True
    else:
        return False

def set_move(board, x,y, player):
    if valid_move(board, x,y):
        board[y][x] = player
        switch = True
        return True
    else:
        switch = False
        return False

def ai_turn(board):
    depth = len(get_valid_locations(board))
    if depth == 0 or game_over(board):
        return

    if depth == 16:
        x = random.choice([0, 1, 2, 3])
        y = random.choice([0, 1, 2, 3])

    else:
        box_pos = minimax(board, depth, AI)
        x,y = box_pos[0], box_pos[1]

    set_move(board, x,y, AI)
    time.sleep(1)


def redraw_window(board):
    Win.fill(Bg)

    Grid.draw(board, Win)
    pygame.display.flip()

Board = Create_Board()

def main():
    global Board
    start = [-1,1]
    player = random.choice(start)
    run = True
    Grid.print_grid(Board)
    color = (0,255,0,0)
    alpha = -infinity
    beta = infinity
    depth = 3
    while run:
        clock.tick(FPS)
        fill(Circle, color)
        redraw_window(Board)
        Win.fill(pygame.Color('lightskyblue4'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and Grid.game_over:
                    Grid.reset(Board)
                    Grid.game_over = False

            if event.type == pygame.MOUSEBUTTONDOWN and not Grid.game_over:
                #print("Yes !")
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if player == -1 and not Grid.game_over:
                        #print(pos[0] // (Width // 4), pos[1] // (Height // 4))
                        Grid.get_mouse(Board, pos[0] // (Width // 4), pos[1] // (Height // 4), player)
                        if switch:
                            if player == -1:
                                player = 1
                            else:
                                player = -1
                        Grid.print_grid(Board)


        if player == AI and not Grid.game_over:
            ai_turn(Board)
            if switch:
                if player == 1:
                    player = -1
                else:
                    player = 1
            Grid.print_grid(Board)

if __name__ == "__main__":
    main()
