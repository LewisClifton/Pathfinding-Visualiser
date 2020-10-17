import pygame
from tkinter import ttk
import tkinter as tk
import main
import dijkstra

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (190, 190, 190)
BLUE = (0,0,200)
LIGHT_BLUE = (150,150,255)

INFINITY = 9999


class Game:

    def __init__(self, screen):

        self.screen = screen

        self.gameOver = False

        self.start = [0,0]
        self.end = [12,12]

        self.grid = [[INFINITY for i in range(main.XSQUARES)] for j in range(main.YSQUARES)]
        self.grid[self.start[0]][self.start[1]] = 0
        self.grid[self.end[0]][self.end[1]] = -1

        self.start_dragging = False
        self.end_dragging = False
        self.left_dragging = False
        self.right_dragging = False

        self.walls = []
        self.distance = INFINITY
        self.route = []

        self.dijkstras = None
        self.astar = None

        self.update_screen()



    def process_events(self):

        if not self.gameOver:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.handle_right_clicks()
                        self.right_dragging = True
                    elif event.button == 1:
                        self.handle_left_clicks()
                        self.left_dragging = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.left_dragging:
                        self.left_dragging = False
                    if self.right_dragging:
                        self.right_dragging = False
                    if self.start_dragging:
                        self.start_dragging = False
                    if self.end_dragging:
                        self.end_dragging = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.left_dragging:
                        self.handle_left_clicks()
                    if self.right_dragging:
                        self.handle_right_clicks()
                    if self.start_dragging:
                        x, y = pygame.mouse.get_pos()
                        x, y = x // main.SQUAREWIDTH, y // main.SQUAREWIDTH
                        if [y, x] != self.end:
                            self.start = [y, x]
                    if self.end_dragging:
                        x, y = pygame.mouse.get_pos()
                        x, y = x // main.SQUAREWIDTH, y // main.SQUAREWIDTH
                        if [y, x] != self.start:
                            self.end = [y, x]

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.do_dijkstra()
                    if event.key == pygame.K_r:
                        self.reset_grid()

                if event.type == pygame.QUIT:
                    return True

        return False

    def update_screen(self):
        self.screen.fill(BLACK)

        for i in range(main.YSQUARES):
            for j in range(main.XSQUARES):
                rect = pygame.Rect(j * main.SQUAREWIDTH, i * main.SQUAREWIDTH, main.SQUAREWIDTH, main.SQUAREWIDTH)
                if [i, j] == self.start:
                    pygame.draw.rect(self.screen, GREEN, rect, 0)
                elif [i, j] == self.end:
                    pygame.draw.rect(self.screen, RED, rect, 0)
                elif self.grid[i][j] == -2:
                    pygame.draw.rect(self.screen, GREY, rect, 0)
                elif self.grid[i][j] == INFINITY:
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
                elif [i, j] in self.route:
                    pygame.draw.rect(self.screen, LIGHT_BLUE, rect, 0)
                else:
                    pygame.draw.rect(self.screen, BLUE, rect, 1)

    def handle_left_clicks(self):
        x, y = pygame.mouse.get_pos()
        x, y = x // main.SQUAREWIDTH, y // main.SQUAREWIDTH
        if self.grid[y][x] == INFINITY and not self.start_dragging and not self.end_dragging:
            self.grid[y][x] = -2
            self.walls.append([y,x])
        if [y, x] == self.start:
            self.start_dragging = True
            self.grid[y][x] = INFINITY
            self.start = [y, x]
        elif [y, x] == self.end:
            self.end_dragging = True
            self.grid[y][x] = INFINITY
            self.end = [y, x]

        self.update_screen()

    def handle_right_clicks(self):
        x, y = pygame.mouse.get_pos()
        x, y = x // main.SQUAREWIDTH, y // main.SQUAREWIDTH
        if self.grid[y][x] == -2:
            self.grid[y][x] = INFINITY
            self.walls.remove([y, x])

        self.update_screen()

    def display_frame(self):
        pygame.display.flip()

    def reset_grid(self):
        self.grid = [[INFINITY for i in range(main.XSQUARES)] for j in range(main.YSQUARES)]
        self.grid[self.start[0]][self.start[1]] = 0
        self.grid[self.end[0]][self.end[1]] = -1
        self.route = []
        self.walls = []

        self.update_screen()
        self.display_frame()

    def do_dijkstra(self):
        import time
        self.dijkstras = dijkstra.Dijkstras(self.grid, self.start, self.end, self.walls)

        for row in self.grid:
            while -1 in row:
                self.grid = next(self.dijkstras.main())
                self.update_screen()
                self.display_frame()
                time.sleep(0.1)
            self.grid[self.end[0]][self.end[1]] = -1

        self.route, self.distance = self.dijkstras.get_route()
        self.update_screen()
        self.display_frame()

    def do_astar(self):
        pass