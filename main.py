import pygame
from random import choice

WIDTH = 723
HEIGHT = 572
RES = WIDTH, HEIGHT

TILE = 30
cols, rows = WIDTH // TILE, HEIGHT // TILE
FPS = 30
waiting_time = 10

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(RES)
pygame.display.set_caption("Labirint generator")
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.color = pygame.Color('black')

    def draw_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(screen, pygame.Color('brown'), (x + 2, y + 2, TILE-2 , TILE - 2))

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(screen, self.color, (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color('orange'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('orange'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color('orange'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('orange'), (x, y), (x, y + TILE), 2)

    def check_cell(self, x, y):
        find_index = lambda x, y: x + (y * cols)
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_Neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        left = self.check_cell(self.x - 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        right = self.check_cell(self.x + 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if left and not left.visited:
            neighbors.append(left)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if right and not right.visited:
            neighbors.append(right)
        return choice(neighbors) if neighbors else False

def find_path(cell, end_cell):
    stack = [cell]
    visited = set()
    prev = {}

    while stack:
        current = stack.pop()
        if current == end_cell:
            break

        visited.add(current)
        neighbors = [current.check_cell(current.x + dx, current.y + dy) for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]]
        for neighbor in neighbors:
            if neighbor and neighbor not in visited and not any(neighbor.walls.values()):
                stack.append(neighbor)
                prev[neighbor] = current

    path = []
    while end_cell:
        path.append(end_cell)
        end_cell = prev.get(end_cell)

    for cell in path:
        cell.color = pygame.Color('red')

    return path

def remove_walls(current, next):
    dx = current.x - next.x
    dy = current.y - next.y
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    if dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    if dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

start_cell = grid_cells[0]
end_cell = grid_cells[-1]

current_cell = start_cell
stack = []
timer = 0

running = True
while running:
    screen.fill(pygame.Color("springgreen4"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_cell()

    next_cell = current_cell.check_Neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()
    if not stack and not hasattr(start_cell, 'path_generated'):
        find_path(start_cell, end_cell)
        start_cell.path_generated = True

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
