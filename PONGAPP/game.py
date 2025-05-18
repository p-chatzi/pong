"""
Classe PongGame pour gérer le jeu Pong avec bonus, scores et effets visuels/sonores.
"""


import sys
import pygame
from constants import (
    WIDTH, HEIGHT, WHITE, BLACK, FPS, PADDLE_WIDTH, PADDLE_SPEED,
    FONT_SIZE, TIME_Y_OFFSET, WIN_SCORE, SPEEDUP_INTERVAL,
    SPEEDUP_FACTOR, BONUS_SPAWN_INTERVAL, SPEED_BOOST, SPEED_SLOW,
    PADDEL_MARGIN_X, PADDLE_HEIGHT
)
import settings
from sounds import init_sounds
from utils import reset_ball, format_time
from bonus import Bonus


class PongGame:
    """
    Classe PongGame représentant le jeu Pong.

    Attributs :
    - screen : Surface de l'écran de jeu.
    - clock : Horloge pour gérer le temps.
    - font : Police utilisée pour afficher le text.
    - paddle_a, paddle_b : Rectangles représentant les paddles des joueurs.
    - ball : Rectangle représentant la ball.
    - ball_speed_x, ball_speed_y : Vitesse de la ball en x et y.
    - score_a, score_b : Scores des joueurs A et B.
    - ping_a, pong_b, ping_pong_c : Sons du jeu.
    - winner : Gagnant de la partie.
    - paused : Indique si le jeu est en pause.
    - start_time : Temps de début de la partie.
    - running : Indique si le jeu est en cours.
    - bonus : Instance du système de bonus.
    - last_bonus_spawn : Temps du dernier spawn de bonus.
    - bonus_spawn_interval : Intervalle entre les spawns de bonus.
    - active_effects : Effets actifs des bonus.
    - paddle_a_speed, paddle_b_speed : Vitesse des paddles.
    - original_paddle_height : height originale des paddles.

    Méthodes :
    - run() : Boucle principale du jeu.
    - update(now) : Met à jour l'état du jeu.
    - apply_bonus_effects() : Applique les effets des bonus.
    - move_paddles() : Gère le déplacement des paddles.
    - move_ball() : Gère le déplacement de la ball.
    - reset_game() : Réinitialise le jeu après un point.
    - draw() : Dessine les éléments du jeu à l'écran.
    - show_winner() : Affiche le gagnant à la fin de la partie.
    """
    def __init__(self, paddle_height, label, width, height):
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)

        self.paddle_a = pygame.Rect(PADDEL_MARGIN_X,
                                    height//2 - paddle_height//2,
                                    PADDLE_WIDTH,
                                    paddle_height)
        self.paddle_b = pygame.Rect(width - PADDEL_MARGIN_X - PADDLE_WIDTH,
                                    height//2 - paddle_height//2,
                                    PADDLE_WIDTH,
                                    paddle_height)

        self.ball, self.ball_speed_x, self.ball_speed_y, self.last_speedup = reset_ball(width, height)

        self.score_a, self.score_b = 0, 0
        self.ping_a, self.pong_b, self.ping_pong_c = init_sounds()
        self.winner = None
        self.paused = False
        self.start_time = pygame.time.get_ticks()
        self.running = True

        # Système de bonus
        self.bonus = Bonus()
        self.last_bonus_spawn = pygame.time.get_ticks()
        self.bonus_spawn_interval = BONUS_SPAWN_INTERVAL
        self.active_effects = {
            "increase_speed_a": False,
            "increase_size_a": False,
            "slow_opponent_a": False,
            "increase_speed_b": False,
            "increase_size_b": False,
            "slow_opponent_b": False
        }
        self.paddle_a_speed = self.paddle_b_speed = PADDLE_SPEED
        self.original_paddle_height = PADDLE_HEIGHT


    def run(self):
        """
        Exécute la boucle principale du jeu, gère les événements, met à jour l'état du jeu 
        et affiche les éléments graphiques. Permet de mettre le jeu en pause avec la barre d'espace.
        """
        while self.running:
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
                self.bonus.update()  # Mettre à jour l'état du bonus

            self.draw()
        self.show_winner()


    def update(self, now):
        """
        Met à jour l'état du jeu.
        Args:
            now (int): Temps actuel en millisecondes.
        Fonctionnalités :
        - Gère l'apparition et les effets des bonus.
        - Applique les effets actifs des bonus.
        - Augmente progressivement la speed de la ball.
        - Met à jour les positions des paddles et de la ball.
        """
        # Gestion du bonus
        if now - self.last_bonus_spawn > self.bonus_spawn_interval and not self.bonus.active:
            self.bonus.spawn()
            self.last_bonus_spawn = now

        effect = (self.bonus.check_collision(self.paddle_a, "a")
                or self.bonus.check_collision(self.paddle_b, "b"))
        if effect:
            self.active_effects[effect] = True
            player = effect[-1]
            for key in self.active_effects:
                if key.endswith(player) and key != effect:
                    self.active_effects[key] = False

        self.apply_bonus_effects()

        if now - self.last_speedup > SPEEDUP_INTERVAL:
            self.ball_speed_x = int(self.ball_speed_x * SPEEDUP_FACTOR)
            self.ball_speed_y = int(self.ball_speed_y * SPEEDUP_FACTOR)
            self.last_speedup = now

        self.clock.tick(FPS)
        self.move_paddles()
        self.move_ball()


    def apply_bonus_effects(self):
        """
        Applique les effets bonus actifs sur les paddles :
        - Augmente ou réduit la speed des paddles.
        - Modifie la taille des paddles.
        - Ralentit l'adversaire si applicable.
        """
        # Effet speed
        if self.active_effects["increase_speed_a"]:
            self.paddle_a_speed = PADDLE_SPEED * SPEED_BOOST
        else:
            self.paddle_a_speed = PADDLE_SPEED
            
        if self.active_effects["increase_speed_b"]:
            self.paddle_b_speed = PADDLE_SPEED * SPEED_BOOST
        else:
            self.paddle_b_speed = PADDLE_SPEED
            
        # Effet taille
        # if self.active_effects["increase_size_a"]:
        #     self.paddle_a.height = self.original_paddle_height * SIZE_BOOST
        # else:
        #     self.paddle_a.height = self.original_paddle_height
            
        # if self.active_effects["increase_size_b"]:
        #     self.paddle_b.height = self.original_paddle_height * SIZE_BOOST
        # else:
        #     self.paddle_b.height = self.original_paddle_height
            
        # Effet ralentissement
        if self.active_effects["slow_opponent_a"]:
            self.paddle_b_speed = PADDLE_SPEED * SPEED_SLOW
        elif not self.active_effects["increase_speed_b"]:
            self.paddle_b_speed = PADDLE_SPEED
            
        if self.active_effects["slow_opponent_b"]:
            self.paddle_a_speed = PADDLE_SPEED * SPEED_SLOW
        elif not self.active_effects["increase_speed_a"]:
            self.paddle_a_speed = PADDLE_SPEED


    def move_paddles(self):
        """
        Déplace les paddles en fonction des touches pressées.
        - 'Z' et 'S' pour la paddle A (haut et bas).
        - Flèches 'Haut' et 'Bas' pour la paddle B.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and self.paddle_a.top > 0:
            self.paddle_a.y -= self.paddle_a_speed
        if keys[pygame.K_s] and self.paddle_a.bottom < self.height - 1:
            self.paddle_a.y += self.paddle_a_speed
        if keys[pygame.K_UP] and self.paddle_b.top > 0:
            self.paddle_b.y -= self.paddle_b_speed
        if keys[pygame.K_DOWN] and self.paddle_b.bottom < self.height - 1:
            self.paddle_b.y += self.paddle_b_speed


    def move_ball(self):
        """
        Déplace la ball et gère les collisions (murs, paddles).
        Met à jour les scores et détermine le gagnant si le score limite est atteint.
        """
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        if self.ball.top <= 0 or self.ball.bottom >= self.height - 1:
            self.ball_speed_y *= -1
            self.pong_b.play()

        if self.ball.colliderect(self.paddle_a):
            self.ball.left = self.paddle_a.right
            self.ball_speed_x *= -1
            self.ping_a.play()

        if self.ball.colliderect(self.paddle_b):
            self.ball.right = self.paddle_b.left
            self.ball_speed_x *= -1
            self.ping_a.play()

        if self.ball.left <= 0:
            self.ping_pong_c.play()
            self.score_b += 1
            self.reset_game()
            if self.score_b == WIN_SCORE:
                self.winner = "Joueur B"
                self.running = False

        if self.ball.right >= self.width:
            self.ping_pong_c.play()
            self.score_a += 1
            self.reset_game()
            if self.score_a == WIN_SCORE:
                self.winner = "Joueur A"
                self.running = False


    def reset_game(self):
        """
        Réinitialise le jeu en rétablissant la position de la ball, 
        sa speed, les effets actifs et la taille des paddles.
        """
        self.ball, self.ball_speed_x, self.ball_speed_y, self.last_speedup = reset_ball(self.width, self.height)
        pygame.time.delay(700)
        # Réinitialiser les effets de bonus
        for effect in self.active_effects:
            self.active_effects[effect] = False
        self.paddle_a.height = settings.get_current_paddle_height()
        self.paddle_b.height = settings.get_current_paddle_height()

    def draw(self):
        """
        Dessine les éléments du jeu sur l'écran.

        - Remplit l'écran avec une couleur de fond.
        - Dessine les paddles, la ball, et une ligne centrale.
        - Affiche le score et le temps écoulé.
        - Affiche un message de pause si le jeu est en pause.
        - Met à jour l'affichage de l'écran.
        """
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.paddle_a)
        pygame.draw.rect(self.screen, WHITE, self.paddle_b)
        pygame.draw.ellipse(self.screen, WHITE, self.ball)
        pygame.draw.aaline(self.screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        self.bonus.draw(self.screen)

        score_text = self.font.render(f"{self.score_a} - {self.score_b}", True, WHITE)
        self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, 20))

        elapsed_time = format_time(pygame.time.get_ticks() - self.start_time)
        time_text = self.font.render(f"Time: {elapsed_time}", True, WHITE)
        time_y = self.height - int(self.height * TIME_Y_OFFSET)
        self.screen.blit(time_text, (self.width//2 - time_text.get_width()//2, time_y))

        if self.paused:
            pause_text = self.font.render("PAUSE (SPACE)", True, WHITE)
            self.screen.blit(pause_text, (self.width//2 - pause_text.get_width()//2, self.height//2))

        pygame.display.flip()


    def show_winner(self):
        """
        Affiche l'écran de fin avec le message du gagnant ou un message de fin de partie.
        Remplit l'écran en noir, affiche le text centré, et attend 3 secondes avant de continuer.
        """
        self.screen.fill(BLACK)
        if self.winner:
            msg = f"{self.winner} GAGNE !"
        else:
            msg = "FIN DE LA PARTIE !"
        text = self.font.render(msg, True, WHITE)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(3000)
