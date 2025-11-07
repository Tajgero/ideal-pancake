# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 17:08:27 2024

@author: tygrys012
"""
import pygame
from sys import exit

def start_licznik(liczenie,max_count):
    '''liczenie wewnątrz innej pętli'''
    # Inicjalizacja Pygame
    
    
    
    pygame.init()
    
    # Wymiary okna
    width = 250
    height = 100
    screen = pygame.display.set_mode((width, height))
    
    # Ustawienie tytułu okna
    pygame.display.set_caption("Licznik kroków")
    
    # Kontrola czasu
    zegar = pygame.time.Clock()
    
    # Kolory
    white = (255, 255, 255)
    black = (0, 0, 0)
    
    # Ustawienie czcionki
    font = pygame.font.SysFont(None, 40)
    
    # GŁÓWNA PĘTLA PROGRAMU
    while True:
        
        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
                
        screen.fill(white)    
        text = font.render(f'Kroki: {liczenie}', True, black)
        text_rect = text.get_rect(center=(width // 2,height // 2))
        
        screen.blit(text, text_rect)
    
        # Spowolnienie iteracji pętli dla czytelności
        # pygame.time.delay(50)  # 500 ms = 0.5 sekundy opóźnienia
        
        pygame.display.update()
        zegar.tick(59)