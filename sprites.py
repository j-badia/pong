import math, random
import pygame
from vector import Vector, vector_from_polar

def deg_to_rad(d):
    return d * math.pi / 180.0

def rad_to_deg(r):
    return r * 180.0 / math.pi

class Side:
    left = object()
    right = object()

class BallOutOfField(Exception):
    def __init__(self, side):
        self.side = side

    def __str__(self):
        return repr(self.side)

class Ball(pygame.sprite.Sprite):
    def __init__(self, field, image, speed, paddles):
        """__init__(self, field, image, speed)

field should be the surface on which the ball will move
image should be a surface representing the ball's picture
speed should be given in pixels per frame"""
        pygame.sprite.Sprite.__init__(self)
        self.field = field
        self.image = image
        self.paddles = paddles
        self.rect = image.get_rect()
        self.initial_speed = speed
        self.velocity = vector_from_polar(speed, 0)
        self.allowed_angles = list(range(25, 65))+list(range(115, 155))+list(range(-65, -25))+list(range(-155, -115))
        self.reset()
        self.speedup_counter = 0

    def update(self):
        self.speedup_counter += 1
        if self.speedup_counter == 400:
            print("Speedup coming up")
        if self.speedup_counter > 600:
            self.speedup_counter = 0
            self.velocity.length += 0.5
        newpos = self.rect.move(*self.velocity)
        for paddle in self.paddles:
            reduced_paddle = paddle.rect.inflate(-4, 0)
            if newpos.colliderect(reduced_paddle):
                if reduced_paddle.top < self.rect.centery < reduced_paddle.bottom:
                    self.velocity.x *= -1
                    if paddle.side == Side.left:
                        newpos.left = reduced_paddle.right
                    elif paddle.side == Side.right:
                        newpos.right = reduced_paddle.left
                    if self.rect.centery > reduced_paddle.centery + reduced_paddle.height * 0.2:
                        self.velocity.y += 1
                        if rad_to_deg(self.velocity.angle) not in self.allowed_angles:
                            self.velocity.y -= 1
                    elif self.rect.centery < reduced_paddle.centery - reduced_paddle.height * 0.2:
                        self.velocity -= 1
                        if rad_to_deg(self.velocity.angle) not in self.allowed_angles:
                            self.velocity.y += 1
                else:
                    self.velocity.y *= -1
        if not newpos.colliderect(self.field.get_rect().inflate(-2*self.rect.width, -2*self.rect.height)):
            if newpos.left < 0:
                raise BallOutOfField(Side.left)
            elif newpos.right > self.field.get_rect().width:
                raise BallOutOfField(Side.right)
            elif newpos.top < 0 or newpos.bottom > self.field.get_rect().height:
                self.velocity.y *= -1
            newpos = self.rect.move(*self.velocity)
        self.rect = newpos
##        print "Ball's angle: {}pi".format(self.velocity.angle/math.pi)

    def reset(self):
        angle = deg_to_rad(random.choice(self.allowed_angles)) # So that angles are not too horizontal or vertical
        print("Ball's angle: {}".format(rad_to_deg(angle)))
        print("Bad? {}".format("No" if rad_to_deg(angle) in self.allowed_angles else "Yes"))
        self.velocity.angle = angle
##        self.velocity.length = self.initial_speed
        print("Speed: x={}, y={}".format(self.velocity.x, self.velocity.y))
        self.rect.center = (self.field.get_width()/2, self.field.get_height()/2)


class Paddle(pygame.sprite.Sprite):
    BAT_TO_WALL_DISTANCE = 20
    def __init__(self, field, image, side, speed):
        """__init__(self, field, image, side)

field should be a surface
image should be the paddle's picture
side should be either Side.left or Side.right
speed should be in pixels per frame"""
        pygame.sprite.Sprite.__init__(self)
        self.field = field
        self.image = image
        self.rect = image.get_rect()
        self.side = side
        self.default_speed = speed
        self.velocity = vector_from_polar(speed, 0)
        self.moving = False
        self.frames_moving = 0
        if self.side == Side.left:
            self.rect.midleft = (Paddle.BAT_TO_WALL_DISTANCE, self.field.get_height()/2)
        elif self.side == Side.right:
            self.rect.midright = (self.field.get_width()-Paddle.BAT_TO_WALL_DISTANCE, self.field.get_height()/2)

    def update(self):
        if not self.moving:
            return
        newpos = self.rect.move(*self.velocity)
        if newpos.top < 0 or newpos.bottom > self.field.get_height():
            self.stop()
            return
        self.rect = newpos
        self.frames_moving += 1
        if self.velocity.length < self.default_speed * 2:
            self.velocity.length = self.default_speed + 2 * math.log(self.frames_moving)

    def stop(self):
        self.moving = False
        self.frames_moving = 0

    def begin_moving_up(self):
        self.velocity.angle = -math.pi/2
        self.velocity.length = self.default_speed
        self.moving = True

    def begin_moving_down(self):
        self.velocity.angle = math.pi/2
        self.velocity.length = self.default_speed
        self.moving = True