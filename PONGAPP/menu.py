"""
Ce fichier gère les menus du jeu Pong.

Fonctions:
- get_pos_x_titre(titre): Calcule la position X pour centrer le titre.
- get_centered_y(text_surface, arrow_img): Calcule la position Y pour centrer une image par rapport à un text.
- load_arrow(font): Charge/redimensionne l'image de la flèche.
- main_menu(screen, font): Affiche le menu principal et gère la navigation.
- parametres_menu(screen, font): Affiche le menu des paramètres et permet de modifier la taille des paddles.

Modules:
- sys: Gestion de l'environnement Python.
- os: Gestion des chemins de fichiers.
- pygame: Bibliothèque pour créer des jeux.
- constants: Contient toutes les constantes du jeu.
- settings: Gère l'état mutable des paramètres.
"""

import sys
import os
import pygame
from constants import (
    WIDTH, WHITE, BLACK, POS_Y_TITRE, MENU_OPTIONS_SPACING,
    MENU_OPTIONS_START_Y, ALLIGN_TEXT_PADDING, PADDLE_SIZES
)
import settings

def load_arrow(font):
    """
    Charge et redimensionne l'image de la flèche pour correspondre à la height du text.

    Args:
        font (pygame.font.Font): La police utilisée pour calculer la height du text.

    Returns:
        pygame.Surface: L'image redimensionnée de la flèche.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    arrow_path = os.path.join(base_dir, 'assets', 'arrow.png')
    image = pygame.image.load(arrow_path).convert_alpha()
    text_temp = font.render("Test", True, WHITE)
    height_text = text_temp.get_height()
    width = int(image.get_width() * (height_text / image.get_height()))
    image_resized = pygame.transform.smoothscale(image, (width, height_text))
    return image_resized

def get_pos_x_titre(titre):
    """
    Calcule la position X pour centrer le text sur l'écran.

    Args:
        titre (pygame.Surface): Surface du text déjà rendue.

    Returns:
        int: La position X pour centrer le titre.
    """
    return WIDTH // 2 - titre.get_width() // 2

def get_centered_y(text_surface, arrow_img):
    """
    Calcule la position Y pour centrer verticalement une image (ex: flèche)
    par rapport à une surface de text.

    Args:
        text_surface (pygame.Surface): Surface du text rendue.
        arrow_img (pygame.Surface): Surface de l'image à aligner.

    Returns:
        int: Décalage Y pour centrer l'image sur le text.
    """
    return (text_surface.get_height() - arrow_img.get_height()) // 2

def main_menu(screen, font):
    """
    Affiche le menu principal du jeu Pong et gère la navigation entre les options.

    Args:
        screen (pygame.Surface): La surface d'affichage où le menu sera dessiné.
        font (pygame.font.Font): La police utilisée pour afficher le text.

    Returns:
        str: L'option sélectionnée par l'utilisateur ("jouer", "paramètres" ou "quitter").
    """
    options = ["Jouer", "Paramètres", "Quitter"]
    selection = 0
    arrow_img = load_arrow(font)

    while True:
        screen.fill(BLACK)
        titre = font.render("PONG", True, WHITE)
        screen.blit(titre, (get_pos_x_titre(titre), POS_Y_TITRE))

        for i, option in enumerate(options):
            text_surface = font.render(option, True, WHITE)
            x_text = get_pos_x_titre(text_surface)
            y_text = MENU_OPTIONS_START_Y + i * MENU_OPTIONS_SPACING

            if i == selection:
                x_arrow = x_text - arrow_img.get_width() - ALLIGN_TEXT_PADDING
                y_arrow = y_text + get_centered_y(text_surface, arrow_img)
                screen.blit(arrow_img, (x_arrow, y_arrow))

            screen.blit(text_surface, (x_text, y_text))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection = (selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selection = (selection + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return options[selection].lower()

def parametres_menu(screen, font):
    """
    Affiche le menu des paramètres et permet de modifier la taille des paddles.
    Navigation identique au menu principal.
    """
    options = ["Taille des paddles", "Taille de l'écran","Retour"]
    selection = 0
    arrow_img = load_arrow(font)

    while True:
        # Affichage du menu
        screen.fill(BLACK)
        titre = font.render("PARAMÈTRES", True, WHITE)
        screen.blit(titre, (get_pos_x_titre(titre), POS_Y_TITRE))

        for i, option in enumerate(options):
            # Affichage de la taille des paddles
            if i == 0:
                size_name = settings.get_current_paddle_name()
                text = f"Taille des paddles : [{size_name}]"

            # Affichage de la taille de l'écran
            if i == 1:
                screen_label = settings.get_current_screen_size_label()
                text = f"Taille de l'écran : [{screen_label}]"

            elif i == 2:
                text = option

            # Rendu du text
            text_surface = font.render(text, True, WHITE)
            x_text = get_pos_x_titre(text_surface)
            y_text = MENU_OPTIONS_START_Y + i * MENU_OPTIONS_SPACING
            screen.blit(text_surface, (x_text, y_text))
            if i == selection:
                x_arrow = x_text - arrow_img.get_width() - ALLIGN_TEXT_PADDING
                y_arrow = y_text + get_centered_y(text_surface, arrow_img)
                screen.blit(arrow_img, (x_arrow, y_arrow))
        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Gestion des événements de navigation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection = (selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selection = (selection + 1) % len(options)

                # Modification de la taille des raquettes
                elif event.key == pygame.K_LEFT and selection == 0:
                    settings.CURRENT_PADDLE_SIZE_INDEX = (settings.CURRENT_PADDLE_SIZE_INDEX - 1) % len(PADDLE_SIZES)
                elif event.key == pygame.K_RIGHT and selection == 0:
                    settings.CURRENT_PADDLE_SIZE_INDEX = (settings.CURRENT_PADDLE_SIZE_INDEX + 1) % len(PADDLE_SIZES)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Retour au menu principal
                    if selection == 2:
                        return

                # Modification de la taille de l'écran
                elif event.key == pygame.K_RIGHT and selection == 1:
                    settings.CURRENT_SCREEN_SIZE_INDEX = (settings.CURRENT_SCREEN_SIZE_INDEX - 1) % len(settings.SCREEN_SIZES)
                elif event.key == pygame.K_LEFT and selection == 1:
                    settings.CURRENT_SCREEN_SIZE_INDEX = (settings.CURRENT_SCREEN_SIZE_INDEX + 1) % len(settings.SCREEN_SIZES)
                # Retour au menu principal
                    if selection == 2:
                        return
