# bonus.py
import pygame
import random
from constants import WIDTH, HEIGHT, WHITE, BLACK, RAQUETTE_HEIGHT, BONUS_RADIUS, BONUS_DURATION, BONUS_BLINK_INTERVAL
from utils import format_time

class Bonus:
    def __init__(self):
        self.radius = BONUS_RADIUS
        self.active = False
        self.type = None
        self.rect = pygame.Rect(0, 0, self.radius*2, self.radius*2)
        self.spawn_time = 0
        self.collected_time = 0
        self.duration = BONUS_DURATION
        self.color = WHITE
        self.types = [
            {"name": "SPEED+", "color": (0, 255, 0), "effect": "increase_speed"},
            {"name": "SIZE+", "color": (255, 255, 0), "effect": "increase_size"},
            {"name": "SLOW", "color": (255, 0, 0), "effect": "slow_opponent"}
        ]
        self.blink_timer = 0
        self.visible = True

    def spawn(self):
        if not self.active:
            self.type = random.choice(self.types)
            self.color = self.type["color"]
            spawn_side = random.choice(["left", "right"])
            
            if spawn_side == "left":
                self.rect.x = random.randint(50, WIDTH//3)
            else:
                self.rect.x = random.randint(WIDTH*2//3, WIDTH - 50)
            
            self.rect.y = random.randint(RAQUETTE_HEIGHT, HEIGHT - RAQUETTE_HEIGHT)
            self.active = True
            self.spawn_time = pygame.time.get_ticks()
            self.blink_timer = 0
            self.visible = True

    def update(self):
        # Faire disparaître le bonus après 10 secondes
        if self.active and pygame.time.get_ticks() - self.spawn_time > self.duration:
            self.active = False

    def draw(self, screen):
        if self.active:
            # Clignotement
            self.blink_timer += 1
            if self.blink_timer % BONUS_BLINK_INTERVAL == 0:
                self.visible = not self.visible
                
            if self.visible:
                pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
                pygame.draw.circle(screen, WHITE, self.rect.center, self.radius + 2, 2)
                
                # Afficher le type et temps restant
                remaining_time = max(0, (self.duration - (pygame.time.get_ticks() - self.spawn_time))) // 1000
                font = pygame.font.SysFont("Arial", 20)
                text = font.render(f"{self.type['name']} {remaining_time}s", True, BLACK)
                screen.blit(text, (self.rect.centerx - text.get_width()//2, 
                                 self.rect.centery - text.get_height()//2))

        # Afficher le temps restant pour les bonus actifs
        if self.collected_time > 0:
            remaining_time = max(0, self.duration - (pygame.time.get_ticks() - self.collected_time))
            if remaining_time > 0:
                time_text = f"BONUS: {self.type['name']} ({remaining_time//1000}s)"
                font = pygame.font.SysFont("Arial", 24)
                text_surface = font.render(time_text, True, self.color)
                y_pos = 10 if self.type['effect'].endswith('a') else 30
                screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, y_pos))

    def check_collision(self, rect, player):
        if self.active and self.rect.colliderect(rect):
            self.active = False
            self.collected_time = pygame.time.get_ticks()
            return self.type['effect'] + player
        return None

    def is_active(self):
        return pygame.time.get_ticks() - self.collected_time < self.duration if self.collected_time > 0 else False