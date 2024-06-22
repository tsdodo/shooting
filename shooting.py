# main.py

import pygame
import random
import time
from player import Player
from enemy import Enemy
from player_beam import PlayerBeam
from enemy_beam import EnemyBeam,RotateEnemyBeam
from constants import *
from utils import check_collision, debug_log

def setup():
    """初期設定を行う関数"""
    global screen, font, button_font, retry_button_rect, quit_button_rect
    global player_explosion_sound, enemy_explosion_sound, beam_fire_sound, background_img, explosion_img

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 効果音の読み込み
    player_explosion_sound = pygame.mixer.Sound(PLAYER_EXPLOSION_SOUND)
    enemy_explosion_sound = pygame.mixer.Sound(ENEMY_EXPLOSION_SOUND)
    beam_fire_sound = pygame.mixer.Sound(BEAM_FIRE_SOUND)

    # 背景画像の読み込み
    background_img = pygame.image.load(BACKGROUND_IMAGE).convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # 爆発画像の読み込み
    explosion_img = pygame.image.load(EXPLOSION_IMAGE).convert_alpha()
    explosion_img = pygame.transform.scale(explosion_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

    # フォント設定
    font = pygame.font.Font(None, 36)  # スコアやライフ表示用のフォント
    button_font = pygame.font.Font(None, 48)  # ボタン用のフォント

    # ボタンの設定
    retry_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2, 100, 50)  # リトライボタンの位置とサイズ
    quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2, 100, 50)  # 終了ボタンの位置とサイズ

    debug_log("Setup complete")

def show_game_over(selected_button):
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

def reset_game(player, init=False):
    """ゲームの状態をリセットする関数"""
    global beams, enemy_beams, enemies, explosions
    beams = []
    enemy_beams = []
    enemies = []
    explosions = []
    player.reset(init) 
    pygame.mixer.music.load(BACKGROUND_MUSIC)
    pygame.mixer.music.play(-1)  # ゲーム再開時に元のBGMを再生
    debug_log("Game reset")

def draw_explosions():
    """爆発エフェクトを描画する関数"""
    global explosions
    for explosion in explosions[:]:
        screen.blit(explosion_img, (explosion[0], explosion[1]))
        explosion[2] -= 1
        if explosion[2] <= 0:
            explosions.remove(explosion)

def be_bombed(player):
    global explosions,player_explosion_sound
    explosions.append([player.x, player.y, EXPLOSION_DURATION])
    player.lives -= 1
    player.hit = True
    player_explosion_sound.play()  # プレイヤー機の爆発音を再生
    if player.lives == 0:
        game_over = True
        pygame.mixer.music.load(GAME_OVER_MUSIC)
        pygame.mixer.music.play(-1)  # ゲームオーバー時に別のBGMを再生
        debug_log("Game over")
    else:
        game_over = False
    return game_over

