import pygame
import sys
import random
import assets
import game_texts
from pygame import mixer
from assets import screen

pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

mixer.music.load('sfx/game_music_3.wav')
mixer.music.play(-1)

# assets
shooter = assets.Shooter('assets/gun.png', 640, 620)
shooter_group = pygame.sprite.GroupSingle(shooter)

bullet_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()

ZOMBIE_EVENT = pygame.USEREVENT
pygame.time.set_timer(ZOMBIE_EVENT, 250)

# game loop
gameOver = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet_x = shooter.rect.centerx - 8
            bullet_y = 570
            bullet1 = assets.Bullet('assets/bullet.png', bullet_x, bullet_y, 20)
            bullet_group.add(bullet1)

        if event.type == pygame.MOUSEMOTION:
            shooter.rect.centerx = event.pos[0]

        if event.type == ZOMBIE_EVENT:
            zombie_x = random.randrange(50, 1200)
            zombie_y = random.randrange(-150, -50)
            zombie1 = assets.Zombie('assets/zombie.png', zombie_x, zombie_y, random.randrange(-2, 2), random.randrange(4, 8))
            zombie_group.add(zombie1)

    if gameOver is False:
        screen.fill((255, 255, 255))
        game_texts.display_score()

        shooter_group.draw(screen)

        bullet_group.draw(screen)
        bullet_group.update()

        zombie_group.draw(screen)
        zombie_group.update()

        # collision
        for bullet in bullet_group:
            for zombie in zombie_group:
                if bullet.rect.colliderect(zombie):
                    bullet.kill()
                    shot_sound = mixer.Sound('sfx/gore_shot_1.wav')
                    shot_sound.play()
                    zombie.get_damage()
                    if zombie.health == 0:
                        game_texts.score_value += 1
                        zombie_scream_sound = mixer.Sound('sfx/zombie_scream_1.wav')
                        zombie_scream_sound.play()
                        zombie.kill()

        # game over
        if pygame.sprite.spritecollide(shooter_group.sprite, zombie_group, True):
            gameOver = True

    else:
        game_texts.game_over()

    pygame.display.update()
    clock.tick(60)
