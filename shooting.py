import pygame
import random

# Pygameの初期化
pygame.init()

# 画面のサイズ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 色の定義
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# プレイヤー設定
player_width = 50
player_height = 60
player_speed = 5

# 敵設定
enemy_width = 50
enemy_height = 50
enemy_speed = 3

# ビーム設定
beam_width = 5
beam_height = 10
beam_speed = 7

# プレイヤー画像の読み込み
player_img = pygame.Surface((player_width, player_height))
player_img.fill(white)  # 仮のプレイヤー画像として白い四角を使用

# 敵画像の読み込み
enemy_img = pygame.Surface((enemy_width, enemy_height))
enemy_img.fill(red)  # 仮の敵画像として赤い四角を使用

# ゲームの変数
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_lives = 3
score = 0

# ビームと敵のリスト
beams = []
enemies = []

# フォント設定
font = pygame.font.Font(None, 36)

# ゲームループ
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # プレイヤーの移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        beams.append([player_x + player_width // 2, player_y])
    
    # ビームの位置更新
    for beam in beams:
        beam[1] -= beam_speed
        if beam[1] < 0:
            beams.remove(beam)
    
    # 新しい敵を追加
    if random.randint(1, 20) == 1:
        enemies.append([random.randint(0, screen_width - enemy_width), 0])
    
    # 敵の位置更新
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > screen_height:
            enemies.remove(enemy)
            player_lives -= 1
    
    # 衝突判定
    for enemy in enemies:
        for beam in beams:
            if (enemy[0] < beam[0] < enemy[0] + enemy_width and
                    enemy[1] < beam[1] < enemy[1] + enemy_height):
                enemies.remove(enemy)
                beams.remove(beam)
                score += 10
    
    # 画面の描画
    screen.fill(black)
    
    # プレイヤーの描画
    screen.blit(player_img, (player_x, player_y))
    
    # ビームの描画
    for beam in beams:
        pygame.draw.rect(screen, white, (beam[0], beam[1], beam_width, beam_height))
    
    # 敵の描画
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))
    
    # スコアとライフの描画
    score_text = font.render(f'Score: {score}', True, white)
    lives_text = font.render(f'Lives: {player_lives}', True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
