import pygame

# ----------------------------- FUNCTIONS ----------------------------- #
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()

        # Formulate matching colored dropping item container
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.speed = 3

    def update(self):
        # Move straight down toward player space
        self.rect.y += self.speed

        # Clear object instance if missed completely
        if self.rect.y > 600:
            self.kill()
