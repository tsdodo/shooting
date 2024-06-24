from typing import Tuple


DEBUG_MODE: bool = False

# 画面の設定
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600

# 色の定義
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
RED: Tuple[int, int, int] = (255, 0, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)
BLUE: Tuple[int, int, int] = (0, 0, 255)

# プレイヤーの設定
PLAYER_WIDTH: int = 50
PLAYER_HEIGHT: int = 60
PLAYER_SPEED: int = 5
INITIAL_PLAYER_X: int = 10
INITIAL_PLAYER_Y: int = SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2
INITIAL_LIVES: int = 3
INITIAL_SCORE: int = 0
PLAEYR_SHOOTER_TIME = (700,1000)

# 敵の設定
ENEMY_WIDTH: int = 50
ENEMY_HEIGHT: int = 50
ENEMY_SPEED: int = -3
ENEMY_PROB_PER_FRAME_RECIP: int = 20  # フレーム毎の敵の出現確率の逆数
SHOOTER_PROB_PER_ENEMY_RECIP: int = 5  # 放射ビームを撃つ敵の出現確率の逆数

# ビームの設定
PLAYER_BEAM_WIDTH: int = 20  # 横長の楕円の幅
PLAYER_BEAM_HEIGHT: int = 5  # 横長の楕円の高さ
PLAYER_BEAM_SPEED: int = 7
PLAYER_BEAM_ANGLE_UNIT: int = 15
ENEMY_BEAM_WIDTH: int = 20  # 横長の楕円の幅
ENEMY_BEAM_HEIGHT: int = 5  # 横長の楕円の高さ
ENEMY_BEAM_SPEED: int = -5
ENEMY_BEAM_ANGLE_UNIT: int = 45

# スコア設定
SCORE_PER_HIT: int = 10  # 敵にビームが当たった時のスコア

# ゲーム設定
EXPLOSION_DURATION: int = 30  # 爆発が表示されるフレーム数期間
PLAYER_HIT_SLEEP_TIME: int = 3  # プレイヤー機の爆発時のスリープ時間

# ファイル名の定義
BACKGROUND_MUSIC: str = "sounds/background_music.mp3"
GAME_OVER_MUSIC: str = "sounds/game_over_music.mp3"
SHOOTING_TIME_MUSIC: str = "sounds/shooting_tiime_musinc.mp3"
PLAYER_EXPLOSION_SOUND: str = "sounds/player_explosion.mp3"
ENEMY_EXPLOSION_SOUND: str = "sounds/enemy_explosion.mp3"
PLAYER_BEAM_FIRE_SOUND: str = "sounds/beam_fire.mp3"
PLAYER_IMAGE: str = "images/player.png"
ENEMY_IMAGE: str = "images/enemy.png"
SHOOTER_ENEMY_IMAGE: str = "images/shooter_enemy.png"
EXPLOSION_IMAGE: str = "images/explosion.png"
BACKGROUND_IMAGE: str = "images/background.png"
PLAYER_BEAM_IMAGE: str = "images/player_beam.png"
ENEMY_BEAM_IMAGE: str = "images/enemy_beam.png"

# ボタンの選択肢
RETRY_BUTTON: str = "retry"
QUIT_BUTTON: str = "quit"
