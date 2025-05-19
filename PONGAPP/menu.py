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
    WHITE, BLACK, POS_Y_TITRE, MENU_OPTIONS_SPACING,
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


def get_pos_x_titre(titre, window_width):
    """
    Calcule la position X pour centrer le text sur l'écran.

    Args:
        titre (pygame.Surface): Surface du text déjà rendue.

    Returns:
        int: La position X pour centrer le titre.
    """
    return window_width // 2 - titre.get_width() // 2


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
    top_visible = 0  # Index de la première option visible
    arrow_img = load_arrow(font)

    while True:
        screen.fill(BLACK)
        titre = font.render("PONG", True, WHITE)

        # Calcul de l'espace disponible et du nombre d'options visibles
        screen_height = screen.get_height()
        title_padding = titre.get_height() + 20
        available_height = screen_height - title_padding - 40
        max_visible = max(1, available_height // MENU_OPTIONS_SPACING)  # Au moins 1 option visible

        # Ajuster top_visible pour que la sélection soit toujours visible
        if selection < top_visible:
            top_visible = selection
        elif selection >= top_visible + max_visible:
            top_visible = selection - max_visible + 1
        # Afficher le titre en haut et centré
        title_y = int(screen.get_height() * 0.1)
        screen.blit(titre, (get_pos_x_titre(titre, screen.get_width()), title_y))

        # Afficher seulement les options visibles
        for i in range(top_visible, min(top_visible + max_visible, len(options))):
            option = options[i]
            text_surface = font.render(option, True, WHITE)
            x_text = get_pos_x_titre(text_surface, screen.get_width())
            # Espace de l'option = (index visible - 0) * espacement + décalage du titre
            title_gap = title_y + titre.get_height() + 30
            y_text = (i - top_visible) * MENU_OPTIONS_SPACING + title_gap

            if i == selection:
                x_arrow = x_text - arrow_img.get_width() - ALLIGN_TEXT_PADDING
                y_arrow = y_text + get_centered_y(text_surface, arrow_img)
                screen.blit(arrow_img, (x_arrow, y_arrow))

            screen.blit(text_surface, (x_text, y_text))

        # Indicateurs de défilement si nécessaire
        if top_visible > 0:
            # Afficher indicateur "plus d'options au-dessus"
            up_text = font.render("▲", True, WHITE)
            screen.blit(up_text, (screen.get_width() // 2, title_padding // 4))

        if top_visible + max_visible < len(options):
            # Afficher indicateur "plus d'options en-dessous"
            down_text = font.render("▼", True, WHITE)
            screen.blit(down_text, (screen.get_width() // 2, screen_height - 20))

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
    options = ["Taille des paddles", "Taille de la balle", "Taille de l'écran", "Retour"]
    selection = 0
    top_visible = 0  # Index de la première option visible
    arrow_img = load_arrow(font)

    while True:
        # Affichage du menu
        screen.fill(BLACK)
        titre = font.render("PARAMÈTRES", True, WHITE)
        titre_height = titre.get_height()
        
        # Calcul de l'espace disponible et du nombre d'options visibles
        screen_height = screen.get_height()
        title_y = int(screen_height * 0.1)  # 10% of screen height for title position
        available_height = screen_height - (title_y + titre_height + 30) - 40  # Available height for options
        max_visible = max(1, available_height // MENU_OPTIONS_SPACING)  # At least 1 option visible
        
        # Ajuster top_visible pour que la sélection soit toujours visible
        if selection < top_visible:
            top_visible = selection
        elif selection >= top_visible + max_visible:
            top_visible = selection - max_visible + 1
            
        # Afficher le titre en haut et centré
        screen.blit(titre, (get_pos_x_titre(titre, screen.get_width()), title_y))
        title_gap = title_y + titre_height + 30  # 30 pixels extra space
        
        # Préparer et afficher les options visibles avec leurs valeurs actuelles
        for i in range(top_visible, min(top_visible + max_visible, len(options))):
            # Déterminer le texte à afficher selon l'option
            if i == 0:
                size_name = settings.get_current_paddle_name()
                text = f"Taille des paddles : [{size_name}]"
            elif i == 1:
                ball_name = settings.get_current_ball_name()
                text = f"Taille de la balle : [{ball_name}]"
            elif i == 2:
                screen_label = settings.get_current_screen_size_label()
                text = f"Taille de l'écran : [{screen_label}]"
            else:
                text = options[i]
                
            # Rendu et affichage du texte (USING SCROLLABLE POSITIONING)
            text_surface = font.render(text, True, WHITE)
            x_text = get_pos_x_titre(text_surface, screen.get_width())
            y_text = (i - top_visible) * MENU_OPTIONS_SPACING + title_gap
            screen.blit(text_surface, (x_text, y_text))
            
            # Afficher la flèche de sélection
            if i == selection:
                x_arrow = x_text - arrow_img.get_width() - ALLIGN_TEXT_PADDING
                y_arrow = y_text + get_centered_y(text_surface, arrow_img)
                screen.blit(arrow_img, (x_arrow, y_arrow))
                
        # Indicateurs de défilement si nécessaire
        if top_visible > 0:
            up_text = font.render("▲", True, WHITE)
            screen.blit(up_text, (screen.get_width() // 2, title_y // 2))
            
        if top_visible + max_visible < len(options):
            down_text = font.render("▼", True, WHITE)
            screen.blit(down_text, (screen.get_width() // 2, screen_height - 20))
            
        pygame.display.flip()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
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
                    
                # Modification de la taille de la balle
                elif event.key == pygame.K_LEFT and selection == 1:
                    settings.CURRENT_BALL_SIZE_INDEX = (settings.CURRENT_BALL_SIZE_INDEX - 1) % len(settings.BALL_SIZES)
                elif event.key == pygame.K_RIGHT and selection == 1:
                    settings.CURRENT_BALL_SIZE_INDEX = (settings.CURRENT_BALL_SIZE_INDEX + 1) % len(settings.BALL_SIZES)
                    
                # Modification de la taille de l'écran
                elif event.key == pygame.K_LEFT and selection == 2:
                    settings.taille_ecran_precedente()
                elif event.key == pygame.K_RIGHT and selection == 2:
                    settings.taille_ecran_suivante()
                    
                # Retour au menu principal
                elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and selection == 3:
                    return
