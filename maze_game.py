
import pygame
import random

# -----------------------------
# Constants
# -----------------------------
CELL_SIZE = 20
MAZE_WIDTH = 21  # Must be odd
MAZE_HEIGHT = 21  # Must be odd
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE + 40  # Extra space for timer

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
GREEN = (0, 200, 0)
GRAY = (200, 200, 200)

# Directions: (dx, dy)
DIRS = [(0, -2), (0, 2), (-2, 0), (2, 0)]


# -----------------------------
# Maze Generator (DFS)
# -----------------------------
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        maze[y][x] = 0
        dirs = DIRS[:]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0
                carve(nx, ny)

    carve(1, 1)
    maze[height - 2][width - 2] = 0  # Ensure exit
    return maze


# -----------------------------
# Game Initialization
# -----------------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Escape with Timer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
player_pos = [1, 1]
exit_pos = [MAZE_WIDTH - 2, MAZE_HEIGHT - 2]
start_ticks = pygame.time.get_ticks()
game_over = False
elapsed_time = 0


# -----------------------------
# Drawing Functions
# -----------------------------
def draw_maze():
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE)
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, rect)


def draw_player():
    rect = pygame.Rect(player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, BLUE, rect)


def draw_exit():
    rect = pygame.Rect(exit_pos[0] * CELL_SIZE, exit_pos[1] * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, GREEN, rect)


def draw_timer(seconds):
    timer_text = font.render(f"Time: {seconds:.1f}s", True, GRAY)
    screen.blit(timer_text, (10, 5))


# -----------------------------
# Game Loop
# -----------------------------
running = True
while running:
    clock.tick(30)
    screen.fill(BLACK)

    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000.0

    draw_maze()
    draw_exit()
    draw_player()
    draw_timer(elapsed_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        elif keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1

        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
            if maze[new_y][new_x] == 0:
                player_pos = [new_x, new_y]

        if player_pos == exit_pos:
            game_over = True
            print(f"탈출 성공! 걸린 시간: {elapsed_time:.2f}초")

    pygame.display.flip()

pygame.quit()