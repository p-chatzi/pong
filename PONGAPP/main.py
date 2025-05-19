"""
Point d'entrée principal pour l'application Pong.
`
Fonctionnalités :
- Initialise Pygame et configure l'environnement.
- Affiche un menu principal avec jouer, paramètres ou quitter.
- Gère les interactioxns utilisateur et événements Pygame.
- Attend une entrée clavier avant de revenir au menu principal.

Fonctions :
- wait_for_key(screen, font): Affiche un message et attend une touche.
- main(): Orchestration principale de l'application.

Modules :
- sys : Quitte proprement l'application.
- pygame : Gestion graphique, événements et interactions utilisateur.
- constants : width et height de l'écran.
- menu : Menu principal et menu des paramètres.
- game : Classe PongGame pour la logique du jeu.
- settings : Gestion des paramètres dynamiques du jeu.
- os : Pour centrer la fenêtre de Pygame sur l'écran.

Exécution :
- À exécuter directement pour appeler la fonction main().
"""

import sys
import os
# Pour centrer la fenêtre de Pygame sur l'écran
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pygame
from constants import WHITE, END_TEXT_OFFSET_Y, FONT_SIZE
from menu import main_menu, parametres_menu
from game import PongGame
from settings import get_current_paddle_height, get_current_screen_size_label, get_current_screen_size


def wait_for_key(screen, font):
    """
    Affiche un message à l'écran et attend qu'une touche soit pressée pour continuer.

    Args:
        screen (pygame.Surface): La surface de l'écran où le text sera affiché.
        font (pygame.font.Font): La police utilisée pour rendre le text.
    """
    width = screen.get_width()
    height = screen.get_height()
    text = font.render("Appuyez sur une touche pour revenir au menu", True, WHITE)
    screen.blit(text, (width // 2 - text.get_width() // 2,
                       height // 2 - text.get_height() // 2 + END_TEXT_OFFSET_Y))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def main():
    """
    Fonction principale de l'application Pong.

    Fonctionnalités :
    - Initialise Pygame et configure l'écran.
    - Affiche le menu principal et gère les choix de l'utilisateur.
    - Lance le jeu Pong si l'utilisateur choisit "jouer".
    - Affiche le menu des paramètres si l'utilisateur choisit "paramètres".
    - Quitte l'application si l'utilisateur choisit "quitter".

    Aucune exception spécifique n'est gérée ici, donc les erreurs potentielles 
    liées à Pygame ou au système doivent être prises en compte dans les fonctions appelées.

    """
    # Initialisation de Pygame
    pygame.init()
    # Initialisation de la taille d'écran
    label = get_current_screen_size_label()
    width, height = get_current_screen_size()
    if label == "Fullscreen":
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        width, height = info.current_w, info.current_h
    else:
        screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Pong")
    font = pygame.font.SysFont("Arial", FONT_SIZE)

    # Boucle principale
    while True:
        choix = main_menu(screen, font)
        if choix == "jouer":
            # Récupération de la taille du paddle
            paddle_height = get_current_paddle_height()

            # Récupération de la taille de l'écran
            width, height = get_current_screen_size()
            label = get_current_screen_size_label()
            if label == "Fullscreen":
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                info = pygame.display.Info()
                width, height = info.current_w, info.current_h
            else:
                screen = pygame.display.set_mode((width, height))

            # Création de l'objet PongGame et lancement du jeu
            jeu = PongGame(paddle_height, width, height)
            jeu.screen = screen
            jeu.font = font
            jeu.run(screen)
            wait_for_key(screen, font)

        # On entre dans le menu des paramètres
        elif choix == "paramètres":
            parametres_menu(screen, font)
            width, height = get_current_screen_size()
            label = get_current_screen_size_label()
            if label == "Fullscreen":
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                info = pygame.display.Info()
                width, height = info.current_w, info.current_h
            else:
                screen = pygame.display.set_mode((width, height))

        # On quitte le jeu
        elif choix == "quitter":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
