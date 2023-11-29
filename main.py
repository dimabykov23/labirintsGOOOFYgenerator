import pygame

from config import Config
from cell import Cell
from utils import remove_walls, find_path

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(Config.RES)
    pygame.display.set_caption("Labirint generator")
    clock = pygame.time.Clock()

    grid_cells = [Cell(col, row) for row in range(Config.rows) for col in range(Config.cols)]

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

        for cell in grid_cells:
            cell.draw(screen)

        current_cell.visited = True
        current_cell.draw_cell(screen)

        next_cell = current_cell.check_neighbors(grid_cells)

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
        clock.tick(Config.FPS)

    pygame.quit()
