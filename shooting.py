from typing import Sequence
import pygame
import random
import time
from base_object import BaseObject
from beam import EnemyBeam, PlayerBeam, RotateEnemyBeam, RotatePlayerBeam
from explosion import EnemyExplosion, PlayerExplosion
from player import Player
from enemy import Enemy
from constants import (
    BACKGROUND_MUSIC,
    BLACK,
    ENEMY_PROB_PER_FRAME_RECIP,
    GAME_OVER_MUSIC,
    PLAEYR_SHOOTER_TIME,
    PLAYER_HIT_SLEEP_TIME,
    QUIT_BUTTON,
    RETRY_BUTTON,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND_IMAGE,
    GREEN,
    SHOOTING_TIME_MUSIC,
    WHITE,
)
from utils import check_collision

#グローバル宣言
screen: pygame.Surface
background_img: pygame.Surface
font: pygame.font.Font
button_font: pygame.font.Font
retry_button_rect: pygame.Rect
quit_button_rect: pygame.Rect
player_beams: list[PlayerBeam|RotatePlayerBeam]
enemy_beams: list[EnemyBeam|RotateEnemyBeam]
enemies: list[Enemy]
explosions: list[PlayerExplosion|EnemyExplosion]


def setup() -> None:
    """初期設定を行う関数"""
    global \
        screen, \
        font, \
        button_font, \
        retry_button_rect, \
        quit_button_rect, \
        background_img

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 背景画像の読み込み
    background_img = pygame.image.load(BACKGROUND_IMAGE).convert()
    background_img = pygame.transform.scale(
        background_img, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    # フォント設定
    font = pygame.font.Font(None, 36)  # スコアやライフ表示用のフォント
    button_font = pygame.font.Font(None, 48)  # ボタン用のフォント

    # ボタンの設定
    # リトライボタンの位置とサイズ
    retry_button_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2, 100, 50
    )
    # 終了ボタンの位置とサイズ
    quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2, 100, 50)


def show_game_over(selected_button: str) -> None:
    """ゲームオーバー画面を表示する関数"""
    screen.fill(BLACK)
    game_over_text = button_font.render("GAME OVER", True, WHITE)
    screen.blit(
        game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 50)
    )

    # リトライボタン
    pygame.draw.rect(
        screen, GREEN if selected_button == RETRY_BUTTON else WHITE, retry_button_rect
    )
    retry_text = button_font.render("Retry", True, BLACK)
    screen.blit(retry_text, (retry_button_rect.x + 10, retry_button_rect.y + 5))

    # 終了ボタン
    pygame.draw.rect(
        screen, GREEN if selected_button == QUIT_BUTTON else WHITE, quit_button_rect
    )
    quit_text = button_font.render("Quit", True, BLACK)
    screen.blit(quit_text, (quit_button_rect.x + 10, quit_button_rect.y + 5))

    pygame.display.flip()


def reset_game(player: Player, init: bool = False) -> None:
    """ゲームの状態をリセットする関数"""
    global player_beams, enemy_beams, enemies, explosions
    player_beams= []
    enemy_beams = []
    enemies = []
    explosions = []
    player.reset(init)
    pygame.mixer.music.load(BACKGROUND_MUSIC)
    pygame.mixer.music.play(-1)  # ゲーム再開時に元のBGMを再生


def draw_explosions(explosions: list[EnemyExplosion|PlayerExplosion]) -> None:
    """爆発エフェクトを描画する関数"""
    for explosion in explosions:
        explosion.draw(screen)
        explosion.reduce_life()
        if explosion.is_dead():
            explosions.remove(explosion)


def draw(obj_array: Sequence[BaseObject]) -> None:
    for obj in obj_array:
        obj.draw(screen)


def bombed(player: Player) -> bool:
    explosions.append(player.explosion())
    game_over = player.is_dead()
    if game_over:
        pygame.mixer.music.load(GAME_OVER_MUSIC)
        pygame.mixer.music.play(-1)  # ゲームオーバー時に別のBGMを再生
    return game_over


