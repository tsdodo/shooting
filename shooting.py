import pygame
import random
import time

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

# 爆発設定
explosion_duration = 30  # 爆発が表示されるフレーム数

# 効果音の読み込み
player_explosion_sound = pygame.mixer.Sound('player_explosion.mp3')
enemy_explosion_sound = pygame.mixer.Sound('enemy_explosion.mp3')
beam_fire_sound = pygame.mixer.Sound('beam_fire.mp3')

# BGMの読み込み
background_music = 'background_music.mp3'
game_over_music = 'game_over_music.mp3'

# BGMの再生
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # ループ再生

# プレイヤー画像の読み込み
player_img = pygame.image.load('player.png')
player_img = pygame.transform.scale(player_img, (player_width, player_height))

# プレイヤーのマスク作成
player_mask = pygame.mask.from_surface(player_img)

# 敵画像の読み込み
enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))

# 敵のマスク作成
enemy_mask = pygame.mask.from_surface(enemy_img)

# 爆発画像の読み込み
explosion_img = pygame.image.load('explosion.png')
explosion_img = pygame.transform.scale(explosion_img, (player_width, player_height))

# ゲームの変数
player_x = 10
player_y = screen_height // 2 - player_height // 2
player_lives = 3
score = 0

# ビームと敵のリスト
beams = []
enemy_beams = []
enemies = []
explosions = []  # 爆発のリスト

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
    global player_x, player_y, beams, enemy_beams, enemies, explosions, player_lives, score
    player_x = 10
    player_y = screen_height // 2 - player_height // 2
    beams = []
    enemy_beams = []
    enemies = []
    explosions = []
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)  # ゲーム再開時に元のBGMを再生

def draw_explosions():
    for explosion in explosions[:]:
        screen.blit(explosion_img, (explosion[0], explosion[1]))
        explosion[2] -= 1
        if explosion[2] <= 0:
            explosions.remove(explosion)
    pygame.display.flip()

def check_collision(mask1, x1, y1, mask2, x2, y2):
    offset_x = x2 - x1
    offset_y = y2 - y1
    return mask1.overlap(mask2, (offset_x, offset_y)) is not None

# ゲームループ
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = event.pos
            if retry_button_rect.collidepoint(mouse_pos):
                reset_game()
                game_over = False
            elif quit_button_rect.collidepoint(mouse_pos):
                running = False
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected_button = 'retry' if selected_button == 'quit' else 'quit'
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
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
            beam_fire_sound.play()  # ビーム発射音を再生
        
        # ビームの位置更新
        for beam in beams[:]:
            beam[0] += beam_speed
            if beam[0] > screen_width:
                beams.remove(beam)
        
        # 新しい敵を追加
        if random.randint(1, 20) == 1:
            enemies.append([screen_width, random.randint(0, screen_height - enemy_height)])
        
        # 敵の位置更新
        for enemy in enemies[:]:
            enemy[0] -= enemy_speed
            if random.randint(1, 50) == 1:
                enemy_beams.append([enemy[0], enemy[1] + enemy_height // 2])
            if enemy[0] < 0:
                enemies.remove(enemy)
        
        # 敵ビームの位置更新
        for enemy_beam in enemy_beams[:]:
            enemy_beam[0] -= enemy_beam_speed
            if enemy_beam[0] < 0:
                enemy_beams.remove(enemy_beam)
        
        # 衝突判定
        player_hit = False
        enemies_to_remove = []
        beams_to_remove = []
        enemy_beams_to_remove = []

        for enemy in enemies:
            for beam in beams:
                if check_collision(enemy_mask, enemy[0], enemy[1], pygame.mask.Mask((beam_width, beam_height), True), beam[0], beam[1]):
                    explosions.append([enemy[0], enemy[1], explosion_duration])
                    enemies_to_remove.append(enemy)
                    beams_to_remove.append(beam)
                    score += 10
                    enemy_explosion_sound.play()  # 敵機の爆発音を再生

            if check_collision(player_mask, player_x, player_y, enemy_mask, enemy[0], enemy[1]):
                explosions.append([enemy[0], enemy[1], explosion_duration])
                enemies_to_remove.append(enemy)
                player_lives -= 1
                player_hit = True
                player_explosion_sound.play()  # プレイヤー機の爆発音を再生
                if player_lives == 0:
                    game_over = True
                    pygame.mixer.music.load(game_over_music)
                    pygame.mixer.music.play(-1)  # ゲームオーバー時に別のBGMを再生

        for enemy_beam in enemy_beams:
            if check_collision(player_mask, player_x, player_y, pygame.mask.Mask((beam_width, beam_height), True), enemy_beam[0], enemy_beam[1]):
                explosions.append([player_x, player_y, explosion_duration])
                enemy_beams_to_remove.append(enemy_beam)
                player_lives -= 1
                player_hit = True
                player_explosion_sound.play()  # プレイヤー機の爆発音を再生
                if player_lives == 0:
                    game_over = True
                    pygame.mixer.music.load(game_over_music)
                    pygame.mixer.music.play(-1)  # ゲームオーバー時に別のBGMを再生

        # リスト外で削除
        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)
        for beam in beams_to_remove:
            if beam in beams:
                beams.remove(beam)
        for enemy_beam in enemy_beams_to_remove:
            if enemy_beam in enemy_beams:
                enemy_beams.remove(enemy_beam)

        # 爆発の更新
        draw_explosions()

        if player_hit and not game_over:
            draw_explosions()  # 爆発を描画して更新
            pygame.display.flip()
            time.sleep(3)  # 3秒間スリープ
            reset_game()

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
