from pygame import Surface, mouse, Vector2
from pygame.sprite import Sprite, Group
from ui import StaticText
from random import choice, sample
from settings import *


class CardManager:
    def __init__(self, screen, player):
        self.bullet_g = Group()
        self.player_g = Group()
        self.player = player
        self.screen = screen
        self.playing = False

    def new_game(self):
        self.player_cards = sample(CARDS, CARDS_AMOUNT)
        self.player_suits = sample(SUITS, CARDS_AMOUNT)
        self.player_abilities = sample(PLAYER_ABILITIES, CARDS_AMOUNT)

        self.bullet_cards = sample(CARDS, CARDS_AMOUNT)
        self.bullet_suits = sample(SUITS, CARDS_AMOUNT)
        self.bullet_abilities = sample(BULLET_ABILITIES, CARDS_AMOUNT)

        self.create_player_cards()
        self.create_bullet_cards()

        self.playing = True
        self.ending = False

    def create_player_cards(self):
        for i in range(CARDS_AMOUNT):
            pos = EDGE_OFFSET + OFFSET * i + CARD_W * i, SH - CARD_H // 4 * 3
            PlayerCard(pos, self.player, self.screen,
                       self.player_suits[i], self.player_cards[i], self.player_abilities[i],
                       self, self.player_g)

    def create_bullet_cards(self):
        for i in range(CARDS_AMOUNT):
            pos = EDGE_OFFSET + OFFSET * i + CARD_W * i, 0 - CARD_H // 4

            BulletCard(pos, self.player, self.screen,
                       self.bullet_suits[i], self.bullet_cards[i], self.bullet_abilities[i],
                       self, self.bullet_g)

    def update(self, dt):
        self.player_g.draw(self.screen)
        self.player_g.update(dt)

        self.bullet_g.draw(self.screen)
        self.bullet_g.update(dt)

class PlayerCard(Sprite):
    def __init__(self, pos, player, screen, suit, card, ability, card_manager, *group):
        super().__init__(*group)
        self.player = player
        self.screen = screen
        self.card_manager = card_manager

        self.image = Surface((CARD_W, CARD_H))
        self.image.fill('white')

        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0], SH

        color = COLORS[suit]
        self.card = StaticText(f'{suit} {card}',
                               self.image, (10, 10), 20, color=color)
        self.ability = StaticText(ability,
                                  self.image,
                                  (self.rect.w // 2, self.rect.h // 2 - 20),
                                  20, color=color,
                                  center_align=True, wrapping=True)

        self.pos = pos
        self.speed = 5

        self.starting = True

    def update(self, dt):
        if self.starting:
            self.rect.y -= self.speed * dt * 2 if self.rect.y >= self.pos[1] else 0
            if self.rect.y <= self.pos[1]:
                self.starting = False
        elif self.card_manager.ending:
            self.rect.y += self.speed * dt * 2 if self.rect.y <= SH else 0
            if self.rect.y >= SH:
                self.kill()
        else:
            mouse_pos = mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                if mouse.get_pressed()[0]:
                    pass
                self.rect.y -= self.speed * dt if self.rect.y >= self.pos[1] - 40 else 0
            else:
                self.rect.y += self.speed * dt if self.rect.y <= self.pos[1] else 0


class BulletCard(Sprite):
    def __init__(self, pos, player, screen, suit, card, ability, card_manager, *group):
        super().__init__(*group)
        self.player = player
        self.screen = screen
        self.card_manager = card_manager

        self.image = Surface((CARD_W, CARD_H))
        self.image.fill('white')

        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0], 0 - CARD_H

        suit, card = suit, card
        color = COLORS[suit]
        self.card = StaticText(f'{suit} {card}',
                               self.image, (CARD_W - 10, CARD_H - 30),
                               20, color=color,
                               right_align=True)
        self.ability = StaticText(ability,
                                  self.image,
                                  (self.rect.w // 2, self.rect.h // 2 - 20),
                                  20, color=color,
                                  center_align=True, wrapping=True)

        self.pos = pos
        self.speed = 5

        self.starting = True

    def update(self, dt):
        if self.starting:
            self.rect.y += self.speed * dt * 2 if self.rect.y <= self.pos[1] else 0
            if self.rect.y >= self.pos[1]:
                self.starting = False
        elif self.card_manager.ending:
            self.rect.y -= self.speed * dt * 2 if self.rect.y >= 0 - CARD_H else 0
            if self.rect.y <= 0 - CARD_H:
                self.kill()
        else:
            mouse_pos = mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                if mouse.get_pressed()[0]:
                    pass
                self.rect.y += self.speed * dt if self.rect.y <= self.pos[1] + 40 else 0
            else:
                self.rect.y -= self.speed * dt if self.rect.y >= self.pos[1] else 0
