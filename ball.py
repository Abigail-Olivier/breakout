import pygame
from random import randint

BLACK = (0, 0, 0)

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        # Create the ball surface and handle transparency
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the square ball
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Set random initial physics speed
        self.velocity = [randint(4, 8), randint(-8, 8)]

        # Get the rect object for positioning
        self.rect = self.image.get_rect()

    def update(self):
        # Update ball position based on speed
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce_y(self):
        # Invert vertical speed for paddle and brick hits
        self.velocity[1] = -self.velocity[1]
        self.velocity[0] = randint(-8, 8)

    def bounce_x(self):
        # Invert horizontal speed for wall hits
        self.velocity[0] = -self.velocity[0]
