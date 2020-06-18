import pygame
import sys
import os
import random
from math import inf as infinity

pygame.font.init()

Width, Height = 750, 750

Win = pygame.display.set_mode((Width, Height))
Bg = (0,0,0)

Cross = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cross.png")), (Width//4, Height//4))
Circle = pygame.transform.scale(pygame.image.load(os.path.join("assets", "circle.png")), ((Width//4), (Height//4)))

clock = pygame.time.Clock()
FPS = 80

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

    def get_mouse(self, board, x, y, player):
        if self.get_cell_value(x,y) == 0:
            self.switch = True

            if player == 1:
                self.set_cell_value(x,y, 1)
            elif player == -1:
                self.set_cell_value(x, y, -1)
            #self.check(x,y, player)
            self.check_rows(player)
            self.check_columns(player)
            self.check_diagonals(player)
            self.check_game()

        else:
            self.switch = False

    def check_rows(self, player):
        for row in self.grid2:
            if row[0] == row[1] == row[2] == row[3] == player:

                if player == -1:
                    print("O wins")
                else:
                    print("X wins")
                self.game_over = True

    def check_columns(self, player):
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

    def check_diagonals(self,player):
        diags = []
        for indx in range(len(self.grid2)):
            diags.append(self.grid2[indx][indx])
        if diags.count(diags[0]) == len(diags) and diags[0] != 0:
            if player == -1:
                print("O wins")
            else:
                print("X wins")
            self.game_over = True

    def check_game(self):
        zero = []
        for row in self.grid2:
            for box in row:
                zero.append(box)
        if zero.count(0) == 0:
            print("It's over !")
            self.game_over = True
        return self.game_over

    def reset(self):
        for y in range(len(self.grid2)):
            for x in range(len(self.grid2[y])):
                self.set_cell_value(x, y, 0)

    def print_grid(self):
        for row in self.grid2:
            print(row)

def good_box(board, x,y):
    return board[y][x] == 0

def empty_cells(board):
    empty = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                empty.append([row, col])

    return empty

def valid_locations(board):
    valid_locations = []
    for x in range(len(board)):
        for y in range(len(board[x])):
            if good_box(board, y,x):
                valid_locations.append([x,y])

    return valid_locations

def put_in_the_box(board,x,y, value):
    return board[y][x] == value

def rewards(board, player):
    score = 0
    opp_piece = -1
    if player == -1:
        opp_piece = 1

    if board.count(player) == 4:
        score += 400

    if board.count(player) == 3 and board.count(-1) == 1:
        score += 50

    if board.count(player) == 2 and board.count(-1) == 2:
        score += 10

    if board.count(player) == 1 and board.count(-1) == 3:
        score -= 10

    if board.count(opp_piece) == 3 and board.count(-1) == 1:
        score -= 10

    return score

def evaluate(board, player):

    score = 0
    #Score (horizontally)
    for row in range(len(board)):
        new_board = [int(j) for j in board[row]]
        score += rewards(new_board, player)

    #Score (vertically)
    board_vt = []
    for row in range(len(board)):
        for i in range(len(board)-1):
            board_vt.append(board[i][row])
            score += rewards(board_vt, player)

    #Score (diagonally)
    # First diagonal (from the left to the right)
    board_dg = []
    for position in range(len(board)):
        extension = board[position][position]
        board_dg.append(extension)
        if position == (len(board)-1):
            score += rewards(board_dg, player)

    # Second diagonal (from the right to the left)
    board_dg2 = []
    for indx, position in enumerate(reversed(range(len(board)))):
        extension = board[indx][position]
        board_dg2.append(extension)
        if indx == (len(board)-1):
            score += rewards(board_dg2, player)

    return score

def check_game(board, player):
    for row in board:
        if row[0] == row[1] == row[2] == row[3] == player:
            return True

    for col in range(len(board[0])):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(check[0]) == len(check) and check[0] != 0:
            return True

    diags = []
    for indx in range(len(board)):
        diags.append(board[indx][indx])
    if diags.count(diags[0]) == len(diags) and diags[0] != 0:
        return True




def is_terminal_node(board):
    return check_game(board, -1) or check_game(board, 1) or len(valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, MaximizingPlayer):
    valid_locations = empty_cells(board)
    print("valid_locations", valid_locations)
    terminal_node = is_terminal_node(board)
    print("terminal_node", terminal_node)
    print("depth : ", depth)

    if depth == 0 or terminal_node:
        print("depth 0 or terminal_node")
        if terminal_node:
            print("terminal_node")
            if check_game(board, -1):
                print("Player wins")
                return (None, None, -1000000)

            elif check_game(board, 1):
                print("AI wins")
                return (None, None, 1000000)

            else:
                print("No one wins")
                return (None, None, 0)

        else:
            print("else")
            print("evaluate", evaluate(board,1))
            return (None, None, evaluate(board, 1))

    if MaximizingPlayer:
        value = -infinity
        x_pos = random.randint(0,3)
        y_pos = random.randint(0,3)
        max_value = -infinity
        for box in valid_locations:
            print("box", box)
            x,y = box[0], box[1]
            new_board = board.copy()
            put_in_the_box(new_board, x,y, 1)
            #print("board", board)
            #print("new board", new_board)
            max_value = max(value, minimax(new_board, depth-1, alpha, beta, False)[2])
            if max_value > value:
                value = max_value
                x_pos, y_pos = x,y
                #print(alpha)
                #print(value)
            Alpha = max(alpha, value)
                #print(alpha)
            if Alpha >= beta:
                break
        print("return")
        return (x_pos, y_pos, max_value)

    else:
        value = infinity
        x_pos = random.randint(0,3)
        y_pos = random.randint(0,3)
        min_value = infinity
        for box in valid_locations:
            print("box else", box)
            x,y = box[0], box[1]
            new_board = board.copy()
            put_in_the_box(new_board, x,y, -1)
            print("board", board)
            print("new board", new_board)
            call_minimax = minimax(new_board, depth-1, alpha, beta, True)[2]
            min_value = min(value, call_minimax)
            if min_value < value:
                value = min_value
                x_pos, y_pos = x,y
            Beta = min(beta, value)
            if alpha >= Beta:
                break
        print("return ")
        return (x_pos, y_pos, min_value)

def redraw_window():
    Win.fill(Bg)

    Grid.draw(Win)
    pygame.display.flip()

Grid = Grid()

def main():
    start = [-1,1]
    player = random.choice(start)
    run = True
    Grid.print_grid()
    board = Grid.grid2
    color = (0,255,0,0)
    alpha = -infinity
    beta = +infinity
    depth = 5
    while run:
        clock.tick(FPS)
        fill(Circle, color)

        redraw_window()
        Win.fill(pygame.Color('lightskyblue4'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and Grid.game_over:
                    Grid.reset()
                    Grid.game_over = False

            if event.type == pygame.MOUSEBUTTONDOWN and not Grid.game_over:
                #print("Yes !")
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if player == -1 and not Grid.game_over:
                        #print(pos[0] // (Width // 4), pos[1] // (Height // 4))
                        Grid.get_mouse(board, pos[0] // (Width // 4), pos[1] // (Height // 4), player)
                        if Grid.switch:
                            if player == -1:
                                player = 1
                            else:
                                player = -1
                        Grid.print_grid()

        if player == 1 and not Grid.game_over:
                x, y, score = minimax(board, depth, alpha, beta, True)
                print("called minimax")
                if good_box(board, x,y):
                    Grid.get_mouse(board, x, y, player)
                    if Grid.switch:
                        if player == -1:
                            player = 1
                        else:
                            player = -1
                    Grid.print_grid()

main()
