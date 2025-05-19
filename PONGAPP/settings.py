"""
settings.py

Ce module gère les paramètres dynamiques du jeu Pong,
notamment la taille courante des paddles sélectionnée dans le menu des paramètres.
"""

from constants import PADDLE_SIZES

# Index de la taille de paddle actuellement sélectionnée (par défaut : Moyen)
CURRENT_PADDLE_SIZE_INDEX = 1


def get_current_paddle_height():
    """Retourne la hauteur de paddle actuellement sélectionnée."""
    return PADDLE_SIZES[CURRENT_PADDLE_SIZE_INDEX][1]


def get_current_paddle_name():
    """Retourne le nom affiché de la taille de paddle actuellement sélectionnée."""
    return PADDLE_SIZES[CURRENT_PADDLE_SIZE_INDEX][0]


SCREEN_SIZES = [
    ("600x300", 600, 300),
    ("800x400", 800, 400),
    ("Fullscreen", 0, 0)
]
CURRENT_SCREEN_SIZE_INDEX = 1 # 800x400 par défaut


def get_current_screen_size():
    """Retourne la largeur et la hauteur de l'écran actuellement sélectionné."""
    return SCREEN_SIZES[CURRENT_SCREEN_SIZE_INDEX][1:3]


def get_current_screen_size_label():
    """Retourne le label de la taille d'écran actuellement sélectionnée."""
    return SCREEN_SIZES[CURRENT_SCREEN_SIZE_INDEX][0]


def taille_ecran_suivante():
    """Passe à la taille d'écran suivante dans la liste des tailles disponibles."""
    global CURRENT_SCREEN_SIZE_INDEX
    CURRENT_SCREEN_SIZE_INDEX = (CURRENT_SCREEN_SIZE_INDEX + 1) % len(SCREEN_SIZES)


def taille_ecran_precedente():
    """Passe à la taille d'écran précédente dans la liste des tailles disponibles."""
    global CURRENT_SCREEN_SIZE_INDEX
    CURRENT_SCREEN_SIZE_INDEX = (CURRENT_SCREEN_SIZE_INDEX - 1) % len(SCREEN_SIZES)

# Liste des tailles de balle (nom affiché, taille en pixels)
BALL_SIZES = [
    ("Petite", 7),
    ("Moyenne", 15),
    ("Grande", 30)
]
CURRENT_BALL_SIZE_INDEX = 1  # Normale par défaut

def get_current_ball_size():
    """Retourne la taille de balle actuellement sélectionnée."""
    return BALL_SIZES[CURRENT_BALL_SIZE_INDEX][1]

def get_current_ball_name():
    """Retourne le nom affiché de la taille de balle actuellement sélectionnée."""
    return BALL_SIZES[CURRENT_BALL_SIZE_INDEX][0]