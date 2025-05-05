# game.py

import pygame
import sys
from constants import *
from sounds import init_sounds
from utils import reset_balle, format_time

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)

        self.raquette_a = pygame.Rect(30, HEIGHT // 2 - RAQUETTE_HEIGHT // 2, RAQUETTE_WIDTH, RAQUETTE_HEIGHT)
        self.raquette_b = pygame.Rect(WIDTH - 40, HEIGHT // 2 - RAQUETTE_HEIGHT // 2, RAQUETTE_WIDTH, RAQUETTE_HEIGHT)

        self.balle, self.balle_vitesse_x, self.balle_vitesse_y, self.last_speedup = reset_balle()

        self.score_a, self.score_b = 0, 0
        self.ping_a, self.pong_b, self.pingpong_c = init_sounds()
        self.winner = None
        self.paused = False
        self.start_time = pygame.time.get_ticks()
        self.running = True  # Ajout de l'attribut running

    def run(self):
        while self.running:  # Utilisation de self.running pour contrôler la boucle principale
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused

            if not self.paused:
                self.update(now)

            self.draw()

        self.show_winner()

    def update(self, now):
        if now - self.last_speedup > SPEEDUP_INTERVAL:
            self.balle_vitesse_x = int(self.balle_vitesse_x * SPEEDUP_FACTOR)
            self.balle_vitesse_y = int(self.balle_vitesse_y * SPEEDUP_FACTOR)
            self.last_speedup = now

        self.clock.tick(FPS)
        self.move_raquettes()
        self.move_balle()

    def move_raquettes(self):
        keys = pygame.key.get_pressed()
        raquette_a_up, raquette_a_down = pygame.K_z, pygame.K_s
        raquette_b_up, raquette_b_down = pygame.K_UP, pygame.K_DOWN

        if keys[raquette_a_up] and self.raquette_a.top > 0:
            self.raquette_a.y -= RAQUETTE_VITESSE
        if keys[raquette_a_down] and self.raquette_a.bottom < HEIGHT:
            self.raquette_a.y += RAQUETTE_VITESSE
        if keys[raquette_b_up] and self.raquette_b.top > 0:
            self.raquette_b.y -= RAQUETTE_VITESSE
        if keys[raquette_b_down] and self.raquette_b.bottom < HEIGHT:
            self.raquette_b.y += RAQUETTE_VITESSE

    def move_balle(self):
        self.balle.x += self.balle_vitesse_x
        self.balle.y += self.balle_vitesse_y

        if self.balle.top <= 0 or self.balle.bottom >= HEIGHT:
            self.balle_vitesse_y *= -1
            self.pong_b.play()

        if self.balle.colliderect(self.raquette_a):
            self.balle.left = self.raquette_a.right
            self.balle_vitesse_x *= -1
            self.ping_a.play()

        if self.balle.colliderect(self.raquette_b):
            self.balle.right = self.raquette_b.left
            self.balle_vitesse_x *= -1
            self.ping_a.play()

        if self.balle.left <= 0:
            self.pingpong_c.play()
            self.score_b += 1
            self.reset_game()
            if self.score_b == WIN_SCORE:
                self.winner = "Joueur B"
                self.running = False  # Mise à jour de self.running

        if self.balle.right >= WIDTH:
            self.pingpong_c.play()
            self.score_a += 1
            self.reset_game()
            if self.score_a == WIN_SCORE:
                self.winner = "Joueur A"
                self.running = False  # Mise à jour de self.running

    def reset_game(self):
        self.balle, self.balle_vitesse_x, self.balle_vitesse_y, self.last_speedup = reset_balle()
        pygame.time.delay(700)

    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.raquette_a)
        pygame.draw.rect(self.screen, WHITE, self.raquette_b)
        pygame.draw.ellipse(self.screen, WHITE, self.balle)
        pygame.draw.aaline(self.screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        win = self.font.render("7 points pour gagner !", True, WHITE)
        text = self.font.render(f"A: {self.score_a}    B: {self.score_b}", True, WHITE)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 40))
        self.screen.blit(win, (WIDTH // 2 - win.get_width() // 2, 5))

        # Affichage du temps écoulé
        elapsed_time = format_time(pygame.time.get_ticks() - self.start_time)
        time_text = self.font.render(f"Temps écoulé: {elapsed_time}", True, WHITE)
        self.screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT - 40))

        if self.paused:
            pause_text = self.font.render("PAUSE - Appuyez sur ESPACE", True, WHITE)
            self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

        pygame.display.flip()

def show_winner(self):
    self.screen.fill(BLACK)
    if self.winner:
        msg = f"{self.winner} gagne !"
    else:
        msg = "Fin du jeu"
    text = self.font.render(msg, True, WHITE)
    self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    return