def main() -> None:
    """ゲームのメインループ"""

    # Pygameの初期化
    pygame.init()

    # 初期設定の呼び出し
    setup()

    # ゲームの初期化
    player = Player()
    reset_game(player, init=True)

    # ゲームループの初期化
    running = True
    game_over = False
    shooting_time = False
    selected_button = RETRY_BUTTON  # 初期選択ボタン
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if retry_button_rect.collidepoint(mouse_pos):
                        reset_game(player, init=True)
                        game_over = False
                    elif quit_button_rect.collidepoint(mouse_pos):
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        selected_button = (
                            RETRY_BUTTON
                            if selected_button == QUIT_BUTTON
                            else QUIT_BUTTON
                        )
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if selected_button == RETRY_BUTTON:
                            reset_game(player, init=True)
                            game_over = False
                        elif selected_button == QUIT_BUTTON:
                            running = False

        if not game_over:
            # 画面の描画
            screen.blit(background_img, (0, 0))  # 背景画像を描画
            # スコアとライフの描画
            score_text = font.render(f"Score: {player.score}", True, WHITE)
            lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
            screen.blit(
                score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10)
            )  # スコアを右上に表示
            screen.blit(lives_text, (10, 10))  # ライフを左上に表示

            # 移動もしくはビーム発射
            player_beams_new = player.key_handler()
            if player_beams_new is not None:
                player_beams.extend(player_beams_new)

            # ビームの位置更新
            for player_beam in player_beams[:]:
                player_beam.move()
                if player_beam.off_screen():
                    player_beams.remove(player_beam)

            # 新しい敵を追加
            if random.randint(1, ENEMY_PROB_PER_FRAME_RECIP) == 1:
                enemies.append(Enemy())

            # 敵ループ
            for enemy in enemies[:]:
                # 敵の移動
                enemy.move()
                # ビーム発射
                enemy_beams_new = enemy.shooting()
                if enemy_beams_new is not None:
                    enemy_beams.extend(enemy_beams_new)
                # 画面外に来たら削除
                if enemy.off_screen():
                    enemies.remove(enemy)
                # 敵とプレイヤーの当たり判定
                elif check_collision(player, enemy):
                    game_over = bombed(player)
                    enemies.remove(enemy)
                else:
                    # 敵とビームの当たり判定
                    for player_beam in player_beams[:]:
                        if check_collision(enemy, player_beam):
                            explosions.append(enemy.explosion())
                            player_beams.remove(player_beam)
                            enemies.remove(enemy)
                            player.score_up()
                            break
            # 敵ビームループ
            if not player.hit:
                for enemy_beam in enemy_beams[:]:
                    # 敵ビームの位置更新
                    enemy_beam.move()
                    # 画面外に来たら削除
                    if enemy_beam.off_screen():
                        enemy_beams.remove(enemy_beam)
                    # 敵ビームとプレイヤーの当たり判定
                    if check_collision(player, enemy_beam):
                        game_over = bombed(player)
                        enemy_beams.remove(enemy_beam)
                        break

            # プレイヤーの描画
            player.draw(screen)
            # ビームの描画
            draw(player_beams)
            # 敵の描画
            draw(enemies)
            # 敵ビームの描画
            draw(enemy_beams)
            # 爆発の更新
            draw_explosions(explosions)

            #放射ビーム発射ゲージアップ
            player.shooting_gage_up()
            #BGM切り替え
            if (not shooting_time) and (player.shooting_gage >= PLAEYR_SHOOTER_TIME[0]):
                pygame.mixer.music.load(SHOOTING_TIME_MUSIC)
                pygame.mixer.music.play(-1)
                shooting_time = True
            elif shooting_time and (player.shooting_gage < PLAEYR_SHOOTER_TIME[0]):
                pygame.mixer.music.load(BACKGROUND_MUSIC)
                pygame.mixer.music.play(-1) 
                shooting_time = False

            pygame.display.flip()
            clock.tick(60)

            if player.hit:
                time.sleep(PLAYER_HIT_SLEEP_TIME)  # 3秒間スリープ
                if not game_over:
                    reset_game(player, init=False)

        else:
            show_game_over(selected_button)

    pygame.quit()


if __name__ == "__main__":
    main()
