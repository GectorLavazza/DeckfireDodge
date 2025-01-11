from random import choice, sample

from pygame import Surface, mouse
from pygame.sprite import Sprite, Group

from settings import *
from ui import StaticText


class CardManager:
    def __init__(self, screen, player):
        self.bullets_cards_g = Group()
        self.player_cards_g = Group()

        self.player = player
        self.screen = screen
        self.playing = False

        self.max_turn_timer = 120
        self.turn_timer = self.max_turn_timer

        self.current_player_abilities = []
        self.current_bullet_abilities = []

    def new_game(self, turn):
        self.turn = turn

        for c in self.player_cards_g.sprites():
            c.starting = True
        for c in self.bullets_cards_g.sprites():
            c.starting = True

        leftover_cards = [tuple(s.card[:2]) for s in
                          self.player_cards_g.sprites() + self.bullets_cards_g.sprites()]
        variants = [v for v in VARIANTS if v not in leftover_cards]

        cards = sample(variants, CARDS_AMOUNT * 2)
        self.player_cards = cards[:4]
        self.player_abilities = sample(PLAYER_ABILITIES, CARDS_AMOUNT)

        self.bullet_cards = cards[4:]
        self.bullet_abilities = sample(BULLET_ABILITIES, CARDS_AMOUNT)

        self.create_player_cards()
        self.create_bullet_cards()

        self.playing = True
        self.ending = False

        self.playing_card = None
        self.beating_card = None

    def create_player_cards(self):
        for i in range(CARDS_AMOUNT):
            pos = EDGE_OFFSET + OFFSET * i + CARD_W * i, SH - CARD_H // 4 * 3

            if any([c.rect.x == pos[0] for c in
                    self.player_cards_g.sprites()]):
                continue

            PlayerCard(pos, self.player, self.screen,
                       self.player_cards[i][0], self.player_cards[i][1],
                       self.player_abilities[i],
                       self, self.player_cards_g)

    def create_bullet_cards(self):
        for i in range(CARDS_AMOUNT):
            pos = EDGE_OFFSET + OFFSET * i + CARD_W * i, 0 - CARD_H // 4

            if any([c.rect.x == pos[0] for c in
                    self.bullets_cards_g.sprites()]):
                continue

            BulletCard(pos, self.player, self.screen,
                       self.bullet_cards[i][0], self.bullet_cards[i][1],
                       self.bullet_abilities[i],
                       self, self.bullets_cards_g)

    def update(self, dt):
        self.player_cards_g.draw(self.screen)
        self.player_cards_g.update(dt)

        self.bullets_cards_g.draw(self.screen)
        self.bullets_cards_g.update(dt)

        if self.playing:
            self.play(dt)

    def play(self, dt):
        bullets_variatns = self.get_variants(self.bullets_cards_g,
                                             self.player_cards_g)
        player_variatns = self.get_variants(self.player_cards_g,
                                            self.bullets_cards_g)

        if not any(bullets_variatns.values()) and not any(
                player_variatns.values()):
            self.turn = 'None'

        elif not any(bullets_variatns.values()) and any(
                player_variatns.values()):
            if self.turn == 'bullets':
                self.turn = 'player'

        elif not any(player_variatns.values()) and any(
                bullets_variatns.values()):
            if self.turn == 'player':
                self.turn = 'bullets'

        if self.turn == 'bullets':
            self.turn_timer -= dt
            if self.turn_timer < 0:
                self.take_turn()
                self.turn = 'player'
                self.turn_timer = self.max_turn_timer

    def beat(self, playing, beating):
        sp, cp = playing[:2]
        sb, cb = beating[:2]

        if sp == sb and CARDS.index(cp) > CARDS.index(cb):
            return True

        return False

    def take_turn(self):
        for card, variants in self.get_variants(self.bullets_cards_g,
                                                self.player_cards_g).items():
            if not variants:
                continue
            else:
                card.kill()
                choice(variants).kill()
                break

    def get_variants(self, g1, g2):
        res = {}
        for card in g1.sprites():
            variants = [c for c in g2.sprites() if
                        self.beat(card.card, c.card)]
            res[card] = variants
        return res

    def finish(self):
        self.ending = True
        self.playing = False


class PlayerCard(Sprite):
    def __init__(self, pos, player, screen, suit, card, ability, card_manager,
                 *group):
        super().__init__(*group)
        self.player = player
        self.screen = screen
        self.card_manager = card_manager

        self.image = Surface((CARD_W, CARD_H))
        self.image.fill('white')

        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0], SH

        self.card = suit, card, ability

        StaticText(f'{suit} {card}',
                   self.image, (10, 10), 20, color=COLORS[suit])
        StaticText(ability,
                   self.image,
                   (self.rect.w // 2, self.rect.h // 2 - 20),
                   20, color=COLORS[suit],
                   center_align=True, wrapping=True)

        self.pos = pos
        self.speed = 5

        self.starting = True
        self.new = True

    def update(self, dt):
        if self.starting:
            if self.new:
                spd = self.speed * 1.5
            else:
                spd = self.speed * 3
            self.rect.y -= spd * dt if self.rect.y >= self.pos[
                1] else 0
            if self.rect.y <= self.pos[1]:
                self.starting = False
                if self.new:
                    self.new = False

        elif self.card_manager.ending:
            self.rect.y += self.speed * dt * 2 if self.rect.y <= SH else 0
        else:
            mouse_pos = mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):

                if mouse.get_pressed()[0]:
                    self.take_turn()

                self.rect.y -= self.speed * dt if self.rect.y >= self.pos[
                    1] - 40 else 0
            else:
                self.rect.y += self.speed * dt if self.rect.y <= self.pos[
                    1] else 0

    def take_turn(self):
        if self.card_manager.turn == 'player':
            self.card_manager.playing_card = self


class BulletCard(Sprite):
    def __init__(self, pos, player, screen, suit, card, ability, card_manager,
                 *group):
        super().__init__(*group)
        self.player = player
        self.screen = screen
        self.card_manager = card_manager

        self.image = Surface((CARD_W, CARD_H))
        self.image.fill('white')

        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0], 0 - CARD_H

        self.card = suit, card, ability

        color = COLORS[suit]
        StaticText(f'{suit} {card}',
                   self.image, (CARD_W - 10, CARD_H - 30),
                   20, color=color,
                   right_align=True)
        StaticText(ability,
                   self.image,
                   (self.rect.w // 2, self.rect.h // 2 - 20),
                   20, color=color,
                   center_align=True, wrapping=True)

        self.pos = pos
        self.speed = 5

        self.starting = True
        self.pressed = False
        self.new = True

    def update(self, dt):
        if self.starting:
            if self.new:
                spd = self.speed * 1.5
            else:
                spd = self.speed * 3
            self.rect.y += spd * dt if self.rect.y <= self.pos[
                1] else 0
            if self.rect.y >= self.pos[1]:
                self.starting = False
                if self.new:
                    self.new = False
        elif self.card_manager.ending:
            self.rect.y -= self.speed * dt * 2 if self.rect.y >= 0 - CARD_H else 0
        else:
            mouse_pos = mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                if mouse.get_pressed()[0]:
                    if self.card_manager.turn == 'player':
                        if not self.pressed:
                            if self.card_manager.playing_card:
                                self.pressed = True
                                self.get_beaten()
            else:
                if not any(mouse.get_pressed()):
                    self.pressed = False

    def get_beaten(self):
        if self.card_manager.beat(self.card_manager.playing_card.card,
                                  self.card):
            self.card_manager.playing_card.kill()
            self.card_manager.turn = 'bullets'
            self.kill()
