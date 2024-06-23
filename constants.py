# constants.py

# デバッグモード
DEBUG_MODE = False

# 画面の設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# プレイヤーの設定
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
INITIAL_PLAYER_X = 10
INITIAL_PLAYER_Y = SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2
INITIAL_LIVES = 3
INITIAL_SCORE = 0

# 敵の設定
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_SPEED = -3
ENEMY_PROB_PER_FRAME = 20 #フレーム毎の敵の出現確率

# ビームの設定
PLAYER_BEAM_WIDTH = 20  # 横長の楕円の幅
PLAYER_BEAM_HEIGHT = 5  # 横長の楕円の高さ
PLAYER_BEAM_SPEED = 7
ENEMY_BEAM_WIDTH = 20  # 横長の楕円の幅
ENEMY_BEAM_HEIGHT = 5  # 横長の楕円の高さ
ENEMY_BEAM_SPEED = -5 
ENEMY_BEAM_ANGLE_UNIT = 45

# スコア設定
SCORE_PER_HIT = 10  # 敵にビームが当たった時のスコア

# ゲーム設定
EXPLOSION_DURATION = 30  # 爆発が表示されるフレーム数期間
PLAYER_HIT_SLEEP_TIME = 3  # プレイヤー機の爆発時のスリープ時間

# ファイル名の定義
BACKGROUND_MUSIC = 'sounds/background_music.mp3'
GAME_OVER_MUSIC = 'sounds/game_over_music.mp3'
PLAYER_EXPLOSION_SOUND = 'sounds/player_explosion.mp3'
ENEMY_EXPLOSION_SOUND = 'sounds/enemy_explosion.mp3'
BEAM_FIRE_SOUND = 'sounds/beam_fire.mp3'
PLAYER_IMAGE = 'images/player.png'
ENEMY_IMAGE = 'images/enemy.png'
EXPLOSION_IMAGE = 'images/explosion.png'
BACKGROUND_IMAGE = 'images/background.png'
PLAYER_BEAM_IMAGE = "images/player_beam.png"
ENEMY_BEAM_IMAGE = "images/enemy_beam.png"

# ボタンの選択肢
RETRY_BUTTON = 'retry'
QUIT_BUTTON = 'quit'
