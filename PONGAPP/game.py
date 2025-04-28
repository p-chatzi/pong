import pygame
import sys

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Raquettes
RAQUETTE_WIDTH, RAQUETTE_HEIGHT = 10, 100
raquette_a = pygame.Rect(30, HEIGHT//2 - RAQUETTE_HEIGHT//2, RAQUETTE_WIDTH, RAQUETTE_HEIGHT)
raquette_b = pygame.Rect(WIDTH-40, HEIGHT//2 - RAQUETTE_HEIGHT//2, RAQUETTE_WIDTH, RAQUETTE_HEIGHT)
RAQUETTE_VITESSE = 7

# Balle
BALLE_SIZE = 15
balle = pygame.Rect(WIDTH//2 - BALLE_SIZE//2, HEIGHT//2 - BALLE_SIZE//2, BALLE_SIZE, BALLE_SIZE)
balle_vitesse_x = 5
balle_vitesse_y = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mouvements des raquettes
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z] and raquette_a.top > 0:
        raquette_a.y -= RAQUETTE_VITESSE
    if keys[pygame.K_s] and raquette_a.bottom < HEIGHT:
        raquette_a.y += RAQUETTE_VITESSE
    if keys[pygame.K_UP] and raquette_b.top > 0:
        raquette_b.y -= RAQUETTE_VITESSE
    if keys[pygame.K_DOWN] and raquette_b.bottom < HEIGHT:
        raquette_b.y += RAQUETTE_VITESSE

    # Mouvement de la balle
    balle.x += balle_vitesse_x
    balle.y += balle_vitesse_y

    # Collision avec le haut/bas
    if balle.top <= 0 or balle.bottom >= HEIGHT:
        balle_vitesse_y *= -1

    # Collision raquettes
    if balle.colliderect(raquette_a):
        balle.left = raquette_a.right
        balle_vitesse_x *= -1
    if balle.colliderect(raquette_b):
        balle.right = raquette_b.left
        balle_vitesse_x *= -1

    # Réinitialisation si la balle sort
    if balle.left <= 0 or balle.right >= WIDTH:
        balle.center = (WIDTH // 2, HEIGHT // 2)
        balle_vitesse_x = 5 * (-1 if balle_vitesse_x > 0 else 1)
        balle_vitesse_y = 5 * (-1 if balle_vitesse_y > 0 else 1)

    # Affichage
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, raquette_a)
    pygame.draw.rect(screen, WHITE, raquette_b)
    pygame.draw.ellipse(screen, WHITE, balle)
    pygame.display.flip()
    clock.tick(FPS)
