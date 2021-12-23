import pygame, random
import pygame.gfxdraw
from math import pi, cos, sin, sqrt, floor

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RADIUS = 20
W = 15
H = 15

# Temporary for testing
random.seed(5)

class Tile:
    def __init__(self, pos, mine):
        self.pos = pos
        self.mine = mine

def find_distance(pos1, pos2):
    return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def find_closest_tile(board, pos):
    low_distance = 99999 # Impossibly high
    closest = Tile((0, 0), False)
    for row in board:
        for tile in row:
            distance = find_distance(tile.pos, pos)
            if distance == low_distance:
                print('something went wrong')
                return None
            elif distance < low_distance:
                low_distance = distance
                closest = tile

    return closest   


# TODO: Make this more precise somehow
def find_point_pos(pos):
    return[
        (pos[0], pos[1] + RADIUS),
        (round(sqrt(3) * RADIUS / 2 + pos[0]), RADIUS / 2 + pos[1]),
        (round(sqrt(3) * RADIUS / 2 + pos[0]), -RADIUS / 2 + pos[1]),
        (pos[0], pos[1] - RADIUS),
        (round(-sqrt(3) * RADIUS / 2 + pos[0]), -RADIUS / 2 + pos[1]),
        (round(-sqrt(3) * RADIUS / 2 + pos[0]), RADIUS / 2 + pos[1]),
    ]

def draw_hexagon(surface, position, color):
    return pygame.draw.polygon(
        surface,
        color,
        find_point_pos(position)
    )

def draw_grid(surface, board):
    for row in board:
        for tile in row:
            pygame.gfxdraw.aapolygon(
                surface,
                find_point_pos(tile.pos),
                BLACK
            )


def gen_coordinates():
    board = [[Tile((0, 0), False) for i in range(W)] for j in range(H)]
    left = 0
    for i in range(W):
        for j in range(H):
            x = round(i * (RADIUS * sqrt(3)) + RADIUS)
            y = j * (3 * RADIUS / 2) + RADIUS
            if j % 2:
                x += floor(RADIUS / 2 * sqrt(3))
            board[i][j].pos = (x, y)
            board[i][j].mine = bool(random.getrandbits(1))
    
    return board

def main():
    # Setup board
    screen = pygame.display.set_mode((640,480))
    screen.fill(BLACK)
    board = gen_coordinates()
    for row in board:
        for tile in row:
            if tile.mine:
                draw_hexagon(screen, tile.pos, RED)
            else:
                draw_hexagon(screen, tile.pos, WHITE)
    
    draw_grid(screen, board)
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                tile = find_closest_tile(board, pos)

                # If in the middle of two tiles
                if tile is None:
                    continue

                if tile.mine:
                    print('mine')
                else:
                    print('safe')
        

if __name__ == '__main__':
    main()