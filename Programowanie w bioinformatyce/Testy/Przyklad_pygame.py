# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 16:51:38 2024

@author: tygrys012
"""
import pygame

# Ustawienia
pygame.init()

screen_width = 200
screen_height = 100
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Liczba kroków")
zegar = pygame.time.Clock()
running = True

# Parametry obiektu
rect_x = 50
rect_y = 50
rect_width = 50
rect_height = 50
rect_speed_x = 5
rect_speed_y = 5

while running:
    # Gra
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('white') # Kolor okna
    
    # RENDER GRY
    
    # Ruch obiektu
    rect_x += rect_speed_x
    rect_y += rect_speed_y

    # Zmiana kierunku, jeśli obiekt uderzy w krawędź ekranu
    if rect_x + rect_width > screen_width or rect_x < 0:
        rect_speed_x = -rect_speed_x
    if rect_y + rect_height > screen_height or rect_y < 0:
        rect_speed_y = -rect_speed_y

    pygame.draw.rect(screen, 'black', [rect_x, rect_y, rect_width, rect_height])

    # Aktualizacja ekranu
    pygame.display.update()

    zegar.tick(60)  # limit FPS do 60

# Zakończenie działania Pygame
pygame.quit()