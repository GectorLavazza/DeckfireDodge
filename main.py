import pygame

from sys import exit
from time import time

from bullets import BulletSpawner
from player import Player
from settings import SW, SH, CENTER
from ui import Text

from card import CardManager


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
    card_manager = CardManager(screen, player)
    bullet_spawner = BulletSpawner(screen, player, card_manager)


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

                if event.key == pygame.K_r:
                    if not card_manager.playing:
                        card_manager.new_game('bullets')
                if event.key == pygame.K_f:
                    card_manager.finish()

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
        player_g.draw(screen)
        bullet_spawner.draw()

        if not card_manager.playing:
            player_g.update(dt)
            bullet_spawner.update(dt)

        card_manager.update(dt)

        if player.health > 0:
            t = round(time() - st, 1)

        health.update(player.health)
        timer.update(t)

        pygame.display.flip()
        clock.tick()

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
