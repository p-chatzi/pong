"""
Constantes pour le jeu Pong : dimensions, couleurs, speeds, scores, bonus et paramètres divers.
"""

# Dimensions de l'écran
WIDTH, HEIGHT = 1000, 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# parametres de jeu
PADDLE_A_X = 30
PADDLE_B_X_OFFSET = 40
SCORE_Y = 20
TIME_Y_OFFSET = 0.05 # Pourcentage de la hauteur de l'écran
RESET_DELAY_MS = 700
WINNER_DISPLAY_MS = 2000
SPEEDUP_INTERVAL = 10000  # 10 secondes
SPEEDUP_FACTOR = 1.5  # facteur acceleration
WIN_SCORE = 1
BALL_SIZE = 15
BALL_SPEED_INIT_X = 5
BALL_SPEED_INIT_Y = 5
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 15
FONT_SIZE = 30 # Taille de la police par defaut
PADDEL_MARGIN_X = 30
END_TEXT_OFFSET_Y = 50

# Paramètres des bonus
BONUS_RADIUS = 25
BONUS_SPAWN_INTERVAL = 15000  # 15 secondes
BONUS_DURATION = 10000  # 10 secondes
BONUS_BLINK_INTERVAL = 20  # Pour le clignotement
BONUS_MARGIN_X = 50
BONUS_LEFT_ZONE = WIDTH // 3
BONUS_RIGHT_ZONE = WIDTH * 2 // 3
BONUS_INFO_Y_PLAYER1 = 10
BONUS_INFO_Y_PLAYER2 = 30
BONUS_FONT_SIZE = 20
BONUS_INFO_FONT_SIZE = 24
SPEED_BOOST = 1.8
SPEED_SLOW = 0.6
SIZE_BOOST = 1.5

# Affichage menu
POS_Y_TITRE = 80
MENU_OPTIONS_START_Y = 200
MENU_OPTIONS_SPACING = 60
ALLIGN_TEXT_PADDING = 10
Y_TEXT = 200

# Tailles des paddles (nom affiché, hauteur)
PADDLE_SIZES = [
    ("Petit", 30),
    ("Moyen", 100),
    ("Grand", 200)
]
CURRENT_PADDLE_SIZE_INDEX = 1  # Taille moyen par défaut
PADDLE_HEIGHT = PADDLE_SIZES[CURRENT_PADDLE_SIZE_INDEX][1]

FPS = 60
