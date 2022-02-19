import sys
import os
import pygame

pygame.init()

WIDTH, HEIGHT = 700, 500
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong - Classic')

FONT = pygame.font.SysFont('comicsans', 50)

SOUND = pygame.mixer.Sound(os.path.join('ball_paddle.mp3'))

PADDLE_HIT = pygame.USEREVENT + 1


class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.ogx = x
        self.y = self.ogy = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.ogx
        self.y = self.ogy


class Ball:

    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, r):
        self.x = self.ogx = x
        self.y = self.ogy = y
        self.r = r
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.r)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.ogx
        self.y = self.ogy
        self.y_vel = 0
        self.x_vel *= 1


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    left_text = FONT.render(f"{left_score}", 1, WHITE)
    right_text = FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_text, (WIDTH//4 - left_text.get_width()//2, 20))
    win.blit(right_text, (WIDTH*3//4 - right_text.get_width()//2, 20))
    for paddle in paddles:
        paddle.draw(win)
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 2, i, 4, HEIGHT//20))
    ball.draw(win)
    pygame.display.update()


def paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def collision(ball, left_paddle, right_paddle):
    if ball.y + ball.r >= HEIGHT or ball.y - ball.r <= 0:
        ball.y_vel *= -1
    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.r <= left_paddle.x + left_paddle.width:
                pygame.event.post(pygame.event.Event(PADDLE_HIT))
                ball.x_vel *= -1
                middle = left_paddle.y + left_paddle.height / 2
                vel_ratio = (left_paddle.height / 2) / ball.MAX_VEL
                distance = middle - ball.y
                ball.y_vel = -1 * distance / vel_ratio
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.r >= right_paddle.x:
                pygame.event.post(pygame.event.Event(PADDLE_HIT))
                ball.x_vel *= -1
                middle = right_paddle.y + right_paddle.height / 2
                vel_ratio = (right_paddle.height / 2) / ball.MAX_VEL
                distance = middle - ball.y
                ball.y_vel = -1 * distance / vel_ratio


def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_WIDTH, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_WIDTH, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    left_score = 0
    right_score = 0
    newFPS = FPS
    while run:
        clock.tick(newFPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == PADDLE_HIT:
                SOUND.play()
                newFPS += 10
        keys = pygame.key.get_pressed()
        paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        collision(ball, left_paddle, right_paddle)
        if ball.x < 0:
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            newFPS = FPS
        if ball.x > WIDTH:
            left_score += 1
            ball.reset()
            newFPS = FPS
        won = False
        won_text = ""
        if left_score >= 10:
            won = True
            newFPS = FPS
            won_text = "Left Player Wins!!"

        if right_score >= 10:
            won = True
            won_text = "Right Player Wins!!"
        if won:
            winner_text = FONT.render(won_text, 1, WHITE)
            WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            pygame.quit()
            sys.exit()
    pygame.quit()


main()

if '__name__' == '__main__':
    main()
