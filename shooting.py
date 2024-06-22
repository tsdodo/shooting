import pygame
import random
import time
import math

# 画面の設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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
BEAM_WIDTH = 20  # 横長の楕円の幅
BEAM_HEIGHT = 5  # 横長の楕円の高さ
BEAM_SPEED = 7
EXPLOSION_DURATION = 30  # 爆発が表示されるフレーム数
PLAYER_HIT_SLEEP_TIME = 3  # プレイヤー機の爆発時のスリープ時間

# ファイル名の定数
BACKGROUND_MUSIC = 'background_music.mp3'
GAME_OVER_MUSIC = 'game_over_music.mp3'
PLAYER_EXPLOSION_SOUND = 'player_explosion.mp3'
ENEMY_EXPLOSION_SOUND = 'enemy_explosion.mp3'
BEAM_FIRE_SOUND = 'beam_fire.mp3'
PLAYER_IMAGE = 'player.png'
ENEMY_IMAGE = 'enemy.png'
EXPLOSION_IMAGE = 'explosion.png'
BACKGROUND_IMAGE = 'background.png'
PLAYER_BEAM_IMAGE = "player_beam.png"
ENEMY_BEAM_IMAGE = "enemy_beam.png"

# ボタン選択肢の定数
RETRY_BUTTON = 'retry'
QUIT_BUTTON = 'quit'

class Enemy:
    def __init__(self, x, y, is_shooter=False):
        self.x = x
        self.y = y
        self.is_shooter = is_shooter
        self.shoot_cooldown = random.randint(50, 100)
        self.radial_shoot_cooldown = random.randint(200, 400) if is_shooter else 0

def setup():
    """初期設定を行う関数"""
    global screen, font, button_font, retry_button_rect, quit_button_rect
    global player_explosion_sound, enemy_explosion_sound, beam_fire_sound
    global player_img, player_mask, enemy_img, enemy_mask, explosion_img, background_img
    global player_beam_img, enemy_beam_img

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 効果音の読み込み
    player_explosion_sound = pygame.mixer.Sound(PLAYER_EXPLOSION_SOUND)
    enemy_explosion_sound = pygame.mixer.Sound(ENEMY_EXPLOSION_SOUND)
    beam_fire_sound = pygame.mixer.Sound(BEAM_FIRE_SOUND)

    # プレイヤー画像の読み込み
    player_img = pygame.image.load(PLAYER_IMAGE)
    player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
    player_mask = pygame.mask.from_surface(player_img)

    # 敵画像の読み込み
    enemy_img = pygame.image.load(ENEMY_IMAGE)
    enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
    enemy_mask = pygame.mask.from_surface(enemy_img)

    # 爆発画像の読み込み
    explosion_img = pygame.image.load(EXPLOSION_IMAGE)
    explosion_img = pygame.transform.scale(explosion_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

    # 背景画像の読み込み
    background_img = pygame.image.load(BACKGROUND_IMAGE).convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # ビーム画像の読み込み
    player_beam_img = pygame.image.load(PLAYER_BEAM_IMAGE).convert_alpha()
    enemy_beam_img = pygame.image.load(ENEMY_BEAM_IMAGE).convert_alpha()

    # フォント設定
    font = pygame.font.Font(None, 36)  # スコアやライフ表示用のフォント
    button_font = pygame.font.Font(None, 48)  # ボタン用のフォント

    # ボタンの設定
    retry_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2, 100, 50)  # リトライボタンの位置とサイズ
    quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2, 100, 50)  # 終了ボタンの位置とサイズ

def show_game_over():
    """ゲームオーバー画面を表示する関数"""
    screen.fill(BLACK)
    game_over_text = button_font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 50))

    # リトライボタン
    pygame.draw.rect(screen, GREEN if selected_button == RETRY_BUTTON else WHITE, retry_button_rect)
    retry_text = button_font.render("Retry", True, BLACK)
    screen.blit(retry_text, (retry_button_rect.x + 10, retry_button_rect.y + 5))

    # 終了ボタン
    pygame.draw.rect(screen, GREEN if selected_button == QUIT_BUTTON else WHITE, quit_button_rect)
    quit_text = button_font.render("Quit", True, BLACK)
    screen.blit(quit_text, (quit_button_rect.x + 10, quit_button_rect.y + 5))

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

