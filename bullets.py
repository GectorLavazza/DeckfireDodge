from pygame.sprite import Group, Sprite
from pygame import Vector2, Surface
from settings import SW, SH, CENTER
from random import choice, choices


class BulletSpawner:
    def __init__(self, screen, player):
        self.screen = screen
        self.group = Group()

        self.player = player

        self.max_tick = 10
        self.tick = self.max_tick

        self.x = range(0, SW + 1)
        self.y = range(0, SH + 1)

    def update(self, dt):
        self.group.update(dt)
        self.group.draw(self.screen)

        self.handle_tick(dt)

    def handle_tick(self, dt):
        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick

            d = choice(('v', 'h'))
            if d == 'v':
                pos = (
                    choice(self.x),
                    choice((-10, SH + 10))
                )
            else:
                pos = (
                    choice((-10, SW + 10)),
                    choice(self.y)
                )

            self.create_bullet(pos, (choice(self.x), choice(self.y)))

    def create_bullet(self, pos, target_pos):
        Bullet(pos, target_pos, self, self.group)


class Bullet(Sprite):
    def __init__(self, pos, target_pos, spawner, *group):
        super().__init__(*group)
        self.spawner = spawner
        self.player = spawner.player
        self.screen_rect = self.spawner.screen.get_rect()

        self.image = Surface((20, 20))
        self.image.fill('red')
        self.rect = self.image.get_rect()

        self.rect.center = pos

        self.speed = 10

        self.direction = Vector2(target_pos) - Vector2(pos)

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

    def update(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        if not self.rect.colliderect(self.screen_rect):
            self.kill()

        if self.rect.colliderect(self.player.rect):
            self.player.health -= 1
            self.kill()
