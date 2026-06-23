import pygame

BLACK = (0, 0, 0)

class Brick(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        # Create the brick surface and handle transparency
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the brick rectangle
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Get the rect object for positioning
        self.rect = self.image.get_rect()
