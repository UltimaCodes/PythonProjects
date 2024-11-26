# Snake game in python

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game Objects
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not self.direction == DOWN:
                self.direction = UP
            elif event.key == pygame.K_DOWN and not self.direction == UP:
                self.direction = DOWN
            elif event.key == pygame.K_LEFT and not self.direction == RIGHT:
                self.direction = LEFT
            elif event.key == pygame.K_RIGHT and not self.direction == LEFT:
                self.direction = RIGHT

class Fruit:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

    def randomize_position(self):
        self.position = (random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                         random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE)

class Obstacle:
    def __init__(self):
        self.position = (0, 0)
        self.color = BLUE
        self.randomize_position()

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

    def randomize_position(self):
        self.position = (random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                         random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE)

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    fruit = Fruit()
    obstacles = [Obstacle() for _ in range(5)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            snake.handle_input(event)

        snake.update()

        # Check for collision with fruit
        if snake.get_head_position() == fruit.position:
            snake.length += 1
            snake.score += 10
            fruit.randomize_position()

        # Check for collision with obstacles
        for obstacle in obstacles:
            if snake.get_head_position() == obstacle.position:
                snake.reset()

        # Draw background
        surface.fill(WHITE)

        # Draw obstacles
        for obstacle in obstacles:
            obstacle.render(surface)

        # Draw fruit
        fruit.render(surface)

        # Draw snake
        snake.render(surface)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {snake.score}", True, (0, 0, 0))
        surface.blit(score_text, (10, 10))

        # Draw surface on the screen
        screen.blit(surface, (0, 0))
        pygame.display.update()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
