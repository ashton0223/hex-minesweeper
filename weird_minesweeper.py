import pygame, random
import pygame.gfxdraw
from math import pi, cos, sin, sqrt, floor

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
YELLOW = (255, 255, 0)
RADIUS = 20
LEFT = 1
RIGHT = 3
W = 15
H = 15

# Temporary for testing
random.seed(5)

class Tile:
    def __init__(self, pos, board_pos, mine):
        self.pos = pos
        self.mine = mine
        self.board_pos = board_pos
        self.revealed = False
        self.flagged = False

def find_distance(pos1, pos2):
    if pos1 == pos2:
        return 0
    else:
        return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def find_closest_tile(board, pos):
    low_distance = 99999 # Impossibly high
    closest = Tile((0, 0), (0, 0), False)
    for row in board:
        for tile in row:
            distance = find_distance(tile.pos, pos)
            if distance == low_distance:
                # Center of a tile is equidistant from other tiles
                if low_distance > RADIUS:
                    continue
                return None
            elif distance < low_distance:
                low_distance = distance
                closest = tile

    return closest   

def find_nearby_tiles(tile, board):
    nearby = []
    x, y = tile.board_pos
    if x > 0:
        nearby.append(board[x - 1][y])
    if x < W - 1:
        nearby.append(board[x + 1][y])
    if y > 0:
        nearby.append(board[x][y - 1])
    if y < H - 1:
        nearby.append(board[x][y + 1])
    if y % 2 == 0 and x > 0:
        if y < H - 1:
            nearby.append(board[x - 1][y + 1])
        if y > 0:
            nearby.append(board[x - 1][y - 1])
    if y % 2 != 0 and x < W - 1:
        if y < H - 1:
            nearby.append(board[x + 1][y + 1])
        if y > 0:
            nearby.append(board[x + 1][y - 1])
    return nearby

def find_nearby_mines(tiles):
    mines = 0
    for tile in tiles:
        if tile.mine:
            mines += 1
    return mines

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
    board = [[Tile((0, 0), (0, 0), False) for i in range(W)] for j in range(H)]
    left = 0
    for i in range(W):
        for j in range(H):
            x = round(i * (RADIUS * sqrt(3)) + RADIUS)
            y = j * (3 * RADIUS / 2) + RADIUS
            if j % 2:
                x += floor(RADIUS / 2 * sqrt(3))
            board[i][j].pos = (x, y)
            num = random.randint(0, 4)
            board[i][j].mine = num == 0
            board[i][j].board_pos = (i, j)
    
    return board

def reveal(screen, board, tile):
    if tile.mine:  
        print('mine')
    else:
        print('safe')
        draw_hexagon(screen, tile.pos, GREY)
        draw_grid(screen, board) #TODO: Replace with single hex
        nearby_tiles = find_nearby_tiles(tile, board)
        mines = find_nearby_mines(nearby_tiles)
        x, y = tile.board_pos
        board[x][y].revealed = True
        if mines != 0:
            font = pygame.font.SysFont('arial', H * 2)
            text = font.render(str(mines), True, (0, 0, 0))
            aligned_pos = (tile.pos[0] - (RADIUS / 2), tile.pos[1] - RADIUS)
            screen.blit(text, aligned_pos)
        else:
            for nearby_tile in nearby_tiles:
                if not nearby_tile.revealed:
                    board = reveal(screen, board, nearby_tile)
    return board
                
def flag(screen, board, tile):
    x, y = tile.board_pos
    board[x][y].flagged = not board[x][y].flagged
    draw_hexagon(screen, tile.pos, YELLOW)
    draw_grid(screen, board)
    return board

def main():
    # Init pygame
    pygame.init()

    # Setup board
    screen = pygame.display.set_mode((640,480))
    screen.fill(BLACK)
    board = gen_coordinates()
    for row in board:
        for tile in row:
            draw_hexagon(screen, tile.pos, WHITE)
    
    draw_grid(screen, board)
    
    pygame.display.update()
    
    hold_tile_left = None
    hold_tile_right = None

    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    hold_tile_left = find_closest_tile(board, pos)
                elif event.button == RIGHT:
                    hold_tile_right = find_closest_tile(board, pos)
                    print('test')
            elif event.type == pygame.MOUSEBUTTONUP:
                tile = find_closest_tile(board, pos)
                if tile is None:
                    continue
                if event.button == LEFT and hold_tile_left is not None and hold_tile_left == tile:
                    board = reveal(screen, board, tile)   
                elif event.button == RIGHT and hold_tile_right is not None and hold_tile_right == tile:
                    board = flag(screen, board, tile) 
                pygame.display.update()
        

if __name__ == '__main__':
    main()