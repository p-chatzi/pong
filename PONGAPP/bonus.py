"""
Module bonus.py
Ce module gère les bonus dans le jeu Pong. Les bonus apparaissent aléatoirement, 
peuvent être collectés par les joueurs, et appliquent des effets temporaires.
Classes:
    - Bonus: Représente un bonus avec des propriétés, effets, et gestion de durée.
Constantes importées:
    - WHITE, BLACK: Couleurs.
    - PADDLE_HEIGHT: height des paddles.
    - BONUS_RADIUS: Rayon du bonus.
    - BONUS_DURATION: Durée d'un bonus actif.
    - BONUS_BLINK_INTERVAL: Intervalle de clignotement.
Fonctions utilitaires:
    - format_time: Formate le temps restant pour affichage.
"""

import random
import pygame
from constants import (
    WHITE, BLACK, GREEN, YELLOW, RED,
    PADDLE_HEIGHT, BONUS_RADIUS, BONUS_DURATION, BONUS_BLINK_INTERVAL,
    BONUS_LEFT_ZONE, BONUS_RIGHT_ZONE, BONUS_MARGIN_X,
    BONUS_INFO_Y_PLAYER1, BONUS_INFO_Y_PLAYER2,
    BONUS_FONT_SIZE, BONUS_INFO_FONT_SIZE
)


class Bonus:
    """
    Classe représentant un bonus dans le jeu Pong.

    Attributs :
        radius (int) : Rayon du bonus.
        active (bool) : Indique si le bonus est actif.
        type (dict) : Type de bonus (nom, couleur, effet).
        rect (pygame.Rect) : Rectangle englobant le bonus.
        spawn_time (int) : Temps d'apparition du bonus.
        collected_time (int) : Temps de collecte du bonus.
        duration (int) : Durée d'effet du bonus.
        color (tuple) : Couleur du bonus.
        types (list) : Liste des types de bonus disponibles.
        blink_timer (int) : Timer pour l'effet de clignotement.
        visible (bool) : Indique si le bonus est visible.

    Méthodes :
        spawn(screen) : Fait apparaître un bonus aléatoire sur le terrain.
        update() : Met à jour l'état du bonus (expiration).
        draw(screen) : Dessine le bonus et affiche ses infos.
        check_collision(rect, player) : Vérifie la collision avec un joueur.
        is_active() : Vérifie si le bonus est encore actif.
    """
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
            {"name": "FAST", "color": GREEN, "effect": "increase_speed"},
            {"name": "BIG", "color": YELLOW, "effect": "increase_size"},
            {"name": "SLOW", "color": RED, "effect": "slow_opponent"}
        ]
        self.blink_timer = 0
        self.visible = True


    def spawn(self, screen):
        """
        Fait apparaître un bonus sur l'écran. Définit son type, couleur, position aléatoire
        et initialise les attributs liés à son état (actif, temps d'apparition, visibilité).
        """
        if not self.active:
            self.type = random.choice(self.types)
            self.color = self.type["color"]
            spawn_side = random.choice(["left", "right"])

            if spawn_side == "left":
                self.rect.x = random.randint(BONUS_MARGIN_X, BONUS_LEFT_ZONE)
            else:
                self.rect.x = random.randint(BONUS_RIGHT_ZONE, screen.get_width() - BONUS_MARGIN_X)

            self.rect.y = random.randint(PADDLE_HEIGHT, screen.get_height() - PADDLE_HEIGHT)
            self.active = True
            self.spawn_time = pygame.time.get_ticks()
            self.blink_timer = 0
            self.visible = True


    def update(self):
        """
        Met à jour l'état du bonus. 
        Désactive le bonus si 10 secondes se sont écoulées depuis son apparition.
        """
        # Faire disparaître le bonus après 10 secondes
        if self.active and pygame.time.get_ticks() - self.spawn_time > self.duration:
            self.active = False


    def draw(self, screen):
        """
        Dessine le bonus sur l'écran s'il est actif et gère son clignotement.
        Args:
            screen (pygame.Surface): Surface sur laquelle dessiner le bonus.

        Affiche également le type et le temps restant du bonus, ainsi que le temps
        restant des bonus actifs.
        """
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
                font = pygame.font.SysFont("Arial", BONUS_FONT_SIZE)
                text = font.render(f"{self.type['name']} {remaining_time}s", True, BLACK)
                screen.blit(text, (self.rect.centerx - text.get_width()//2,
                self.rect.centery - text.get_height()//2))

        # Afficher le temps restant pour les bonus actifs
        if self.collected_time > 0:
            remaining_time = max(0, self.duration - (pygame.time.get_ticks() - self.collected_time))
            if remaining_time > 0:
                time_text = f"BONUS: {self.type['name']} ({remaining_time//1000}s)"
                font = pygame.font.SysFont("Arial", BONUS_INFO_FONT_SIZE)
                text_surface = font.render(time_text, True, self.color)
                y_pos = (
                    BONUS_INFO_Y_PLAYER1
                    if self.type['effect'].endswith('a')
                    else BONUS_INFO_Y_PLAYER2
                    )
                screen.blit(text_surface, (screen.get_width()//2 - text_surface.get_width()//2, y_pos))


    def check_collision(self, rect, player):
        """
        Vérifie la collision entre un rectangle et un joueur. Si actif et collision détectée, 
        désactive l'objet, enregistre le temps de collecte et retourne l'effet appliqué au joueur.
        
        Args:
            rect (pygame.Rect): Rectangle à tester pour la collision.
            player (int): Identifiant ou attribut du joueur.

        Returns:
            Optional[int]: Effet appliqué au joueur ou None si pas de collision.
        """
        if self.active and self.rect.colliderect(rect):
            self.active = False
            self.collected_time = pygame.time.get_ticks()
            return self.type['effect'] + player
        return None


    def is_active(self):
        """
        Détermine si le bonus est actif.

        Returns:
            True si le temps écoulé depuis la collecte est inférieur à la durée,
            sinon False.
        """
        return (
            pygame.time.get_ticks() - self.collected_time < self.duration
            if self.collected_time > 0
            else False)
