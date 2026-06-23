import pygame

BLACK = (0, 0, 0)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        # Create paddle base and transparency layers
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < 0:
            self.rect.x = 0

    def moveRight(self, pixels):
        self.rect.x += pixels
        # Dynamically evaluate width limits so wide paddle stops accurately
        if self.rect.x > 800 - self.rect.width:
            self.rect.x = 800 - self.rect.width

    def reset_size(self, color):
        # Reset canvas specifications back to 100 wide
        self.image = pygame.Surface([100, 10])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, 100, 10])

        # Preserve position center points to eliminate jumping bugs
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
