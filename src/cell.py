from random import choice

import pygame

from config import Config


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.color = pygame.Color('black')

    def draw_cell(self, screen):
        x = self.x * Config.TILE
        y = self.y * Config.TILE
        pygame.draw.rect(screen, pygame.Color('brown'), (x + 2, y + 2, Config.TILE - 2, Config.TILE - 2))

    def draw(self, screen):
        x = self.x * Config.TILE
        y = self.y * Config.TILE

        if self.visited:
            pygame.draw.rect(screen, self.color, (x, y, Config.TILE, Config.TILE))

        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color('orange'), (x, y), (x + Config.TILE, y), 2)

        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('orange'), (x + Config.TILE, y), (x + Config.TILE, y + Config.TILE),
                             2)

        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color('orange'), (x + Config.TILE, y + Config.TILE), (x, y + Config.TILE),
                             2)

        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('orange'), (x, y), (x, y + Config.TILE), 2)

    def check_cell(self, x, y, grid_cells):
        find_index = lambda x, y: x + (y * Config.cols)

        if x < 0 or x > Config.cols - 1 or y < 0 or y > Config.rows - 1:
            return False

        return grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, grid_cells)
        left = self.check_cell(self.x - 1, self.y, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, grid_cells)
        right = self.check_cell(self.x + 1, self.y, grid_cells)

        if top and not top.visited:
            neighbors.append(top)

        if left and not left.visited:
            neighbors.append(left)

        if bottom and not bottom.visited:
            neighbors.append(bottom)

        if right and not right.visited:
            neighbors.append(right)

        return choice(neighbors) if neighbors else False
