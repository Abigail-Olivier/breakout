import pygame
import random

# ----------------------------- FUNCTIONS ----------------------------- #
class Particle(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()

        # Create small square particle texture matching parent brick color
        self.image = pygame.Surface([5, 5])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        # Calculate random explosive physics speeds
        self.velocity_x = random.randint(-4, 4)
        self.velocity_y = random.randint(-6, -1)

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Simulate gravitational pull downwards
        self.velocity_y += 0.3

        # Terminate sprite execution loop when dropping off-screen
        if self.rect.y > 600:
            self.kill()
