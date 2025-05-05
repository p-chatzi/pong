import sys
import pygame
from constants import WIDTH, HEIGHT
from menu import main_menu, parametres_menu
from game import PongGame

def wait_for_key(screen, font):
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