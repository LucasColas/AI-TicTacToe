import pygame
import sys
import os

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

        self.search_dirs = [(0,-1), (-1,-1), (-1,0), (-1,-1), (0,1), (1,1), (1,0), (1,-1)]


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
        if self.get_cell_value(x,y) == 0:
            self.switch = True

            if player == "X":
                self.set_cell_value(x,y, 1)
            elif player == "O":
                self.set_cell_value(x, y, -1)
            #self.check(x,y, player)
            self.check_columns(player)

        else:
            self.switch = False

    def check_columns(self, player):
        for x in self.grid2:
            for y in self.grid2:
                print(y)



    def check_within_bounds(self, x, y):
        return x >= 0 and x < 4 and y >= 0 and y < 4

    def check(self, x,y, player):
        """
        count = 1
        for indx, (dirx, diry) in enumerate(self.search_dirs):
            if self.check_within_bounds(x+dirx, y+diry) and self.get_cell_value(x+dirx, y+diry) == player:
                print("Yes, check")
                count += 1
                print("first", count)
                xx = x + dirx
                yy = y + diry

                if self.check_within_bounds(xx+dirx, yy+diry) and self.get_cell_value(xx+dirx, yy+diry) == player:
                    count += 1
                    print("second",count)
                    if count == 4:
                        print("count", count)
                        break
                if count < 4:
                    print("check")

                    new_dir = 0
                    if indx == 0:
                        new_dir = self.search_dirs[4]
                    elif indx == 1:
                        new_dir = self.search_dirs[5]
                    elif indx == 2:
                        new_dir = self.search_dirs[6]
                    elif indx == 3:
                        new_dir = self.search_dirs[7]
                    elif indx == 4:
                        new_dir = self.search_dirs[0]
                    elif indx == 5:
                        new_dir = self.search_dirs[1]
                    elif indx == 6:
                        new_dir = self.search_dirs[2]
                    elif indx == 7:
                        new_dir = self.search_dirs[3]

                    if self.check_within_bounds(x + new_dir[0], y + new_dir[1]) and self.get_cell_value(x + new_dir[0], y + new_dir[1]) == player:
                        count += 1
                        print("third",count)
                        if count == 4:
                            break
                    else:
                        count = 1
                        print("fourth", count)

        if count == 4:
            print(player, 'wins')

        """
        pass




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
    color = (0,255,0,0)
    while run:
        clock.tick(FPS)
        fill(Circle, color)

        redraw_window()
        Win.fill(pygame.Color('lightskyblue4'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print("Yes !")

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    #print(pos[0] // (Width // 4), pos[1] // (Height // 4))
                    Grid.get_mouse(pos[0] // (Width // 4), pos[1] // (Height // 4), player)
                    if Grid.switch:
                        if player == "X":
                            player = "O"
                        else:
                            player = "X"
                    Grid.print_grid()


ui()
