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
green = (0, 255, 0)
blue = (0, 0, 255)

# プレイヤー設定
player_width = 50
player_height = 60
player_speed = 5

# 敵設定
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemy_beam_speed = 5

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
player_x = 10
player_y = screen_height // 2 - player_height // 2
player_lives = 3
score = 0

# ビームと敵のリスト
beams = []
enemy_beams = []
enemies = []

# フォント設定
font = pygame.font.Font(None, 36)

# ボタンの設定
button_font = pygame.font.Font(None, 48)
retry_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
quit_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 60, 200, 50)
selected_button = 'retry'

def show_game_over():
    screen.fill(black)
    game_over_text = font.render("GAME OVER", True, white)
    screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 50))

    # リトライボタン
    pygame.draw.rect(screen, green if selected_button == 'retry' else white, retry_button_rect)
    retry_text = button_font.render("Retry", True, black)
    screen.blit(retry_text, (retry_button_rect.x + 50, retry_button_rect.y + 5))

    # 終了ボタン
    pygame.draw.rect(screen, green if selected_button == 'quit' else white, quit_button_rect)
    quit_text = button_font.render("Quit", True, black)
    screen.blit(quit_text, (quit_button_rect.x + 60, quit_button_rect.y + 5))

    pygame.display.flip()

def reset_game():
    global player_x, player_y, player_lives, score, beams, enemy_beams, enemies
    player_x = 10
    player_y = screen_height // 2 - player_height // 2
    player_lives = 3
    score = 0
    beams = []
    enemy_beams = []
    enemies = []

# ゲームループ
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected_button = 'retry' if selected_button == 'quit' else 'quit'
                if event.key == pygame.K_SPACE:
                    if selected_button == 'retry':
                        reset_game()
                        game_over = False
                    elif selected_button == 'quit':
                        running = False
    
    if not game_over:
        # プレイヤーの移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < screen_height - player_height:
            player_y += player_speed
        if keys[pygame.K_SPACE]:
            beams.append([player_x + player_width, player_y + player_height // 2])
        
        # ビームの位置更新
        for beam in beams:
            beam[0] += beam_speed
            if beam[0] > screen_width:
                beams.remove(beam)
        
        # 新しい敵を追加
        if random.randint(1, 20) == 1:
            enemies.append([screen_width, random.randint(0, screen_height - enemy_height)])
        
        # 敵の位置更新
        for enemy in enemies:
            enemy[0] -= enemy_speed
            if random.randint(1, 50) == 1:
                enemy_beams.append([enemy[0], enemy[1] + enemy_height // 2])
            if enemy[0] < 0:
                enemies.remove(enemy)
        
        # 敵ビームの位置更新
        for enemy_beam in enemy_beams:
            enemy_beam[0] -= enemy_beam_speed
            if enemy_beam[0] < 0:
                enemy_beams.remove(enemy_beam)
        
        # 衝突判定
        for enemy in enemies:
            for beam in beams:
                if (enemy[0] < beam[0] < enemy[0] + enemy_width and
                        enemy[1] < beam[1] < enemy[1] + enemy_height):
                    enemies.remove(enemy)
                    beams.remove(beam)
                    score += 10
            if (enemy[0] < player_x + player_width and
                    enemy[0] + enemy_width > player_x and
                    enemy[1] < player_y + player_height and
                    enemy[1] + enemy_height > player_y):
                enemies.remove(enemy)
                player_lives -= 1
                if player_lives == 0:
                    game_over = True
        
        for enemy_beam in enemy_beams:
            if (enemy_beam[0] < player_x + player_width and
                    enemy_beam[0] + beam_width > player_x and
                    enemy_beam[1] < player_y + player_height and
                    enemy_beam[1] + beam_height > player_y):
                enemy_beams.remove(enemy_beam)
                player_lives -= 1
                if player_lives == 0:
                    game_over = True
        
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
        
        # 敵ビームの描画
        for enemy_beam in enemy_beams:
            pygame.draw.rect(screen, red, (enemy_beam[0], enemy_beam[1], beam_width, beam_height))
        
        # スコアとライフの描画
        score_text = font.render(f'Score: {score}', True, white)
        lives_text = font.render(f'Lives: {player_lives}', True, white)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        
        pygame.display.flip()
        clock.tick(60)
    else:
        show_game_over()

pygame.quit()
