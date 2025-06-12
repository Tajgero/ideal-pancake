import pygame
from os.path import join 
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collisions): # Dodaje do grupy przy inicjalizacji obiektu
        super().__init__(groups) # Dziedziczność grupowania???
        self.frames() # Uruchamia ładowanie frames postaci
        self.state, self.frame_index = 'down', 0
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        
        # Hitbox - po lewej i prawej w grafice player są puste przestrzenie 
        self.hitbot_rect = self.rect.inflate(-60, -90) # Zmniejszam hitbox o 40 z każdej
        
        # Ruch
        self.vector = pygame.Vector2()
        self.speed = 450
        self.collisions = collisions # Można zachować logikę kolizji
    
    def frames(self):
        '''Wyciąga każdą klatkę dla danego ruchu do słownika frames'''
        self.frames = {'left':[], 'right':[], 'up':[], 'down':[]}
        
        for state in self.frames.keys(): # np. 'left' to inaczej state
            # tuple: (string: 'Lokalizacja', np. 'images\\player'
            # list: [string: 'subfoldery'], np. ['down', 'left', 'right', 'up']
            # list: [string: 'nazwy plików']) np. ['0.png', '1.png', '2.png', '3.png']
            for path, folders, files in walk(join('images', 'player', state)):
                if files: # Interesują nas tylko same pliki
                    for file in sorted(files, key=lambda name: int(name.split('.')[0])): # Wyciągam dla każdego plik z plików
                        # np. 0.png jest splitowane na podstawie '.'
                        # ['0', 'png'] i wyciągamy 1 element '0'
                        # i sortowaniu podlega ten właśnie element w funkcji int()
                        # Ścieżka + plik np. images\player\down\0.png 
                        full_path = join(path, file)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf) # Dołączamy do listy dla klucza surf                
    
    def input(self):
        keys = pygame.key.get_pressed()
        # Tworzenie wektorów jednostkowych, normalizacja i ustalenie prędkości
        self.vector.x = int(keys[pygame.K_RIGHT]) or keys[pygame.K_d] - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.vector.y = int(keys[pygame.K_DOWN]) or keys[pygame.K_s] - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.vector = self.vector.normalize() if self.vector else self.vector
        
    def move(self, dt):
        self.hitbot_rect.x += self.vector.x * self.speed * dt # Przesuwa lewo o wektor
        self.collision('horizontal')
        self.hitbot_rect.y += self.vector.y * self.speed * dt # Przesuwa górę o wektor
        self.collision('vertical')
        self.rect.center = self.hitbot_rect.center # Ustawia naszego gracza tam gdzie hitbox
        
    def collision(self, direction):
        # Trzeba wszystkie obstacle wziąć
        for sprite in self.collisions:
            if sprite.rect.colliderect(self.hitbot_rect): # Jeśli zajdzie overlap
                if direction == 'horizontal':
                    if self.vector.x > 0: # Zderzenie z lewej obiektu
                        # Prawą część player przenosimy na lewą część obiektu
                        self.hitbot_rect.right = sprite.rect.left
                    if self.vector.x < 0: # Zderzenie z prawej obiektu
                        self.hitbot_rect.left = sprite.rect.right
                else:
                    if self.vector.y > 0: # Zderzenie z góry obiektu
                        self.hitbot_rect.bottom = sprite.rect.top
                    if self.vector.y < 0: # Zderzenie z dołu obiektu
                        self.hitbot_rect.top = sprite.rect.bottom
        
    def animate(self, dt):
        # Poznanie state animacji
        if self.vector.x != 0: # Przy ruchu x
            if self.vector.x > 0:
                self.state = 'right'
            else:
                self.state = 'left'
                
        elif self.vector.y != 0: # Przy ruchu y
            if self.vector.y > 0:
                self.state = 'down'
            else:
                self.state = 'up'
                
        # Animacja - wyciągamy ze słownika state i dostajemy listę klatek
        # z listy wyciągam daną klatkę zgodnie z frame_index
        # % modulo powoduje powtórzenie procesu
        if self.vector:
            self.frame_index += 5 * dt # Czas animacji
        else:
            self.frame_index = 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        