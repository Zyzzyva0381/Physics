import pygame
import sys
import math
from pygame.locals import *

__author__ = "Zyzzyva038"


class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __repr__(self):
        return "(x: %.3f, y: %.3f, length: %.3f)" % (self.x, self.y, self.length)

    def to_tuple(self):
        return int(self.x), int(self.y)

    __str__ = __repr__

    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        if self.x == 0 and self.y == 0:
            return Vector(1, 0)
        return Vector(self.x / self.length, self.y / self.length)


class Ball(object):
    def __init__(self, mass, pos_x, pos_y):
        self.mass = mass
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.resultant = Vector(0, 0)
        self.position = Vector(pos_x, pos_y)

    def apply_force(self, force):
        self.resultant += force

    def apply_drag(self, constant):
        if self.velocity != Vector(0, 0):
            self.apply_force(-self.velocity.normalize() * ((self.velocity.length * self.velocity.length) * constant))

    def update(self):
        self.acceleration = self.resultant / self.mass
        self.resultant = Vector(0, 0)
        self.velocity += self.acceleration
        self.position += self.velocity

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (int(self.position.x), int(self.position.y)), self.mass)

    def show(self):
        print(f"v: {self.velocity}, \na: {self.acceleration}, \npos: {self.position}\n")


class Spring(object):
    def __init__(self, anchor_x, anchor_y, rest_length, stiffness):
        self.anchor = Vector(anchor_x, anchor_y)
        self.rest_length = rest_length
        self.stiffness = stiffness
        self.length = -1  # not a valid number

    def connect(self, ball):
        self.length = self.anchor - ball.position
        direction = self.length.normalize()
        power = self.length.length - self.rest_length
        return direction * power * self.stiffness

    def draw(self, ball, screen):
        pygame.draw.line(screen, (0, 0, 0), (self.anchor.x, self.anchor.y), (ball.position.x, ball.position.y))


def test():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    fps_clock = pygame.time.Clock()
    fps = 80

    ball_mass = 30
    gravity_acceleration = 2

    ball = Ball(ball_mass, 100, 50)
    # gravity = Vector(0, gravity_acceleration * ball.mass)
    gravity_direction = - math.pi / 2
    gravity_mod = gravity_acceleration * ball.mass
    gravity = Vector(gravity_mod * math.cos(gravity_direction), - gravity_mod * math.sin(gravity_direction))
    # ball.velocity = Vector(30, 0)

    spring = Spring(400, 50, 300, 1)

    while True:
        screen.fill((255, 255, 255))
        ball.apply_force(gravity)
        elastic = spring.connect(ball)
        ball.apply_force(elastic)
        ball.apply_drag(0.0005)
        ball.update()
        ball.draw(screen)
        spring.draw(ball, screen)
        pygame.display.update()

        check_quit()

        fps_clock.tick(fps)
        print(spring.length.length)


def check_quit():
    for _ in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYDOWN):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()


def sign(a):
    if a > 0:
        return 1
    return 0


def reflection(point, slope, const):
    return Vector(point.y, point.x)  # TODO finish the function


if __name__ == "__main__":
    test()
