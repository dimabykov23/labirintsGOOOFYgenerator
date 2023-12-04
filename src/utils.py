import pygame


def find_path(cell, end_cell):
    stack = [cell]
    visited = set()
    prev = {}

    while stack:
        current = stack.pop()

        if current == end_cell:
            break

        visited.add(current)
        neighbors = [current.check_cell(current.x + dx, current.y + dy) for dx, dy in
                     [(0, -1), (-1, 0), (0, 1), (1, 0)]]

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


def remove_walls(current_cell, next_cell):
    dx = current_cell.x - next_cell.x
    dy = current_cell.y - next_cell.y

    if dx == 1:
        current_cell.walls['left'] = False
        next_cell.walls['right'] = False

    if dx == -1:
        current_cell.walls['right'] = False
        next_cell.walls['left'] = False

    if dy == 1:
        current_cell.walls['top'] = False
        next_cell.walls['bottom'] = False

    if dy == -1:
        current_cell.walls['bottom'] = False
        next_cell.walls['top'] = False