def main():
    """ゲームのメインループ"""
    global selected_button, running, game_over
    global player_x, player_y, beams, enemy_beams, enemies, explosions, player_lives, score

    # Pygameの初期化
    pygame.init()

    # 初期設定の呼び出し
    setup()

    # ゲームの初期化
    reset_game(init=True)

    # ゲームループの初期化
    running = True
    game_over = False
    selected_button = RETRY_BUTTON  # 初期選択ボタン
    clock = pygame.time.Clock()

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
                        selected_button = RETRY_BUTTON if selected_button == QUIT_BUTTON else QUIT_BUTTON
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if selected_button == RETRY_BUTTON:
                            reset_game(init=True)
                            game_over = False
                        elif selected_button == QUIT_BUTTON:
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
                is_shooter = random.randint(1, 5) == 1  # ランダムに放射状ビームを撃つ敵を追加
                enemies.append(Enemy(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT), is_shooter))
            
            # 敵の位置更新
            for enemy in enemies[:]:
                enemy.x -= ENEMY_SPEED
                if enemy.is_shooter and enemy.radial_shoot_cooldown <= 0:
                    for angle in range(0, 360, 45):  # 45度ごとにビームを放射
                        radians = math.radians(angle)
                        enemy_beams.append([enemy.x, enemy.y + ENEMY_HEIGHT // 2, math.cos(radians) * ENEMY_BEAM_SPEED, math.sin(radians) * ENEMY_BEAM_SPEED])
                    enemy.radial_shoot_cooldown = random.randint(200, 400)
                else:
                    enemy.radial_shoot_cooldown -= 1
                if enemy.shoot_cooldown <= 0:
                    enemy_beams.append([enemy.x, enemy.y + ENEMY_HEIGHT // 2, -ENEMY_BEAM_SPEED, 0])
                    enemy.shoot_cooldown = random.randint(50, 100)
                else:
                    enemy.shoot_cooldown -= 1
                if enemy.x < 0:
                    enemies.remove(enemy)
            
            # 敵ビームの位置更新
            for enemy_beam in enemy_beams[:]:
                enemy_beam[0] += enemy_beam[2]
                enemy_beam[1] += enemy_beam[3]
                if enemy_beam[0] < 0 or enemy_beam[0] > SCREEN_WIDTH or enemy_beam[1] < 0 or enemy_beam[1] > SCREEN_HEIGHT:
                    enemy_beams.remove(enemy_beam)
            
            # 衝突判定
            player_hit = False
            enemies_to_remove = []
            beams_to_remove = []
            enemy_beams_to_remove = []

            for enemy in enemies:
                for beam in beams:
                    if check_collision(enemy_mask, enemy.x, enemy.y, pygame.mask.Mask((BEAM_WIDTH, BEAM_HEIGHT), True), beam[0], beam[1]):
                        explosions.append([enemy.x, enemy.y, EXPLOSION_DURATION])
                        enemies_to_remove.append(enemy)
                        beams_to_remove.append(beam)
                        score += SCORE_PER_HIT
                        enemy_explosion_sound.play()  # 敵機の爆発音を再生

                if check_collision(player_mask, player_x, player_y, enemy_mask, enemy.x, enemy.y):
                    explosions.append([enemy.x, enemy.y, EXPLOSION_DURATION])
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
                time.sleep(PLAYER_HIT_SLEEP_TIME)  # 3秒間スリープ
                reset_game(init=False)

            # 画面の描画
            screen.blit(background_img, (0, 0))  # 背景画像を描画
            screen.blit(player_img, (player_x, player_y))  # プレイヤーの描画
            
            # ビームの描画
            for beam in beams:
                screen.blit(player_beam_img, (beam[0], beam[1]))  # プレイヤーのビームの描画
            
            # 敵の描画
            for enemy in enemies:
                screen.blit(enemy_img, (enemy.x, enemy.y))
            
            # 敵ビームの描画
            for enemy_beam in enemy_beams:
                screen.blit(enemy_beam_img, (enemy_beam[0], enemy_beam[1]))  # 敵のビームの描画
            
            # スコアとライフの描画
            score_text = font.render(f'Score: {score}', True, WHITE)
            lives_text = font.render(f'Lives: {player_lives}', True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))  # スコアを右上に表示
            screen.blit(lives_text, (10, 10))  # ライフを左上に表示
            
            pygame.display.flip()
            clock.tick(60)
        else:
            show_game_over()

    pygame.quit()

if __name__ == "__main__":
    main()
