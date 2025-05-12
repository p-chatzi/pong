"""
Constantes pour le jeu Pong : dimensions, couleurs, vitesses, scores, bonus et paramètres divers.
"""

WIDTH, HEIGHT = 1920, 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
FPS = 60

RAQUETTE_WIDTH, RAQUETTE_HEIGHT = 10, 100
RAQUETTE_VITESSE = 15

BALLE_SIZE = 15
BALLE_VITESSE_INIT_X = 5
BALLE_VITESSE_INIT_Y = 5

WIN_SCORE = 7

SPEEDUP_INTERVAL = 10000  # 10 secondes
SPEEDUP_FACTOR = 1.5  # facteur acceleration

# Paramètres des bonus
BONUS_RADIUS = 25
BONUS_SPAWN_INTERVAL = 15000  # 15 secondes
BONUS_DURATION = 10000  # 10 secondes
BONUS_BLINK_INTERVAL = 20  # Pour le clignotement