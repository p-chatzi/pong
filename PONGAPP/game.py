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
RAQUETTE_VITESSE = 15

# Balle
BALLE_SIZE = 15
balle = pygame.Rect(WIDTH//2 - BALLE_SIZE//2, HEIGHT//2 - BALLE_SIZE//2, BALLE_SIZE, BALLE_SIZE)
BALLE_VITESSE_INIT_X = 5
BALLE_VITESSE_INIT_Y = 5
balle_vitesse_x = BALLE_VITESSE_INIT_X
balle_vitesse_y = BALLE_VITESSE_INIT_Y

# Scores
score_a, score_b = 0, 0
font = pygame.font.SysFont("Arial", 30)
WIN_SCORE = 7

# Son
pygame.mixer.init()
ping_a= pygame.mixer.Sound('4359__noisecollector__pongblipf4.wav')
pong_b= pygame.mixer.Sound('4388__noisecollector__pongblipe5.wav')
pingpong_c = pygame.mixer.Sound('475557__rannem__bip.wav')

# Augmentation de la vitesse en fonction du temps
SPEEDUP_INTERVAL = 10000 # 10 secondes
last_speedup = pygame.time.get_ticks()
SPEEDUP_FACTOR = 1.5  # facteur acceleration

def reset_balle():
    global balle_vitesse_x, balle_vitesse_y, last_speedup
    balle.center = (WIDTH // 2, HEIGHT // 2)
    # On alterne la direction à chaque point
    balle_vitesse_x = -BALLE_VITESSE_INIT_X if balle_vitesse_x > 0 else BALLE_VITESSE_INIT_X
    balle_vitesse_y = BALLE_VITESSE_INIT_Y if balle_vitesse_y > 0 else -BALLE_VITESSE_INIT_Y
    last_speedup = pygame.time.get_ticks()

running = True
winner = None
paused = False

while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused  # Inverse l'état pause

    if not paused:

        if now - last_speedup > SPEEDUP_INTERVAL:
            # On augmente la vitesse (en gardant le signe)
            if balle_vitesse_x > 0:
                balle_vitesse_x = int(balle_vitesse_x * SPEEDUP_FACTOR)
            else:
                balle_vitesse_x = int(balle_vitesse_x * SPEEDUP_FACTOR)
            if balle_vitesse_y > 0:
                balle_vitesse_y = int(balle_vitesse_y * SPEEDUP_FACTOR)
            else:
                balle_vitesse_y = int(balle_vitesse_y * SPEEDUP_FACTOR)
            last_speedup = now

        clock.tick(FPS)

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

        # Mouvement de la ballee
        balle.x += balle_vitesse_x
        balle.y += balle_vitesse_y

        # Collision avec le haut/bas
        if balle.top <= 0 or balle.bottom >= HEIGHT:
            balle_vitesse_y *= -1
            pong_b.play()

        # Collision raquettes
        if balle.colliderect(raquette_a):
            balle.left = raquette_a.right
            balle_vitesse_x *= -1
            ping_a.play()

        if balle.colliderect(raquette_b):
            balle.right = raquette_b.left
            balle_vitesse_x *= -1
            ping_a.play()

        # Balle à gauche : point pour B
        if balle.left <= 0:
            pingpong_c.play()
            score_b += 1
            reset_balle()
            pygame.time.delay(700)
            if score_b == WIN_SCORE:
                winner = "Joueur B"
                running = False

        # Balle à droite : point pour A
        if balle.right >= WIDTH:
            pingpong_c.play()
            score_a += 1
            reset_balle()
            pygame.time.delay(700)
            if score_a == WIN_SCORE:
                winner = "Joueur A"
                running = False


    # Affichage
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, raquette_a)
    pygame.draw.rect(screen, WHITE, raquette_b)
    pygame.draw.ellipse(screen, WHITE, balle)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    win = font.render("7 points pour gagner !", True, WHITE)
    text = font.render(f"A: {score_a}    B: {score_b}", True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 40))
    screen.blit(win, (WIDTH // 2 - win.get_width() // 2, 5))

    if paused:
        pause_text = font.render("PAUSE - Appuyez sur ESPACE", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

    pygame.display.flip()

# Affichage du gagnant
screen.fill(BLACK)
if winner:
    msg = f"{winner} gagne !"
else:
    msg = "Fin du jeu"
text = font.render(msg, True, WHITE)
win = font.render(msg, True, WHITE)
screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
screen.blit(win, (WIDTH//2 - win.get_width()//2, HEIGHT//2 - win.get_height()//2))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
