import pygame
import random
import time

# Pygameの初期化
pygame.init()

# 画面の設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 定数の定義
INITIAL_LIVES = 3  # プレイヤーの初期ライフ
INITIAL_SCORE = 0  # 初期スコア
SCORE_PER_HIT = 10  # 敵にビームが当たった時のスコア
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
INITIAL_PLAYER_X = 10  # プレイヤーの初期X位置
INITIAL_PLAYER_Y = SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2  # プレイヤーの初期Y位置
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_SPEED = 3
ENEMY_BEAM_SPEED = 5
BEAM_WIDTH = 5
BEAM_HEIGHT = 10
BEAM_SPEED = 7
EXPLOSION_DURATION = 30  # 爆発が表示されるフレーム数

# 効果音の読み込み
player_explosion_sound = pygame.mixer.Sound('player_explosion.mp3')
enemy_explosion_sound = pygame.mixer.Sound('enemy_explosion.mp3')
beam_fire_sound = pygame.mixer.Sound('beam_fire.mp3')

# BGMの読み込み
BACKGROUND_MUSIC = 'background_music.mp3'
GAME_OVER_MUSIC = 'game_over_music.mp3'

# BGMの再生
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.play(-1)  # ループ再生

# プレイヤー画像の読み込み
player_img = pygame.image.load('player.png')
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

# プレイヤーのマスク作成（衝突判定用）
player_mask = pygame.mask.from_surface(player_img)

# 敵画像の読み込み
enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))

# 敵のマスク作成（衝突判定用）
enemy_mask = pygame.mask.from_surface(enemy_img)

# 爆発画像の読み込み
explosion_img = pygame.image.load('explosion.png')
explosion_img = pygame.transform.scale(explosion_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

# フォント設定
font = pygame.font.Font(None, 36)  # スコアやライフ表示用のフォント

# ボタンの設定
button_font = pygame.font.Font(None, 48)  # ボタン用のフォント
retry_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)  # リトライボタンの位置とサイズ
quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)  # 終了ボタンの位置とサイズ
selected_button = 'retry'  # 初期選択ボタン

def show_game_over():
    """ゲームオーバー画面を表示する関数"""
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

    # リトライボタン
    pygame.draw.rect(screen, GREEN if selected_button == 'retry' else WHITE, retry_button_rect)
    retry_text = button_font.render("Retry", True, BLACK)
    screen.blit(retry_text, (retry_button_rect.x + 50, retry_button_rect.y + 5))

    # 終了ボタン
    pygame.draw.rect(screen, GREEN if selected_button == 'quit' else WHITE, quit_button_rect)
    quit_text = button_font.render("Quit", True, BLACK)
    screen.blit(quit_text, (quit_button_rect.x + 60, quit_button_rect.y + 5))

    pygame.display.flip()

def reset_game(init=False):
    """ゲームの状態をリセットする関数"""
    global player_x, player_y, beams, enemy_beams, enemies, explosions, player_lives, score
    player_x = INITIAL_PLAYER_X
    player_y = INITIAL_PLAYER_Y
    beams = []
    enemy_beams = []
    enemies = []
    explosions = []
    if init:
        player_lives = INITIAL_LIVES  # リセット時にライフを元に戻す
        score = INITIAL_SCORE  # リセット時にスコアを元に戻す
    pygame.mixer.music.load(BACKGROUND_MUSIC)
    pygame.mixer.music.play(-1)  # ゲーム再開時に元のBGMを再生

def draw_explosions():
    """爆発エフェクトを描画する関数"""
    for explosion in explosions[:]:
        screen.blit(explosion_img, (explosion[0], explosion[1]))
        explosion[2] -= 1
        if explosion[2] <= 0:
            explosions.remove(explosion)
    pygame.display.flip()

def check_collision(mask1, x1, y1, mask2, x2, y2):
    """マスクを使用して衝突判定を行う関数"""
    offset_x = x2 - x1
    offset_y = y2 - y1
    return mask1.overlap(mask2, (offset_x, offset_y)) is not None

# ゲームループの初期化
running = True
game_over = False
clock = pygame.time.Clock()

