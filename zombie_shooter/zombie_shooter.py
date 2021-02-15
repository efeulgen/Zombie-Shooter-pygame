import pygame
import sys
import random
import math
from pygame import mixer


class Shooter(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        if self.rect.centery != 620:
            self.rect.centery = 620


class Bullet(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.speed = speed

    def update(self):
        self.rect.centery -= self.speed
        if self.rect.centery <= -100:
            self.kill()


class Zombie(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed):
        super().__init__()
        self.undamaged = pygame.image.load(path)
        self.damaged = pygame.image.load('zombie_damaged.png')
        self.image = self.undamaged
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.health = 3

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed
        if self.rect.centery >= 720:
            self.kill()

    def get_damage(self):
        self.image = self.damaged
        self.health -= 1


def main():
    global gameOver
    global score_value
    screen.fill((255, 255, 255))
    # screen.blit(bg, bg_rect)
    display_score()

    shooter_group.draw(screen)
    shooter.update()

    bullet_group.draw(screen)
    bullet_group.update()

    zombie_group.draw(screen)
    zombie_group.update()

    # collision
    for bullet in bullet_group:
        for zombie in zombie_group:
            if bullet.rect.colliderect(zombie):
                bullet.kill()
                shot_sound = mixer.Sound('gore_shot_1.wav')
                shot_sound.play()
                zombie.get_damage()
                if zombie.health == 0:
                    score_value += 1
                    zombie_scream_sound = mixer.Sound('zombie_scream_1.wav')
                    zombie_scream_sound.play()
                    zombie.kill()

    # if pygame.sprite.spritecollide(shooter_group.sprite, zombie_group, True):
        # gameOver = True
    for zombie2 in zombie_group:
        if math.sqrt((math.pow(shooter.rect.centerx - zombie2.rect.centerx, 2)) +
                     (math.pow(shooter.rect.centery - zombie2.rect.centery, 2))) <= 40:
            gameOver = True


def game_over():
    game_over_text = game_font.render('GAME OVER', True, (0, 0, 0))
    game_over_text_rect = game_over_text.get_rect(center=(640, 360))
    screen.blit(game_over_text, game_over_text_rect)


def display_score():
    score_text = score_font.render('Score: ' + str(score_value), True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(80, 50))
    screen.blit(score_text, score_rect)


pygame.init()
screen = pygame.display.set_mode((1280, 720))
# bg = pygame.image.load('bg_1.png')
# bg_rect = bg.get_rect(center=(640, 360))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

mixer.music.load('game_music_3.wav')
mixer.music.play(-1)

# assets
shooter = Shooter('gun.png', 640, 620)
shooter_group = pygame.sprite.GroupSingle()
shooter_group.add(shooter)

bullet_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
game_font = pygame.font.Font('LazenbyCompSmooth.ttf', 80)

score_value = 0
score_font = pygame.font.Font('LazenbyCompSmooth.ttf', 30)

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
            bullet1 = Bullet('bullet.png', bullet_x, bullet_y, 20)
            bullet_group.add(bullet1)

        if event.type == ZOMBIE_EVENT:
            zombie_x = random.randrange(50, 1200)
            zombie_y = random.randrange(-150, -50)
            zombie1 = Zombie('zombie.png', zombie_x, zombie_y, random.randrange(-2, 2), random.randrange(4, 8))
            zombie_group.add(zombie1)

    if gameOver is False:
        main()

    else:
        game_over()

    pygame.display.update()
    clock.tick(60)
