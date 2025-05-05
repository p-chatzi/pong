import pygame
import random
from constants import WIDTH, HEIGHT, BALLE_SIZE, BALLE_VITESSE_INIT_X, BALLE_VITESSE_INIT_Y

def reset_balle():
    # Position initiale de la balle au centre de l'écran
    balle = pygame.Rect(WIDTH // 2 - BALLE_SIZE // 2, HEIGHT // 2 - BALLE_SIZE // 2, BALLE_SIZE, BALLE_SIZE)

    # Vitesse initiale aléatoire
    balle_vitesse_x = random.choice([-1, 1]) * BALLE_VITESSE_INIT_X
    balle_vitesse_y = random.choice([-1, 1]) * BALLE_VITESSE_INIT_Y

    last_speedup = pygame.time.get_ticks()

    return balle, balle_vitesse_x, balle_vitesse_y, last_speedup

def format_time(milliseconds):

    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"

