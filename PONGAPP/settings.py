"""
settings.py

Ce module gère les paramètres dynamiques du jeu Pong,
notamment la taille courante des paddles sélectionnée dans le menu des paramètres.
"""

from constants import PADDLE_SIZES

# Index de la taille de paddle actuellement sélectionnée (par défaut : Moyen)
CURRENT_PADDLE_SIZE_INDEX = 1

def get_current_paddle_height():
    """
    Retourne la hauteur de paddle actuellement sélectionnée.
    """
    return PADDLE_SIZES[CURRENT_PADDLE_SIZE_INDEX][1]

def get_current_paddle_name():
    """
    Retourne le nom affiché de la taille de paddle actuellement sélectionnée.
    """
    return PADDLE_SIZES[CURRENT_PADDLE_SIZE_INDEX][0]
