"""
Initialise et charge les sons du jeu depuis le dossier 'assets' en utilisant pygame.mixer.
"""


import os
import pygame


def init_sounds():
    """
    Initialise les sons pour le jeu Pong.

    Cette fonction configure le module mixer de Pygame, détermine les chemins absolus
    des fichiers audio nécessaires et charge ces sons pour une utilisation ultérieure.

    Retourne :
        tuple : Contient trois objets pygame.mixer.Sound correspondant aux sons chargés.
    """
    pygame.mixer.init()
    # Récupérer le dossier où se trouve ce script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construire le chemin absolu vers chaque fichier son
    ping_a_path = os.path.join(base_dir, 'assets', 'ping_a.wav')
    pong_b_path = os.path.join(base_dir, 'assets', 'pong_b.wav')
    ping_pong_c_path = os.path.join(base_dir, 'assets', 'ping_pong_c.wav')

    # load les sons avec les chemins absolus
    ping_a = pygame.mixer.Sound(ping_a_path)
    pong_b = pygame.mixer.Sound(pong_b_path)
    ping_pong_c = pygame.mixer.Sound(ping_pong_c_path)
    return ping_a, pong_b, ping_pong_c
