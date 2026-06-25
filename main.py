import pygame
import random
from paddle import Paddle
from ball import Ball
from brick import Brick
from particle import Particle
from powerup import PowerUp

pygame.init()

# ----------------------------- CONSTANTS ----------------------------- #
RED = (251, 66, 1)
ORANGE = (239, 135, 14)
YELLOW = (254, 206, 0)
GREEN = (19, 171, 88)
BLUE = (127, 210, 250)
PINK = (255, 191, 218)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

score = 0
lives = 3

# ---------------------------- GAME INITIALIZATION ---------------------------- #
# Load high score from file or default to 0
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")

all_sprites_list = pygame.sprite.Group()

# Initialize white paddle
paddle = Paddle(WHITE, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 560

# Initialize white ball
ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

all_bricks = pygame.sprite.Group()
all_powerups = pygame.sprite.Group()
powerup_timer = 0

# Generate red bricks
for i in range(7):
    brick = Brick(RED, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)

# Generate orange bricks
for i in range(7):
    brick = Brick(ORANGE, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)

# Generate yellow bricks
for i in range(7):
    brick = Brick(YELLOW, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)

all_sprites_list.add(paddle)
all_sprites_list.add(ball)

carryOn = True
clock = pygame.time.Clock()

# -------------------------- MAIN EXECUTION --------------------------- #
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False

    # Move paddle via arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(5)
    if keys[pygame.K_RIGHT]:
        paddle.moveRight(5)

    # Tick down powerup timer and reset paddle when it hits zero
    if powerup_timer > 0:
        powerup_timer -= 1
        if powerup_timer == 0:
            paddle.reset_size(WHITE)

    # Run game update logic
    all_sprites_list.update()

    # Bounce off side walls
    if ball.rect.x >= 790:
        ball.bounce_x()
    if ball.rect.x <= 0:
        ball.bounce_x()

    # Handle ball dropping past paddle floor
    if ball.rect.y > 590:
        lives -= 1
        ball.rect.x = 345
        ball.rect.y = 195
        ball.bounce_y()

        if lives == 0:
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            screen.blit(text, (250, 300))
            pygame.display.flip()
            pygame.time.wait(3000)
            carryOn = False

    # Bounce off top ceiling border
    if ball.rect.y < 40:
        ball.bounce_y()

    # Check collisions between ball and paddle using dynamic reflection
    if pygame.sprite.collide_mask(ball, paddle):
        ball.rect.y -= ball.velocity[1]

        paddle_center = paddle.rect.x + (paddle.rect.width / 2)
        ball_center = ball.rect.x + (ball.rect.width / 2)
        hit_pos = ball_center - paddle_center

        # Change horizontal direction and intensity based on hit placement
        ball.velocity[0] = int(hit_pos / 8)
        ball.bounce_y()

    # Check collisions between ball and any bricks
    brick_collision_list = pygame.sprite.spritecollide(ball, all_bricks, False)
    for brick in brick_collision_list:
        ball.bounce_y()
        score += 1

        # Spawn 6 custom-colored explosion particles
        for _ in range(6):
            particle = Particle(brick.image.get_at((0, 0)), brick.rect.x + 40, brick.rect.y + 15)
            all_sprites_list.add(particle)

        # Spawn falling powerup on a 35 percent chance from orange or yellow rows
        if brick.image.get_at((0, 0)) in [ORANGE, YELLOW] and random.random() < 0.35:
            powerup = PowerUp(brick.image.get_at((0, 0)), brick.rect.x + 40, brick.rect.y + 15)
            all_sprites_list.add(powerup)
            all_powerups.add(powerup)

        brick.kill()

        if len(all_bricks) == 0:
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, WHITE)
            screen.blit(text, (200, 300))
            pygame.display.flip()
            pygame.time.wait(3000)
            carryOn = False

    # Check if paddle catches falling powerups
    powerup_hit_list = pygame.sprite.spritecollide(paddle, all_powerups, True)
    for powerup in powerup_hit_list:
        # Scale paddle width up to 150 pixels wide
        paddle.image = pygame.Surface([150, 10])
        paddle.image.fill(BLACK)
        paddle.image.set_colorkey(BLACK)
        pygame.draw.rect(paddle.image, WHITE, [0, 0, 150, 10])

        old_center = paddle.rect.center
        paddle.rect = paddle.image.get_rect()
        paddle.rect.center = old_center

        # Run powerup for 10 seconds total at 60 fps
        powerup_timer = 600

    # Draw phase
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

    # Render score statistics
    font = pygame.font.Font(None, 34)
    text = font.render("Score: " + str(score), 1, WHITE)
    screen.blit(text, (20, 10))
    text = font.render("High Score: " + str(high_score), 1, WHITE)
    screen.blit(text, (300, 10))
    text = font.render("Lives: " + str(lives), 1, WHITE)
    screen.blit(text, (650, 10))

    # Output sprites
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

# Check and overwrite persistent record if broken
if score > high_score:
    with open("highscore.txt", "w") as file:
        file.write(str(score))

pygame.quit()
