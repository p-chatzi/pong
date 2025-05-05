import pygame

def init_sounds():
    pygame.mixer.init()
    ping_a = pygame.mixer.Sound('assets/4359__noisecollector__pongblipf4.wav')
    pong_b = pygame.mixer.Sound('assets/4388__noisecollector__pongblipe5.wav')
    pingpong_c = pygame.mixer.Sound('assets/475557__rannem__bip.wav')
    return ping_a, pong_b, pingpong_c
