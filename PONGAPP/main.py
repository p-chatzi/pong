"""
Point d'entrée principal pour l'application Pong.

Fonctionnalités :
- Initialise Pygame et configure l'environnement.
- Affiche un menu principal avec jouer, paramètres ou quitter.
- Gère les interactions utilisateur et événements Pygame.
- Attend une entrée clavier avant de revenir au menu principal.

Fonctions :
- wait_for_key(screen, font): Affiche un message et attend une touche.
- main(): Orchestration principale de l'application.

Modules :
- sys : Quitte proprement l'application.
- pygame : Gestion graphique, événements et interactions utilisateur.
- constants : Largeur et hauteur de l'écran.
- menu : Menu principal et menu des paramètres.
- game : Classe PongGame pour la logique du jeu.

Exécution :
- À exécuter directement pour appeler la fonction main().
"""


import sys
import pygame
from constants import WIDTH, HEIGHT
from menu import main_menu, parametres_menu
from game import PongGame


def wait_for_key(screen, font):
    """
    Affiche un message à l'écran et attend qu'une touche soit pressée pour continuer.

    Args:
        screen (pygame.Surface): La surface de l'écran où le texte sera affiché.
        font (pygame.font.Font): La police utilisée pour rendre le texte.
    """
    text = font.render("Appuyez sur une touche pour revenir au menu", True, (255,255,255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + 60))
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
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    font = pygame.font.SysFont("Arial", 30)
    while True:
        choix = main_menu(screen, font)
        if choix == "jouer":
            jeu = PongGame()
            jeu.screen = screen
            jeu.font = font
            jeu.run()
            wait_for_key(screen, font)
        elif choix == "paramètres":
            parametres_menu(screen, font)
        elif choix == "quitter":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
