import math, os, random
import pygame
from pygame.locals import *
from sprites import Ball, Paddle, Side, BallOutOfField

RETRO = False

SIZE = (800, 600)
if RETRO:
    BG_COLOR = (0, 0, 0)
    FONT_COLOR = (250, 250, 250)
else:
    BG_COLOR = (250, 250, 250)
    FONT_COLOR = (0, 0, 0)

paddle_img = "paddle{}.png".format("_retro" if RETRO else "")
ball_img = "ball{}.png".format("_retro" if RETRO else "")
FONT_HEIGHT = 50
DATA_DIR = "data"
FPS = 60

def main():
    screen = pygame.display.set_mode(SIZE)
    background = pygame.surface.Surface(SIZE)
    background.fill(BG_COLOR)
    screen.blit(background, screen.get_rect())
    pygame.display.update()


    paddle_image = pygame.image.load(os.path.join(DATA_DIR, paddle_img)).convert_alpha()
    paddle_left = Paddle(screen, paddle_image, Side.left, 5)
    paddle_right = Paddle(screen, paddle_image, Side.right, 5)
    ball_image = pygame.image.load(os.path.join(DATA_DIR, ball_img)).convert_alpha()
    ball = Ball(screen, ball_image, 8, [paddle_left, paddle_right])

    everything = pygame.sprite.RenderUpdates(ball, paddle_left, paddle_right)

    clock = pygame.time.Clock()
    paused = False

    paddle_callbacks = {K_UP: paddle_right.begin_moving_up,
                     K_DOWN: paddle_right.begin_moving_down,
                     K_w: paddle_left.begin_moving_up,
                     K_s: paddle_left.begin_moving_down,
    }
    wait_counter = 0
    is_last_wait = False
    player1_score = 0
    player1_score_tmp = 0
    player2_score = 0
    player2_score_tmp = 0
    font = pygame.font.Font(None, FONT_HEIGHT)

    while True:
        is_last_wait = wait_counter == 1
        if wait_counter > 0:
            wait_counter -= 1
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    ball.reset()
                elif event.key == K_p:
                    paused = not paused
                elif event.key in paddle_callbacks:
                    paddle_callbacks[event.key]()
            elif event.type == KEYUP and event.key in paddle_callbacks:
                keys = pygame.key.get_pressed()
                if keys[K_UP] ^ keys[K_DOWN]:
                    if keys[K_UP]:
                        paddle_right.begin_moving_up()
                    else:
                        paddle_right.begin_moving_down()
                elif not keys[K_UP] and not keys[K_DOWN]:
                    paddle_right.stop()
                if keys[K_w] ^ keys[K_s]:
                    if keys[K_w]:
                        paddle_left.begin_moving_up()
                    else:
                        paddle_left.begin_moving_down()
                elif not keys[K_w] and not keys[K_s]:
                    paddle_left.stop()
        clock.tick(FPS)
        if not paused and wait_counter == 0:
            everything.clear(screen, background)
            if is_last_wait:
                player1_score =  player1_score_tmp
                player2_score =  player2_score_tmp
                ball.reset()
            else:
                try:
                    everything.update()
                except BallOutOfField as e:
                    wait_counter = 100
                    if e.side == Side.left:
                        player2_score_tmp += 1
                    elif e.side == Side.right:
                        player1_score_tmp += 1
            msg1 = font.render("{0}".format(player1_score), True, FONT_COLOR, BG_COLOR)
            msg2 = font.render("{0}".format(player2_score), True, FONT_COLOR, BG_COLOR)
            screen.blit(msg1, (30, 30))
            screen.blit(msg2, (screen.get_width()-30-font.size("{0}".format(player2_score))[0], 30))
            dirty_rects = everything.draw(screen)
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()