"""
Ce fichier gère les menus du jeu Pong.

Fonctions:
- charger_fleche(font): Charge/redimensionne l'image de la flèche.
- main_menu(screen, font): Affiche le menu principal et gère la navigation.
- parametres_menu(screen, font): Affiche le menu des paramètres et permet de revenir.

Modules:
- sys: Gestion de l'environnement Python.
- os: Gestion des chemins de fichiers.
- pygame: Bibliothèque pour créer des jeux.
- constants: Contient WIDTH, WHITE, BLACK.

Constantes:
- WIDTH: Largeur de la fenêtre.
- WHITE: Couleur blanche.
- BLACK: Couleur noire.
"""


import sys
import os
import pygame
from constants import WIDTH, WHITE, BLACK


def charger_fleche(font):
    """
    Charge et redimensionne l'image de la flèche pour correspondre à la hauteur du texte.

    Args:
        font (pygame.font.Font): La police utilisée pour calculer la hauteur du texte.

    Returns:
        pygame.Surface: L'image redimensionnée de la flèche.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fleche_path = os.path.join(base_dir, 'assets', 'fleche.png')  # Chemin mis à jour pour refléter le fichier de flèche
    image = pygame.image.load(fleche_path).convert_alpha()
    texte_temp = font.render("Test", True, WHITE)
    hauteur_texte = texte_temp.get_height()
    largeur = int(image.get_width() * (hauteur_texte / image.get_height()))
    image_redim = pygame.transform.smoothscale(image, (largeur, hauteur_texte))
    return image_redim


def main_menu(screen, font):
    """
    Affiche le menu principal du jeu Pong et gère la navigation entre les options.

    Args:
        screen (pygame.Surface): La surface d'affichage où le menu sera dessiné.
        font (pygame.font.Font): La police utilisée pour afficher le texte.

    Returns:
        str: L'option sélectionnée par l'utilisateur ("jouer", "paramètres" ou "quitter").
    """
    options = ["Jouer", "Paramètres", "Quitter"]
    selection = 0
    fleche_img = charger_fleche(font)

    while True:
        screen.fill(BLACK)
        titre = font.render("PONG", True, WHITE)
        screen.blit(titre, (WIDTH // 2 - titre.get_width() // 2, 80))

        for i, option in enumerate(options):
            text_surface = font.render(option, True, WHITE)
            x_text = WIDTH // 2 - text_surface.get_width() // 2
            y_text = 200 + i * 60

            if i == selection:
                x_fleche = x_text - fleche_img.get_width() - 10  # 10 px d’espace
                y_fleche = y_text + (text_surface.get_height() - fleche_img.get_height()) // 2
                screen.blit(fleche_img, (x_fleche, y_fleche))

            screen.blit(text_surface, (x_text, y_text))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection = (selection - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selection = (selection + 1) % len(options)
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return options[selection].lower()


def parametres_menu(screen, font):
    """
    Affiche le menu des paramètres du jeu Pong et permet de revenir au menu principal.

    Args:
        screen (pygame.Surface): La surface d'affichage où le menu sera dessiné.
        font (pygame.font.Font): La police utilisée pour afficher le texte.
    """
    fleche_img = charger_fleche(font)

    while True:
        screen.fill(BLACK)
        titre = font.render("PARAMÈTRES", True, WHITE)
        screen.blit(titre, (WIDTH // 2 - titre.get_width() // 2, 80))

        option = "Retour"
        text_surface = font.render(option, True, WHITE)
        x_text = WIDTH // 2 - text_surface.get_width() // 2
        y_text = 200

        x_fleche = x_text - fleche_img.get_width() - 10
        y_fleche = y_text + (text_surface.get_height() - fleche_img.get_height()) // 2
        screen.blit(fleche_img, (x_fleche, y_fleche))
        screen.blit(text_surface, (x_text, y_text))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return
