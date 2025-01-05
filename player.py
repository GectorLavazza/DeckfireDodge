from pygame import Vector2, Surface
from pygame.sprite import Sprite

from settings import SW, SH, CENTER


class Player(Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Surface((40, 40))
        self.image.fill('blue')

        self.rect = self.image.get_rect()
        self.rect.center = CENTER

        self.input = Vector2(0, 0)

        self.speed = 10
        self.velocity = Vector2(0, 0)

        self.max_health = 10
        self.health = self.max_health

        self.is_dashing = False
        self.is_sprinting = False
        self.dash_tick = 5

    def update(self, dt):
        if self.is_sprinting:
            self.speed = 15
        else:
            if self.is_dashing:
                self.dash_tick -= dt
                if self.dash_tick <= 0:
                    self.is_dashing = False
                    self.speed = 10
            else:
                self.speed = 10

        self.move(dt)

    def move(self, dt):
        if self.input.length() > 0:
            self.input = self.input.normalize()

        self.velocity.x = self.input.x * dt * self.speed
        self.velocity.y = self.input.y * dt * self.speed

        if 0 <= self.rect.x + self.velocity.x <= SW - self.rect.w:
            self.rect.centerx += self.velocity.x
        if 0 <= self.rect.y + self.velocity.y <= SH - self.rect.h:
            self.rect.centery += self.velocity.y

    def dash(self):
        self.speed = 50
        self.is_dashing = True
        self.dash_tick = 5
