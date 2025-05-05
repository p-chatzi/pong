import pygame
from constants import WIDTH, HEIGHT, BALLE_SIZE, BALLE_VITESSE_INIT_X, BALLE_VITESSE_INIT_Y

def reset_balle():
    balle = pygame.Rect(WIDTH // 2 - BALLE_SIZE // 2, HEIGHT // 2 - BALLE_SIZE // 2, BALLE_SIZE, BALLE_SIZE)
    balle_vitesse_x = BALLE_VITESSE_INIT_X
    balle_vitesse_y = BALLE_VITESSE_INIT_Y
    last_speedup = pygame.time.get_ticks()
    return balle, balle_vitesse_x, balle_vitesse_y, last_speedup