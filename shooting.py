import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Player settings
player_width = 50
player_height = 60
player_speed = 5

# Enemy settings
enemy_width = 50
enemy_height = 50
enemy_speed = 3

# Beam settings
beam_width = 5
beam_height = 10
beam_speed = 7

# Load player image
player_img = pygame.image.load('player.png')
player_img = pygame.transform.scale(player_img, (player_width, player_height))

# Load enemy image
enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))

# Game variables
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_lives = 3
score = 0

# Beam and enemy lists
beams = []
enemies = []

# Font
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        beams.append([player_x + player_width // 2, player_y])
    
    # Update beam positions
    for beam in beams:
        beam[1] -= beam_speed
        if beam[1] < 0:
            beams.remove(beam)
    
    # Add new enemy
    if random.randint(1, 20) == 1:
        enemies.append([random.randint(0, screen_width - enemy_width), 0])
    
    # Update enemy positions
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > screen_height:
            enemies.remove(enemy)
            player_lives -= 1
    
    # Check for collisions
    for enemy in enemies:
        for beam in beams:
            if (enemy[0] < beam[0] < enemy[0] + enemy_width and
                    enemy[1] < beam[1] < enemy[1] + enemy_height):
                enemies.remove(enemy)
                beams.remove(beam)
                score += 10
    
    # Draw everything
    screen.fill(black)
    
    # Draw player
    screen.blit(player_img, (player_x, player_y))
    
    # Draw beams
    for beam in beams:
        pygame.draw.rect(screen, white, (beam[0], beam[1], beam_width, beam_height))
    
    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))
    
    # Draw score and lives
    score_text = font.render(f'Score: {score}', True, white)
    lives_text = font.render(f'Lives: {player_lives}', True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
