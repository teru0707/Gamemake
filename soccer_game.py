import pygame
import sys
import random

# 初期化
pygame.init()

# 画面サイズと色の設定
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = (0, 128, 0)  # サッカー場の緑色

# プレイヤーとボールの設定
PLAYER_SIZE = (100, 100)
BALL_SIZE = (45, 45)
PLAYER_SPEED = 6.5
BALL_SPEED = 5

# 画像の読み込みとスケーリング
try:
    player1_image = pygame.image.load("player1.png")
    player2_image = pygame.image.load("player2.png")
    ball_image = pygame.image.load("ball.png")

    player1_image = pygame.transform.scale(player1_image, PLAYER_SIZE)
    player2_image = pygame.transform.scale(player2_image, PLAYER_SIZE)
    ball_image = pygame.transform.scale(ball_image, BALL_SIZE)
except pygame.error as e:
    print(f"画像の読み込みに失敗しました: {e}")
    pygame.quit()
    sys.exit()

# ゴールの設定
GOAL_WIDTH = 20
GOAL_HEIGHT = 200
GOAL_COLOR = (255, 255, 255)  # ゴールは白色

# 画面を作成
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("サッカーゲーム")

# フォントの設定
font = pygame.font.Font(None, 74)
win_font = pygame.font.Font(None, 100) 

# スコア、ボール、プレイヤーの初期化
def reset_game():
    global player1, player2, ball, ball_dx, ball_dy, score1, score2, goal1, goal2
    player1 = pygame.Rect(100, SCREEN_HEIGHT // 2 - PLAYER_SIZE[1] // 2, *PLAYER_SIZE)
    player2 = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2 - PLAYER_SIZE[1] // 2, *PLAYER_SIZE)
    ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE[0] // 2, SCREEN_HEIGHT // 2 - BALL_SIZE[1] // 2, *BALL_SIZE)
    ball_dx, ball_dy = BALL_SPEED, BALL_SPEED
    score1, score2 = 0, 0
    goal1 = pygame.Rect(0, SCREEN_HEIGHT // 2 - GOAL_HEIGHT // 2, GOAL_WIDTH, GOAL_HEIGHT)
    goal2 = pygame.Rect(SCREEN_WIDTH - GOAL_WIDTH, SCREEN_HEIGHT // 2 - GOAL_HEIGHT // 2, GOAL_WIDTH, GOAL_HEIGHT)

reset_game()

# ボールを中央にリセットする関数
def reset_ball():
    global ball_dx, ball_dy
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # ランダムな速度を設定 (例: 2～5の範囲でランダム)
    speed = random.randint(2, 5)
    ball_dx = random.choice([-1, 1]) * speed
    ball_dy = random.choice([-1, 1]) * speed

# プレイヤーとボールが衝突した際に、ボールの速度が0.25ずつ増加する関数
def increase_speed_on_player_collicion():
    global ball_dx, ball_dy
    if ball_dx > 0:
        ball_dx += 0.25
    else:
        ball_dx -= 0.25

    if ball_dy > 0:
        ball_dy += 0.25
    else:
        ball_dy -= 0.25
# ボールが壁に衝突した際に、ボールの速度が0.1ずつ増加する関数
def increae_speed_on_wall_collicion():
    global ball_dx, ball_dy
    if ball_dx > 0:
        ball_dx += 0.1
    else:
        ball_dx -= 0.1

    if ball_dy > 0:
        ball_dy += 0.1
    else:
        ball_dy -= 0.1

# 勝者を表示する関数
def display_winner(winner):
    win_text = win_font.render(f"{winner} win!!", True, (255, 0, 0))
    screen.fill(BG_COLOR)  # 背景をクリア
    screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2))
    pygame.display.flip()  # 画面更新
    pygame.time.wait(5000)  # 3秒待機


# メインループ
clock = pygame.time.Clock()
running = True
while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # リセット処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:  # "R"キーでリセット
        reset_game()

    # キー入力処理
    if keys[pygame.K_w] and player1.top > 0:
        player1.move_ip(0, -PLAYER_SPEED)
    if keys[pygame.K_s] and player1.bottom < SCREEN_HEIGHT:
        player1.move_ip(0, PLAYER_SPEED)
    if keys[pygame.K_UP] and player2.top > 0:
        player2.move_ip(0, -PLAYER_SPEED)
    if keys[pygame.K_DOWN] and player2.bottom < SCREEN_HEIGHT:
        player2.move_ip(0, PLAYER_SPEED)

    # ボールの移動
    ball.move_ip(ball_dx, ball_dy)

    # 壁で跳ね返る
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_dy *= -1
        increae_speed_on_wall_collicion()

    # ゴール判定
    if ball.colliderect(goal1):  # 左ゴールに入った
        score2 += 1
        if score2 == 5:
            display_winner("player2")
            running = False
        reset_ball()
    elif ball.colliderect(goal2):  # 右ゴールに入った
        score1 += 1
        if score1 == 5:
            display_winner("player1")
            running = False
        reset_ball()
    elif ball.left <= 0 or ball.right >= SCREEN_WIDTH:  # ゴール外に出た場合
        reset_ball()

    # プレイヤーとボールの衝突
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_dx *= -1
        increase_speed_on_player_collicion()

    # 画面の描画
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, GOAL_COLOR, goal1)  # 左ゴール
    pygame.draw.rect(screen, GOAL_COLOR, goal2)  # 右ゴール
    screen.blit(player1_image, player1.topleft)  # プレイヤー1の画像
    screen.blit(player2_image, player2.topleft)  # プレイヤー2の画像
    screen.blit(ball_image, ball.topleft)        # ボールの画像

    # スコア表示
    score_text = font.render(f"{score1} - {score2}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

    # 画面更新
    pygame.display.flip()
    clock.tick(60)

# ゲーム終了
pygame.quit()
sys.exit()
