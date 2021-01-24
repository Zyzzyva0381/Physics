from physics import Vector
import physics
import math
import pygame
import sys
from pygame.locals import *


class Oscillator(object):
    def __init__(self, vibrate=lambda x: math.sin(x), position=Vector(0, 0), threshold=500):
        self.position = position
        self.vibrate = vibrate
        self.is_active = False
        self.wave = None
        self.threshold = threshold

    def activate(self, velocity):
        self.is_active = True
        self.wave = Wave(velocity, self.vibrate, self.position)

    def deactivate(self):
        self.is_active = False

    def update(self, span):
        if not self.wave:
            return
        if not self.is_active:
            self.wave.sub_range += span * self.wave.velocity
        self.wave.range += span * self.wave.velocity
        if self.wave.sub_range > self.threshold:
            self.wave = None

    def strength(self, position):
        r = (position - self.position).length
        if self.wave and self.wave.sub_range < r < self.wave.range:
            return self.vibrate((self.wave.range - r) / self.wave.velocity)
        return 0

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), self.position.to_tuple(), 3)
        if self.wave:
            for radius in self.wave.sub_range, self.wave.range:
                if radius > 1:
                    pygame.draw.circle(screen, (255, 0, 0), self.position.to_tuple(), int(radius), 1)


class Wave(object):
    def __init__(self, velocity, vibrate, position):
        self.position = position
        self.velocity = velocity
        self.vibrate = vibrate
        self.range = 0
        self.sub_range = 0


class Plane(object):
    def __init__(self, slope=1, const=0):
        self.equation = lambda x: slope * x + const
        self.slope = slope
        self.const = const

    def wave(self, oscillators, point):
        strength = 0
        for oscillator in oscillators:
            if oscillator.position.y < self.equation(oscillator.position.x):
                if point.y > self.equation(point.x):
                    strength += -oscillator.strength(point)
                if point.y < self.equation(point.x):
                    strength += oscillator.strength(physics.reflection(point, self.slope, self.const))
            elif oscillator.position.y >= self.equation(oscillator.position.x):
                if point.y < self.equation(point.x):
                    strength += -oscillator.strength(point)
                if point.y > self.equation(point.x):
                    strength += oscillator.strength(physics.reflection(point, self.slope, self.const))
        return strength

    def draw(self, x_min, x_max):
        pygame.draw.line(screen, (0, 0, 0), (x_min, self.equation(x_min)), (x_max, self.equation(x_max)))


def main():
    global screen

    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    fps_clock = pygame.time.Clock()
    fps = 80

    oscillator = Oscillator(position=Vector(200, 300), vibrate=lambda a: math.sin(18 * a))
    oscillator2 = Oscillator(position=Vector(500, 300), vibrate=lambda a: math.sin(18 * a))
    velocity = 360

    plane = Plane()

    while True:

        for x in range(0, 800, 10):
            for y in range(0, 600, 10):
                strength = (oscillator.strength(Vector(x, y))
                            + oscillator2.strength(Vector(x, y))
                            + plane.wave((oscillator, oscillator2), Vector(x, y)))
                colored = 125 + 50 * strength
                pygame.draw.rect(screen, (colored, colored, colored), Rect((x, y), (x + 10, y + 10)))

        oscillator.update(1 / fps)
        oscillator.draw()
        oscillator2.update(1 / fps)
        oscillator2.draw()
        plane.draw(0, 800)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_w:
                    oscillator.activate(velocity)
                    oscillator2.activate(velocity)
                elif event.key == K_s:
                    oscillator.deactivate()
                    oscillator2.deactivate()
            elif event.type == MOUSEBUTTONUP:
                print(oscillator.strength(Vector(event.pos[0], event.pos[1])),
                      oscillator2.strength(Vector(event.pos[0], event.pos[1])))

        fps_clock.tick(fps)
        pygame.display.update()


if __name__ == "__main__":
    main()
