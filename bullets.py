from random import choice, randint

from pygame import Vector2, Surface
from pygame.sprite import Group, Sprite

from settings import SW, SH


class BulletSpawner:
    def __init__(self, screen, player, card_manager):
        self.screen = screen
        self.group = Group()

        self.player = player
        self.card_manager = card_manager
        self.abilities = self.card_manager.current_bullet_abilities
        self.bullets_speed_boost = self.card_manager.bullets_speed_boost
        self.bullets_frequency = self.card_manager.bullets_frequency

        self.max_tick = 10
        self.tick = self.max_tick

        self.x = range(0, SW + 1)
        self.y = range(0, SH + 1)

    def update(self, dt):
        self.group.update(dt)
        self.handle_tick(dt)
        self.abilities = self.card_manager.current_bullet_abilities
        self.bullets_speed_boost = self.card_manager.bullets_speed_boost
        self.bullets_frequency = self.card_manager.bullets_frequency

    def draw(self):
        self.group.draw(self.screen)

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
        if randint(1, 100) == 1 and not any(
                [type(s) == Item for s in self.group]):
            Item(pos, target_pos, self, self.group)
        else:
            if 'targets player' in self.abilities:
                tp = self.player.rect.center
            else:
                tp = target_pos
            Bullet(pos, tp, self, self.group)


class Bullet(Sprite):
    def __init__(self, pos, target_pos, spawner, *group):
        super().__init__(*group)
        self.spawner = spawner

        speed_boost = self.spawner.bullets_speed_boost

        self.player = spawner.player
        self.screen_rect = self.spawner.screen.get_rect()
        self.special = False

        if 'big bullets' in self.spawner.abilities and 'small bullets' not in self.spawner.player.abilities:
            size = (30, 30)
        elif 'big bullets' not in self.spawner.abilities and 'small bullets' in self.spawner.player.abilities:
            size = (10, 10)
        else:
            size = (20, 20)

        self.image = Surface(size)

        if randint(1, 10) == 1:
            self.image.fill('purple')
            self.special = True
        else:
            self.image.fill('red')

        self.rect = self.image.get_rect()

        self.rect.center = pos

        if 'random speed' in self.spawner.abilities:
            self.speed = randint(5, 15) + speed_boost
        else:
            self.speed = 10 + speed_boost

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
            if self.special:
                self.spawner.card_manager.new_game('bullets')
            self.kill()


class Item(Sprite):
    def __init__(self, pos, target_pos, spawner, *group):
        super().__init__(*group)
        self.spawner = spawner
        self.player = spawner.player
        self.screen_rect = self.spawner.screen.get_rect()

        self.image = Surface((30, 30))
        self.image.fill('green')
        self.rect = self.image.get_rect()

        self.rect.center = pos

        self.speed = randint(1, 10)

        self.direction = Vector2(target_pos) - Vector2(pos)

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

    def update(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        if not self.rect.colliderect(self.screen_rect):
            self.kill()

        if self.rect.colliderect(self.player.rect):
            self.spawner.card_manager.new_game('player')
            self.kill()
