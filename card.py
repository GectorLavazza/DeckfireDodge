from pygame import Surface, mouse
from pygame.sprite import Sprite


class Card(Sprite):
    def __init__(self, pos, player, screen, *group):
        super().__init__(*group)
        self.player = player
        self.screen = screen

        self.image = Surface((250, 350))
        self.image.fill('white')

        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.pos = pos
        self.speed = 5

    def update(self, dt):
        mouse_pos = mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.rect.y -= self.speed * dt if self.rect.y >= self.pos[1] - 40 else 0
        else:
            self.rect.y += self.speed * dt if self.rect.y <= self.pos[1] else 0
