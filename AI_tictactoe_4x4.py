import pygame
import sys
import os
import random
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

    def set_cell_value(self, grid, x, y, value):
        grid[y][x] = value

    def get_mouse(self, grid, x, y, player):
        self.check_game()
        if self.get_cell_value(x,y) == 0:
            self.switch = True
            if player == 1:
                self.set_cell_value(grid, x,y, 1)
            elif player == -1:
                self.set_cell_value(grid, x, y, -1)
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
        for row in range(len(self.grid2)):
            for col in range(len(self.grid2[row])):
                if self.grid2[row][col] == 0:
                    cells.append([row, col])

        return cells

    def good_move(self, x, y):
        if [x,y] in empty_cells():
            return True
        else:
            return False

    def reset(self, grid):
        for y in range(len(self.grid2)):
            for x in range(len(self.grid2[y])):
                self.set_cell_value(grid, x, y, 0)

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

        if board.count(opp_piece) == 3 and self.grid2.count(-1) == 1:
            score -= 10

        return score

    def evaluate(self, player):
        score = 0

        #Score (horizontally)
        for row in range(len(self.grid2)):
            new_board = [int(j) for j in self.grid2[row]]
            score += self.rewards(new_board, player)

        #Score (vertically)
        board_vt = []
        for row in range(len(self.grid2)):
            for i in range(len(self.grid2)-1):
                board_vt.append(self.grid2[i][row])
                score += self.rewards(board_vt, player)

        #Score (diagonally)
        # First diagonal (from the left to the right)
        board_dg = []
        for position in range(len(self.grid2)):
            extension = self.grid2[position][position]
            board_dg.append(extension)
            if position == (len(self.grid2)-1):
                score += self.rewards(board_dg, player)

        # Second diagonal (from the right to the left)
        board_dg2 = []
        for indx, position in enumerate(reversed(range(len(self.grid2)))):
            extension = self.grid2[indx][position]
            board_dg2.append(extension)
            if indx == (len(self.grid2)-1):
                score += self.rewards(board_dg2, player)

        return score


    def print_grid(self):
        for row in self.grid2:
            print(row)

Grid = Grid()


def is_it_over():
    return Grid.empty_cells() == 0 or Grid.check_game() or Grid.winning(-1) or Grid.winning(1)

def minimax(Grid_board, depth, Alpha, Beta, MaximizingPlayer):
    valid_locations = Grid.empty_cells()
    print("valid_locations", valid_locations)
    terminal_node = is_it_over()
    print("enter minimax")

    if depth == 0 or terminal_node:
        if terminal_node:
            print("terminal_node")
            if Grid.winning(-1):
                return (None, -10000000)
            elif Grid.winning(1):
                return (None, 10000000)
            else:
                return (None, 0)
        else:
            print("evaluate")
            return (None,Grid.evaluate(1))

    if MaximizingPlayer:
        print("MaximizingPlayer")
        best = -infinity
        pos1 = random.randint(2,3)
        pos2 = random.randint(2,3)
        position = [0, 0]
        score = 0
        return_min = []
        for case in valid_locations:
            print("Check valid_locations")
            x,y = case[0], case[1]

            new_grid = list(Grid_board)
            Grid.set_cell_value(new_grid,x,y, 1)
            print("New grid", new_grid)
            print("Grid", Grid_board)

            score = max(best, minimax(new_grid, depth-1, Alpha, Beta, False)[1])

            if score > best:
                best = score
                position = case

            Alpha = max(Alpha, score)
            if Alpha >= Beta:
                break
        return_min.append(position[0])
        return_min.append(position[1])
        return_min.append(score)
        return return_min


    else: #Minimizing
        best = +infinity
        return_min = []
        pos1 = random.randint(2,3)
        pos2 = random.randint(2,3)
        position = [0, 0]
        score = 0
        for case in valid_locations:
            x,y = case[0], case[1]

            new_grid = list(Grid_board)
            Grid.set_cell_value(new_grid,x,y, -1)
            print(new_grid)

            score = min(best, minimax(new_grid, depth-1, Alpha, Beta, True)[1])

            if score < best:
                best = score
                position = case
            Beta = min(Beta, score)

            if Beta >= Alpha:
                break
        return_min.append(position[0])
        return_min.append(position[1])
        return_min.append(score)
        return return_min


def redraw_window():
    Win.fill(Bg)

    Grid.draw(Win)
    pygame.display.flip()


def main():
    global Grid
    Grid_board = Grid.grid2
    start = [-1,1]
    player = random.choice(start) # -1 = O(player) and 1 = X (AI)
    run = True
    Grid.print_grid()
    color = (0,255,0,0)
    while run:
        clock.tick(FPS)
        fill(Circle, color)
        redraw_window()
        Win.fill(pygame.Color('lightskyblue4'))
        Grid.winning(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and not Grid.game_over:
                #print("Yes !")

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    #print(pos[0] // (Width // 4), pos[1] // (Height // 4))
                    Grid.get_mouse(Grid_board, pos[0] // (Width // 4), pos[1] // (Height // 4), player)
                    if Grid.switch:
                        if player == -1:
                            player = 1
                        else:
                            player = -1
                    Grid.print_grid()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and Grid.game_over:
                    Grid.reset(Grid_board)
                    Grid.game_over = False
main()
