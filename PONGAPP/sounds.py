import os
import pygame

def init_sounds():
    pygame.mixer.init()
    # Récupérer le dossier où se trouve ce script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construire le chemin absolu vers chaque fichier son
    ping_a_path = os.path.join(base_dir, 'assets', '4359__noisecollector__pongblipf4.wav')
    pong_b_path = os.path.join(base_dir, 'assets', '4388__noisecollector__pongblipe5.wav')
    pingpong_c_path = os.path.join(base_dir, 'assets', '475557__rannem__bip.wav')

    # Charger les sons avec les chemins absolus
    ping_a = pygame.mixer.Sound(ping_a_path)
    pong_b = pygame.mixer.Sound(pong_b_path)
    pingpong_c = pygame.mixer.Sound(pingpong_c_path)
    return ping_a, pong_b, pingpong_c
