import pygame
import sys
import os

pygame.font.init()

Width, Height = 750, 750

Win = pygame.display.set_mode((Width, Height))
Bg = (0,255,255)

Cross = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cross")), (Width//4, Height//4))
Cirlce = pygame.transform.scale(pygame.image.load(os.path.join("assets", "circle")), (Width//4, Height//4))

clock = pygame.time.Clock()
FPS = 80

class Grid():
    def __init__(self):
        self.grid = [((0, Height//4), (Width, Height//4)), ((0, (2*Height)//4), (Width, (2*Height)//4)), ((0, (3*Height)//4), (Width, (3*Height)//4)), ((Width//4, 0), (Width//4, Height)), (((2*Width)//4, 0), ((2*Width)//4, Height)), (((3*Width)//4,0), ((3*Width)//4, Height))]

        self.grid2 = [[0 for x in range(4)] for y in range(4)]


    def draw(self, window):
        for line in self.grid:
            pygame.draw.line(window, (255, 255, 255), line[0], line[1], 2)

    def get_cell_value(self, x,y):
        return self.grid2[y][x]

    def set_cell_value(self, x, y, value):
        self.grid2[y][x] = value

    def get_mouse(self, x, y, player):
        if player == "X":
            self.set_cell_value(x, y, "X")
        elif player == "O":
            self.set_cell_value(x,y, "O")

    def print_grid(self):
        for row in self.grid2:
            print(row)

Grid = Grid()


def redraw_window():
    Win.fill(Bg)

    Grid.draw(Win)
    pygame.display.flip()


def ui():
    player = "X"
    run = True
    Grid.print_grid()
    while run:
        clock.tick(FPS)

        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print("Yes !")

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    #print(pos[0] // (Width // 4), pos[1] // (Height // 4))
                    Grid.get_mouse(pos[0] // (Width // 4), pos[1] // (Height // 4), player)
                    if player == "X":
                        player = "O"
                    else:
                        player = "X"
                    Grid.print_grid()


ui()
