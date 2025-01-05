import pygame

from sys import exit
from time import time

from bullets import BulletSpawner
from player import Player
from settings import SW, SH, CENTER
from ui import Text

from card import Card


def main():
    pygame.init()
    pygame.display.set_caption('Deckfire Dodge')

    flags = pygame.DOUBLEBUF | pygame.SCALED
    screen = pygame.display.set_mode((SW, SH), flags, depth=8, vsync=1)

    clock = pygame.time.Clock()


    last_time = time()

    running = 1

    player_g = pygame.sprite.Group()
    player = Player(player_g)
    bullet_spawner = BulletSpawner(screen, player)

    cards_g = pygame.sprite.Group()
    for i in range(4):
        pos = 56 + (250 + 56) * i, 500
        Card(pos, player, screen, cards_g)


    health = Text(screen, (0, 0), 50)
    timer = Text(screen, (SW, 0), 50, right_align=True)

    st = time()

    while running:

        dt = time() - last_time
        dt *= 60
        last_time = time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = 0

                if event.key == pygame.K_F10:
                    pygame.display.toggle_fullscreen()

                if event.key == pygame.K_w:
                    player.input.y = -1
                if event.key == pygame.K_s:
                    player.input.y = 1
                if event.key == pygame.K_a:
                    player.input.x = -1
                if event.key == pygame.K_d:
                    player.input.x = 1
                if event.key == pygame.K_SPACE:
                    player.dash()
                if event.key == pygame.K_LSHIFT:
                    player.is_sprinting = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.input.y = 0
                if event.key == pygame.K_s:
                    player.input.y = 0
                if event.key == pygame.K_a:
                    player.input.x = 0
                if event.key == pygame.K_d:
                    player.input.x = 0
                if event.key == pygame.K_LSHIFT:
                    player.is_sprinting = False

        screen.fill('black')

        # player_g.draw(screen)
        cards_g.draw(screen)

        # player_g.update(dt)
        # bullet_spawner.update(dt)
        cards_g.update(dt)

        if player.health > 0:
            t = round(time() - st, 1)

        health.update(player.health)
        # timer.update(t)

        pygame.display.flip()
        clock.tick()

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