# ゲームの初期化
reset_game(init=True)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = event.pos
            if retry_button_rect.collidepoint(mouse_pos):
                reset_game(init=True)
                game_over = False
            elif quit_button_rect.collidepoint(mouse_pos):
                running = False
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected_button = 'retry' if selected_button == 'quit' else 'quit'
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_button == 'retry':
                        reset_game(init=True)
                        game_over = False
                    elif selected_button == 'quit':
                        running = False
    
    if not game_over:
        # プレイヤーの移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
            player_x += PLAYER_SPEED
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - PLAYER_HEIGHT:
            player_y += PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            beams.append([player_x + PLAYER_WIDTH, player_y + PLAYER_HEIGHT // 2])
            beam_fire_sound.play()  # ビーム発射音を再生
        
        # ビームの位置更新
        for beam in beams[:]:
            beam[0] += BEAM_SPEED
            if beam[0] > SCREEN_WIDTH:
                beams.remove(beam)
        
        # 新しい敵を追加
        if random.randint(1, 20) == 1:
            enemies.append([SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT)])
        
        # 敵の位置更新
        for enemy in enemies[:]:
            enemy[0] -= ENEMY_SPEED
            if random.randint(1, 50) == 1:
                enemy_beams.append([enemy[0], enemy[1] + ENEMY_HEIGHT // 2])
            if enemy[0] < 0:
                enemies.remove(enemy)
        
        # 敵ビームの位置更新
        for enemy_beam in enemy_beams[:]:
            enemy_beam[0] -= ENEMY_BEAM_SPEED
            if enemy_beam[0] < 0:
                enemy_beams.remove(enemy_beam)
        
        # 衝突判定
        player_hit = False
        enemies_to_remove = []
        beams_to_remove = []
        enemy_beams_to_remove = []

        for enemy in enemies:
            for beam in beams:
                if check_collision(enemy_mask, enemy[0], enemy[1], pygame.mask.Mask((BEAM_WIDTH, BEAM_HEIGHT), True), beam[0], beam[1]):
                    explosions.append([enemy[0], enemy[1], EXPLOSION_DURATION])
                    enemies_to_remove.append(enemy)
                    beams_to_remove.append(beam)
                    score += SCORE_PER_HIT
                    enemy_explosion_sound.play()  # 敵機の爆発音を再生

            if check_collision(player_mask, player_x, player_y, enemy_mask, enemy[0], enemy[1]):
                explosions.append([enemy[0], enemy[1], EXPLOSION_DURATION])
                enemies_to_remove.append(enemy)
                player_lives -= 1
                player_hit = True
                player_explosion_sound.play()  # プレイヤー機の爆発音を再生
                if player_lives == 0:
                    game_over = True
                    pygame.mixer.music.load(GAME_OVER_MUSIC)
                    pygame.mixer.music.play(-1)  # ゲームオーバー時に別のBGMを再生

        for enemy_beam in enemy_beams:
            if check_collision(player_mask, player_x, player_y, pygame.mask.Mask((BEAM_WIDTH, BEAM_HEIGHT), True), enemy_beam[0], enemy_beam[1]):
                explosions.append([player_x, player_y, EXPLOSION_DURATION])
                enemy_beams_to_remove.append(enemy_beam)
                player_lives -= 1
                player_hit = True
                player_explosion_sound.play()  # プレイヤー機の爆発音を再生
                if player_lives == 0:
                    game_over = True
                    pygame.mixer.music.load(GAME_OVER_MUSIC)
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
            reset_game(init=False)

        # 画面の描画
        screen.fill(BLACK)
        
        # プレイヤーの描画
        screen.blit(player_img, (player_x, player_y))
        
        # ビームの描画
        for beam in beams:
            pygame.draw.rect(screen, WHITE, (beam[0], beam[1], BEAM_WIDTH, BEAM_HEIGHT))
        
        # 敵の描画
        for enemy in enemies:
            screen.blit(enemy_img, (enemy[0], enemy[1]))
        
        # 敵ビームの描画
        for enemy_beam in enemy_beams:
            pygame.draw.rect(screen, RED, (enemy_beam[0], enemy_beam[1], BEAM_WIDTH, BEAM_HEIGHT))
        
        # スコアとライフの描画
        score_text = font.render(f'Score: {score}', True, WHITE)
        lives_text = font.render(f'Lives: {player_lives}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        
        pygame.display.flip()
        clock.tick(60)
    else:
        show_game_over()

pygame.quit()