def main():
    """ゲームのメインループ"""
    global selected_button, running, game_over, screen, font, button_font, retry_button_rect, quit_button_rect
    global player_explosion_sound, enemy_explosion_sound, beam_fire_sound, background_img, explosions

    # Pygameの初期化
    pygame.init()

    # 初期設定の呼び出し
    setup()

    # ゲームの初期化
    player = Player(INITIAL_PLAYER_X, INITIAL_PLAYER_Y)
    reset_game(player, init=True)
    debug_log("Game initialized")

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
                debug_log(f"Mouse click at {mouse_pos}")
                if retry_button_rect.collidepoint(mouse_pos):
                    reset_game(player, init=True)
                    game_over = False
                    debug_log("Retry button clicked")
                elif quit_button_rect.collidepoint(mouse_pos):
                    running = False
                    debug_log("Quit button clicked")
            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        selected_button = RETRY_BUTTON if selected_button == QUIT_BUTTON else QUIT_BUTTON
                        debug_log(f"Selected button: {selected_button}")
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if selected_button == RETRY_BUTTON:
                            reset_game(player, init=True)
                            game_over = False
                            debug_log("Retry button selected with keyboard")
                        elif selected_button == QUIT_BUTTON:
                            running = False
                            debug_log("Quit button selected with keyboard")
        
        if not game_over:
            # プレイヤーの移動
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x > 0:
                player.move_left()
            if keys[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - PLAYER_WIDTH:
                player.move_right()
            if keys[pygame.K_UP] and player.y > 0:
                player.move_up()
            if keys[pygame.K_DOWN] and player.y < SCREEN_HEIGHT - PLAYER_HEIGHT:
                player.move_down()
            if keys[pygame.K_SPACE]:
                beams.append(PlayerBeam(player.x + PLAYER_WIDTH, player.y + PLAYER_HEIGHT // 2))
                beam_fire_sound.play()  # ビーム発射音を再生
                debug_log("Player fired a beam")
            
            # ビームの位置更新
            for beam in beams[:]:
                beam.move()
                if beam.x > SCREEN_WIDTH or beam.x < 0 or beam.y > SCREEN_HEIGHT or beam.y < 0:
                    beams.remove(beam)
                    debug_log("Player beam removed")

            # 新しい敵を追加
            if random.randint(1, 20) == 1:
                # 敵の生成位置を調整してプレイヤーから離す
                enemy_x = SCREEN_WIDTH
                enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT)
                while abs(enemy_y - player.y) < ENEMY_HEIGHT * 2:
                    enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT)
                is_shooter = random.randint(1, 5) == 1  # ランダムに放射状ビームを撃つ敵を追加
                enemies.append(Enemy(enemy_x, enemy_y, is_shooter))
                debug_log(f"New enemy added at ({enemy_x}, {enemy_y})")
            
            # 敵の位置更新
            for enemy in enemies[:]:
                enemy.move()
                enemy.update_cooldowns()
                if enemy.is_shooter and enemy.radial_shoot_cooldown <= 0:
                    for angle in range(0, 360, 45):  # 45度ごとにビームを放射
                        enemy_beams.append(RotateEnemyBeam(enemy.x, enemy.y + ENEMY_HEIGHT // 2, angle))
                    enemy.radial_shoot_cooldown = random.randint(200, 400)
                    debug_log("Enemy fired radial beams")
                if enemy.shoot_cooldown <= 0:
                    enemy_beams.append(EnemyBeam(enemy.x, enemy.y + ENEMY_HEIGHT // 2))
                    enemy.shoot_cooldown = random.randint(50, 100)
                    debug_log("Enemy fired a beam")
                if enemy.x < 0:
                    enemies.remove(enemy)
                    debug_log("Enemy removed")

            # 敵ビームの位置更新
            for enemy_beam in enemy_beams[:]:
                enemy_beam.move()
                if enemy_beam.x < 0 or enemy_beam.x > SCREEN_WIDTH or enemy_beam.y < 0 or enemy_beam.y > SCREEN_HEIGHT:
                    enemy_beams.remove(enemy_beam)
                    debug_log("Enemy beam removed")

            # 衝突判定
            enemies_to_remove = []
            beams_to_remove = []
            enemy_beams_to_remove = []

            for enemy in enemies:
                for beam in beams:
                    if check_collision(enemy.mask, enemy.x, enemy.y, beam.mask, beam.x, beam.y):
                        explosions.append([enemy.x, enemy.y, EXPLOSION_DURATION])
                        enemies_to_remove.append(enemy)
                        beams_to_remove.append(beam)
                        player.score += SCORE_PER_HIT
                        enemy_explosion_sound.play()  # 敵機の爆発音を再生
                        debug_log("Enemy hit by player beam")

                if check_collision(player.mask, player.x, player.y, enemy.mask, enemy.x, enemy.y):
                    game_over = be_bombed(player)
                    enemies_to_remove.append(enemy)
                    debug_log(f"Player hit by enemy. Player position: ({player.x}, {player.y}), Enemy position: ({enemy.x}, {enemy.y}), Lives left: {player.lives}")

            for enemy_beam in enemy_beams:
                if check_collision(player.mask, player.x, player.y, enemy_beam.mask, enemy_beam.x, enemy_beam.y):
                    game_over = be_bombed(player)
                    enemy_beams_to_remove.append(enemy_beam)
                    debug_log(f"Player hit by enemy beam. Player position: ({player.x}, {player.y}), Enemy beam position: ({enemy_beam.x}, {enemy_beam.y}), Lives left: {player.lives}")

            # リスト外で削除
            for enemy in enemies_to_remove:
                if enemy in enemies:
                    enemies.remove(enemy)
                    debug_log("Enemy removed from list")
            for beam in beams_to_remove:
                if beam in beams:
                    beams.remove(beam)
                    debug_log("Player beam removed from list")
            for enemy_beam in enemy_beams_to_remove:
                if enemy_beam in enemy_beams:
                    enemy_beams.remove(enemy_beam)
                    debug_log("Enemy beam removed from list")

            # 画面の描画
            screen.blit(background_img, (0, 0))  # 背景画像を描画
            player.draw(screen)  # プレイヤーの描画
            
            # ビームの描画
            for beam in beams:
                beam.draw(screen)  # プレイヤーのビームの描画
            
            # 敵の描画
            for enemy in enemies:
                enemy.draw(screen)
            
            # 敵ビームの描画
            for enemy_beam in enemy_beams:
                enemy_beam.draw(screen)  # 敵のビームの描画
            
            # 爆発の更新
            draw_explosions()
            
            # スコアとライフの描画
            score_text = font.render(f'Score: {player.score}', True, WHITE)
            lives_text = font.render(f'Lives: {player.lives}', True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))  # スコアを右上に表示
            screen.blit(lives_text, (10, 10))  # ライフを左上に表示
            
            pygame.display.flip()
            clock.tick(60)
            
            if player.hit and not game_over:
                draw_explosions()  # 爆発を描画して更新
                pygame.display.flip()
                debug_log("Player hit, sleeping for recovery")
                time.sleep(PLAYER_HIT_SLEEP_TIME)  # 3秒間スリープ
                reset_game(player, init=False)

        else:
            show_game_over(selected_button)

    pygame.quit()
    debug_log("Game quit")

if __name__ == "__main__":
    main()
