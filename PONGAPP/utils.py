""" 
Module utilitaire pour le jeu Pong.

Fonctions:
- reset_ball: Réinitialise la ball au centre avec une speed aléatoire.
- format_time: Formate une durée en millisecondes en "minutes:secondes".
"""

import random
import pygame
from constants import WIDTH, HEIGHT, BALL_SIZE, BALL_SPEED_INIT_X, BALL_SPEED_INIT_Y

def reset_ball():
    """
    Réinitialise la ball au centre avec une speed aléatoire et retourne ses paramètres initiaux.
    """
    # Position initiale de la ball au centre de l'écran
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                    HEIGHT // 2 - BALL_SIZE // 2,
                    BALL_SIZE,
                    BALL_SIZE)

    # Vitesse initiale aléatoire
    ball_speed_x = random.choice([-1, 1]) * BALL_SPEED_INIT_X
    ball_speed_y = random.choice([-1, 1]) * BALL_SPEED_INIT_Y

    last_speedup = pygame.time.get_ticks()

    return ball, ball_speed_x, ball_speed_y, last_speedup

def format_time(milliseconds):
    """
    Formate une durée en millisecondes en une chaîne "minutes:secondes".

    Args:
        milliseconds (int): Durée en millisecondes.

    Returns:
        str: Durée formatée en "minutes:secondes".
    """

    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"
