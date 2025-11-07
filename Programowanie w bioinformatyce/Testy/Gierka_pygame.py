# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 19:15:37 2024

@author: Tajgero
"""
import pygame, sys, math

pygame.init()

# Parametry okna
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GPT gra")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Gracz
player_width, player_height = 50, 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT // 2 - player_height // 2
player_speed = 5

# Przeszkoda - koło
obstacle_radius = 30
obstacle_x, obstacle_y = 150, HEIGHT // 2 # 150 pikseli od lewej krawędzi ekranu i w jej połowie

# Oblicz odległość pomiędzy środkiem prostokąta a środkiem koła
def distance(player_x, player_y, obstacle_x, obstacle_y):
    center_x = player_x + player_width // 2
    center_y = player_y + player_height // 2
    return math.sqrt((center_x - obstacle_x) ** 2 + (center_y - obstacle_y) ** 2)

# Główna pętla gry
running = True
while running:
    # Ustawienia prędkości gry FPS
    clock = pygame.time.Clock().tick(60)
    
    # Obsługa zdarzeń (klawisze, zamknięcie okna)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    # Pobieranie stanu klawiszy
    keys = pygame.key.get_pressed()

    # Ruch prostokąta
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT]:
        player_x += player_speed
    elif keys[pygame.K_UP]:
        player_y -= player_speed
    elif keys[pygame.K_DOWN]:
        player_y += player_speed

    # Ograniczenie ruchu prostokąta do boków ekranu
    if player_x < 0:
        player_x = 0
    elif player_x + player_width > WIDTH:
        player_x = WIDTH - player_width
    elif player_y < 0:
        player_y = 0
    elif player_y + player_height > HEIGHT:
        player_y = HEIGHT - player_height

        # Ograniczenie ruchu, aby prostokąt nie mógł wejść w koło
    if distance(player_x, player_y, obstacle_x, obstacle_y) < obstacle_radius + player_width // 2:
        
        if keys[pygame.K_LEFT]:
            player_x += player_speed
        elif keys[pygame.K_RIGHT]:
            player_x -= player_speed
        elif keys[pygame.K_UP]:
            player_y += player_speed
        elif keys[pygame.K_DOWN]:
            player_y -= player_speed        

    # Rysowanie tła, gracza i przeszkody
    screen.fill(WHITE)

    # Rysowanie gracza - prostokąt
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    # Rysowanie przeszkody - koło
    pygame.draw.circle(screen, RED, (obstacle_x, obstacle_y), obstacle_radius)

    # Aktualizacja okna gry
    pygame.display.flip()
    
pygame.quit()