import pygame
from assets import screen


def game_over():
    game_font = pygame.font.Font('fonts/LazenbyCompSmooth.ttf', 80)
    game_over_text = game_font.render('GAME OVER', True, (0, 0, 0))
    game_over_text_rect = game_over_text.get_rect(center=(640, 360))
    screen.blit(game_over_text, game_over_text_rect)


score_value = 0


def display_score():
    score_font = pygame.font.Font('fonts/LazenbyCompSmooth.ttf', 30)
    score_text = score_font.render('Score: ' + str(score_value), True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(80, 50))
    screen.blit(score_text, score_rect)
