from itertools import product

from pygame import Surface, mouse
from pygame.sprite import Sprite
from ui import StaticText
from random import choice, sample

SUITS = ('Diamonds', 'Hearts', 'Spears', 'Clubs')
COLORS = {
    'Diamonds': 'red',
    'Hearts': 'red',
    'Spears': 'black',
    'Clubs': 'black'
}
CARDS = ('6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
PLAYER_ABILITIES = ('dash', 'sprint', 'shield', 'heal', '- speed', '- frequency', 'small bullets')

current_abilities = sample(PLAYER_ABILITIES, 4)

class Card(Sprite):
    def __init__(self, pos, player, screen, *group):
        super().__init__(*group)
        self.player = player
        self.screen = screen

        self.image = Surface((250, 350))
        self.image.fill('white')

        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        suit, card = choice(SUITS), choice(CARDS)
        color = COLORS[suit]
        self.card = StaticText(f'{suit} {card}',
                               self.image, (10, 10), 20, color=color)
        self.ability = StaticText(choice(current_abilities),
                                  self.image,
                                  (self.rect.w // 2, self.rect.h // 2 - 20),
                                  20, color=color,
                                  center_align=True)

        self.pos = pos
        self.speed = 5

    def update(self, dt):
        mouse_pos = mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if mouse.get_pressed()[0]:
                self.rect.center = mouse_pos
            else:
                self.rect.y -= self.speed * dt if self.rect.y >= self.pos[1] - 40 else 0
                self.rect.x = self.pos[0]
        else:
            self.rect.y += self.speed * dt if self.rect.y <= self.pos[1] else 0
            self.rect.x = self.pos[0]
