# game.py
import pygame
import sys
from constants import *
from sounds import init_sounds
from utils import reset_balle, format_time
from bonus import Bonus

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)

        self.raquette_a = pygame.Rect(30, HEIGHT//2 - RAQUETTE_HEIGHT//2, RAQUETTE_WIDTH, RAQUETTE_HEIGHT)
        self.raquette_b = pygame.Rect(WIDTH - 40, HEIGHT//2 - RAQUETTE_HEIGHT//2, RAQUETTE_WIDTH, RAQUETTE_HEIGHT)

        self.balle, self.balle_vitesse_x, self.balle_vitesse_y, self.last_speedup = reset_balle()

        self.score_a, self.score_b = 0, 0
        self.ping_a, self.pong_b, self.pingpong_c = init_sounds()
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
        self.raquette_a_speed = RAQUETTE_VITESSE
        self.raquette_b_speed = RAQUETTE_VITESSE
        self.original_raquette_height = RAQUETTE_HEIGHT

    def run(self):
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
        # Gestion du bonus
        if now - self.last_bonus_spawn > self.bonus_spawn_interval and not self.bonus.active:
            self.bonus.spawn()
            self.last_bonus_spawn = now
            
        effect = self.bonus.check_collision(self.raquette_a, "a") or self.bonus.check_collision(self.raquette_b, "b")
        if effect:
            self.active_effects[effect] = True
            player = effect[-1]
            for key in self.active_effects:
                if key.endswith(player) and key != effect:
                    self.active_effects[key] = False
            
        self.apply_bonus_effects()
        
        if now - self.last_speedup > SPEEDUP_INTERVAL:
            self.balle_vitesse_x = int(self.balle_vitesse_x * SPEEDUP_FACTOR)
            self.balle_vitesse_y = int(self.balle_vitesse_y * SPEEDUP_FACTOR)
            self.last_speedup = now

        self.clock.tick(FPS)
        self.move_raquettes()
        self.move_balle()

    def apply_bonus_effects(self):
        # Effet vitesse
        if self.active_effects["increase_speed_a"]:
            self.raquette_a_speed = RAQUETTE_VITESSE * 1.8
        else:
            self.raquette_a_speed = RAQUETTE_VITESSE
            
        if self.active_effects["increase_speed_b"]:
            self.raquette_b_speed = RAQUETTE_VITESSE * 1.8
        else:
            self.raquette_b_speed = RAQUETTE_VITESSE
            
        # Effet taille
        if self.active_effects["increase_size_a"]:
            self.raquette_a.height = self.original_raquette_height * 1.5
        else:
            self.raquette_a.height = self.original_raquette_height
            
        if self.active_effects["increase_size_b"]:
            self.raquette_b.height = self.original_raquette_height * 1.5
        else:
            self.raquette_b.height = self.original_raquette_height
            
        # Effet ralentissement
        if self.active_effects["slow_opponent_a"]:
            self.raquette_b_speed = RAQUETTE_VITESSE * 0.6
        elif not self.active_effects["increase_speed_b"]:
            self.raquette_b_speed = RAQUETTE_VITESSE
            
        if self.active_effects["slow_opponent_b"]:
            self.raquette_a_speed = RAQUETTE_VITESSE * 0.6
        elif not self.active_effects["increase_speed_a"]:
            self.raquette_a_speed = RAQUETTE_VITESSE

    def move_raquettes(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and self.raquette_a.top > 0:
            self.raquette_a.y -= self.raquette_a_speed
        if keys[pygame.K_s] and self.raquette_a.bottom < HEIGHT:
            self.raquette_a.y += self.raquette_a_speed
        if keys[pygame.K_UP] and self.raquette_b.top > 0:
            self.raquette_b.y -= self.raquette_b_speed
        if keys[pygame.K_DOWN] and self.raquette_b.bottom < HEIGHT:
            self.raquette_b.y += self.raquette_b_speed

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
                self.running = False

        if self.balle.right >= WIDTH:
            self.pingpong_c.play()
            self.score_a += 1
            self.reset_game()
            if self.score_a == WIN_SCORE:
                self.winner = "Joueur A"
                self.running = False

    def reset_game(self):
        self.balle, self.balle_vitesse_x, self.balle_vitesse_y, self.last_speedup = reset_balle()
        pygame.time.delay(700)
        # Réinitialiser les effets de bonus
        for effect in self.active_effects:
            self.active_effects[effect] = False
        self.raquette_a.height = self.original_raquette_height
        self.raquette_b.height = self.original_raquette_height

    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.raquette_a)
        pygame.draw.rect(self.screen, WHITE, self.raquette_b)
        pygame.draw.ellipse(self.screen, WHITE, self.balle)
        pygame.draw.aaline(self.screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

        self.bonus.draw(self.screen)

        score_text = self.font.render(f"{self.score_a} - {self.score_b}", True, WHITE)
        self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

        elapsed_time = format_time(pygame.time.get_ticks() - self.start_time)
        time_text = self.font.render(f"Time: {elapsed_time}", True, WHITE)
        self.screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, HEIGHT - 40))

        if self.paused:
            pause_text = self.font.render("PAUSE (SPACE)", True, WHITE)
            self.screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2))

        pygame.display.flip()

    def show_winner(self):
        self.screen.fill(BLACK)
        if self.winner:
            msg = f"{self.winner} WINS!"
        else:
            msg = "GAME OVER"
        text = self.font.render(msg, True, WHITE)
        self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(3000)