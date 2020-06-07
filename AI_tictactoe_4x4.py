import pygame
import sys
import os
from math import inf as infinity
from random import choice

pygame.font.init()

Width, Height = 750, 750

Win = pygame.display.set_mode((Width, Height))
Bg = (0,0,0)

Cross = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cross.png")), (Width//4, Height//4))
Circle = pygame.transform.scale(pygame.image.load(os.path.join("assets", "circle.png")), ((Width//4), (Height//4)))

clock = pygame.time.Clock()
FPS = 80

def fill(surface, color): #Change the color of a .png image
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))


class Grid():
    def __init__(self):
        self.grid = [((0, Height//4), (Width, Height//4)), ((0, (2*Height)//4), (Width, (2*Height)//4)), ((0, (3*Height)//4), (Width, (3*Height)//4)), ((Width//4, 0), (Width//4, Height)), (((2*Width)//4, 0), ((2*Width)//4, Height)), (((3*Width)//4,0), ((3*Width)//4, Height))]

        self.grid2 = [[0 for x in range(4)] for y in range(4)]
        self.Cross = Cross
        self.Circle = Circle

        self.switch = True
        self.game_over = False

    def draw(self, window):
        for line in self.grid:
            pygame.draw.line(window, (255, 255, 255), line[0], line[1], 2)

        for x in range(len(self.grid2)):
            for y in range(len(self.grid2[x])):
                if self.get_cell_value(x,y) == 1:
                    window.blit(self.Cross, (x*(Width//4),y*(Height//4)))
                elif self.get_cell_value(x,y) == -1:
                    window.blit(self.Circle, (x*(Width//4),y*(Height//4)))

    def get_cell_value(self, x,y):
        return self.grid2[y][x]

    def set_cell_value(self, x, y, value):
        self.grid2[y][x] = value

    def get_mouse(self, x, y, player):
        self.check_game()
        if self.get_cell_value(x,y) == 0:
            self.switch = True
            if player == 1:
                self.set_cell_value(x,y, 1)
            elif player == -1:
                self.set_cell_value(x, y, -1)
            self.winning(player)

        else:
            self.switch = False

    def winning(self, player):
        #Check rows
        for row in self.grid2:
            if row[0] == row[1] == row[2] == row[3] == player:

                if player == -1:
                    print("O wins")
                else:
                    print("X wins")
                self.game_over = True
                return self.game_over

        #Check columns
        for col in range(len(self.grid2[0])):
            check = []
            for row in self.grid2:
                check.append(row[col])
            if check.count(check[0]) == len(check) and check[0] != 0:
                if player == -1:
                    print("O wins")
                else:
                    print("X wins")
                self.game_over = True
                return self.game_over

        #Check diagonals
        diags = []
        for indx in range(len(self.grid2)):
            diags.append(self.grid2[indx][indx])
        if diags.count(diags[0]) == len(diags) and diags[0] != 0:
            if player == -1:
                print("O wins")
            else:
                print("X wins")
            self.game_over = True
            return self.game_over

    def check_game(self):
        zero = []
        for row in self.grid2:
            for case in row:
                zero.append(case)
        if zero.count(0) == 0:
            print("It's over !")
            self.game_over = True
        return self.game_over

    def empty_cells(self):
        cells = []
        for x, row in enumerate(self.grid2):
            for y, cell in enumerate(self.grid2):
                if cell == 0:
                    cells.append([x, y])

        return cells

    def good_move(self, x, y):
        if [x,y] in empty_cells():
            return True
        else:
            return False

    def reset(self):
        for y in range(len(self.grid2)):
            for x in range(len(self.grid2[y])):
                self.set_cell_value(x, y, 0)

    def rewards(self, board, player):
        score = 0
        opp_piece = 1
        if player == -1:
            opp_piece = 1
        else:
            opp_piece = -1

        if board.count(player) == 4:
            score += 400

        if board.count(player) == 3 and self.grid2.count(-1) == 1:
            score += 50

        if board.count(player) == 2 and self.grid2.count(-1) == 2:
            score += 10

        if board.count(player) == 1 and self.grid2.count(-1) == 3:
            score -= 10

        if board.count(opp_piece) == 3 and self.grid2.count(-1) = 1:
            score -= 10

        return score

    def evaluate(self, player):
        score = 0

        #Score (horizontally)
        for row in range(len(self.grid2)):
            new_board = [int(j) for j in list(self.grid2[row])]
            for col in range(len(new_board)):
                board = board[row]
                score += self.rewards()

        #Score (vertically)
        for row in range(len(self.grid2)):
            for i in range(len(self.grid2)-1):
                pass


    def print_grid(self):
        for row in self.grid2:
            print(row)


Grid = Grid()

def is_it_over(player):
    return Grid.empty_cells() == 0 or Grid.check_game() or Grid.winning(player)

def minimax(player, Grid, depth, Alpha, Beta, MaximizingPlayer):
    valid_locations = Grid.empty_cells()
    terminal_node = is_it_over(player)

    if depth == 0 or terminal_node:
        if terminal_node:
            pass


def redraw_window():
    Win.fill(Bg)

    Grid.draw(Win)
    pygame.display.flip()


def main():
    player = -1 #O
    run = True
    Grid.print_grid()
    color = (0,255,0,0)
    while run:
        clock.tick(FPS)
        fill(Circle, color)

        redraw_window()
        Win.fill(pygame.Color('lightskyblue4'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and not Grid.game_over:
                Grid.winning(player)
                if pygame.mouse.get_pressed()[0] and player == -1:
                    pos = pygame.mouse.get_pos()
                    #print(pos[0] // (Width // 4), pos[1] // (Height // 4))
                    Grid.get_mouse(pos[0] // (Width // 4), pos[1] // (Height // 4), player)
                    if Grid.switch:
                        if player == -1:
                            player = 1
                        else:
                            player = -1
                    Grid.print_grid()

                """
                if player == 1:
                    depth = len(Grid.empty_cells())
                    Grid.get_mouse(position[0], position[1], player)
                    if Grid.switch:
                        if player == 1:
                            player = 1
                        else:
                            player = -1
                """

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and Grid.game_over:
                    Grid.reset()
                    Grid.game_over = False

            if player == -1 and not Grid.game_over:
                pass

main()
