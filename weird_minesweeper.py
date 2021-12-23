import pygame, random

RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Temporary for testing
random.seed(5)

def main():
    # Setup board
    screen = pygame.display.set_mode((640,480))
    screen.fill(BLACK)
    board = [[False for i in range(10)] for j in range(10)]
    for i in range(10):
        for j in range(10):
            board[i][j] = bool(random.getrandbits(1))
            if board[i][j]:
                pygame.draw.rect(screen, RED, (i * 10, j * 10, 10, 10), 1)
    
    
    pygame.display.update()
    while True:
        print("")

if __name__ == '__main__':
    main()