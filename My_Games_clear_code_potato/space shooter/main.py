import pygame, sys
from random import randint as rd
from random import uniform as uf
from numpy.random import choice

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, surface): # Dodaje do grupy przy inicjalizacji obiektu
        super().__init__(groups) # Dziedziczność grupowania???
        self.image = surface
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()    
        self.speed = 350

        # Cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        
        # Maskowanie - niepotrzebne gdy do kolizji dajemy już maskowanie
        # self.mask = pygame.mask.from_surface(self.image)
  
    def laser_timer(self): # Tworzy timer by strzelać co ileś sekundy
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            # Kiedy różnica czasu strzału jest większa niż cooldown
            # pozwala na strzał
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
  
    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt # Przesuwa środek o wektor

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            # Kładzie laser na czubku statku, wystarczy 1 instancja strzału
            # potem ogarnia cooldown
            Laser((all_sprites, laser_sprites), laser_surf, self.rect.midtop)
            laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks() # Czas strzału
        
        self.laser_timer() # Odpala timer strzelania
        
        
class Star(pygame.sprite.Sprite):
    speed = 100
    def __init__(self, groups, surface):
        super().__init__(groups)
        self.image = surface # Pojedynczy import surface, niepotrzebnie wiele razy
        self.rect = self.image.get_frect(center = (rd(0,WINDOW_WIDTH), rd(0,WINDOW_HEIGHT)))
        self.speed = Star.speed
        
    def update(self, dt):
        self.rect.y += self.speed * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
        

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surface, position):
        super().__init__(groups)
        self.image = surface
        # Pozycjonujemy laser względem statku
        self.rect = self.image.get_frect(midbottom = position)

    def update(self, dt):
        # Zapewnia ruch lasera zgodnie ze statkiem (dt)
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0: # Laser powyżej okna usuwany
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, groups, frames, position):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = position)
        explosion_sound.play()
        
    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else: # Rozwala explosion gdy przekroczy wszystkie klatki
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surface, position):
        super().__init__(groups)
        self.original_surf = surface
        self.image = surface
        self.rect = self.image.get_rect(center = position)
        self.direction = pygame.Vector2(uf(-0.5,0.5), 1)
        self.speed = rd(400,500)
        
        # Transform
        self.rotation = 0
        self.rotation_speed = rd(50, 80) * choice([-1,1])
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt # Porusza meteorytem w dół
        if self.rect.top > WINDOW_HEIGHT: # Kasuje meteoryt gdy poniżej okna
            self.kill()
            
        # Ciągła rotacja - ze sprytem
        self.rotation += self.rotation_speed * dt # Trzeba zachować klatki
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_rect(center = self.rect.center)

            
def collisions():
    """Kolizje - można kolidować z wieloma grupami 
    w sprites tutaj za pomocą maski - od razu ją tworzy
    ale jest to bardzo wyżerające zasoby komputera
    Sprawdzam kolizję każdego lasera z meteorytem i usuwam oba"""
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        pygame.quit()
        sys.exit()

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            Explosion(all_sprites, explosion_frames, laser.rect.midtop)
            
def display_score():
    """Wyświetla wynik w postaci czasu"""
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (240,240,240)) # Tworzy surface i antiallising
    text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2,WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    
    # Rysowanko - początek/koniec/grubość
    # Prostokąt - granica/zaokrąglenie
    pygame.draw.rect(display_surface, (240,240,240), text_rect.inflate(20,10).move(0,-5), 5, 10)   
            
    
# =============================================================================
#     Główne ustawienia
# =============================================================================
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space shooter!')
clock = pygame.time.Clock() # Zegar


# =============================================================================
#     Import
# =============================================================================
meteor_surf = pygame.image.load('images/meteor.png').convert_alpha()
star_surf = pygame.image.load('images/star.png').convert_alpha()
laser_surf = pygame.image.load('images/laser.png').convert_alpha()
player_surf = pygame.image.load('images/player.png').convert_alpha()
explosion_frames = [pygame.image.load(f'images/explosion/{i}.png').convert_alpha() for i in range(21)] # Ilość klatek

font = pygame.font.Font("images/Oxanium-bold.ttf", 40)


# =============================================================================
#     Dźwięki
# =============================================================================
laser_sound = pygame.mixer.Sound('audio/laser.wav')
explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
game_music = pygame.mixer.Sound('audio/game_music.wav')
# damage_sound = pygame.mixer.Sound('audio/damage.ogg')

laser_sound.set_volume(0.01)
explosion_sound.set_volume(0.01)
game_music.set_volume(0.008)
game_music.play(loops= -1) # Nieskończoność
# damage_sound.set_volume(0.2)


# =============================================================================
#     Sprites - grupowanie
# =============================================================================
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
star_sprites = pygame.sprite.Group()
for i in range(20): # Tworzy tyle instancji gwiazd
    Star((all_sprites, star_sprites), star_surf)
    Star((all_sprites, star_sprites), star_surf).rect.centery -= WINDOW_HEIGHT # Bufor gwiazd powyżej

# Tworzy gracza jako obiekt
player = Player(all_sprites, player_surf)


# =============================================================================
#     Custom events/timers
# =============================================================================
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)
star_maker_event = pygame.event.custom_type()
pygame.time.set_timer(star_maker_event, # Szybkość timera zależy od szybkości spadania gwiazd
                      (WINDOW_HEIGHT * (5900 // 6) // Star.speed))
# 100 pikseli - 1 sekundę (59 klatek/60 klatek)
# 750 pikseli - x sekund - 1000x milisekund


while True:
    dt = clock.tick(59) / 1000 # Pomiar czasu [s] do wytworzenia 1 klatki czas/liczbę klatek
# =============================================================================
#     Event
# =============================================================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and 
                                         event.key == pygame.K_ESCAPE): # Wyłącza grę przy kliknięciu X
            pygame.quit()
            sys.exit()
        elif event.type == meteor_event:
            # Ustawia meteoryty i wywołuje je
            x, y = rd(0, WINDOW_WIDTH), rd(-200, -100)
            Meteor((all_sprites, meteor_sprites), meteor_surf, (x,y))
            # all_sprites - update i wyświetlanie
            # meteor_sprites - klasyfikacja wszystkich meteorytów
        if event.type == star_maker_event: # Tworzy gwiazdy powyżej okna co timer sekund
            for i in range(20):
                Star((all_sprites, star_sprites), star_surf).rect.centery -= WINDOW_HEIGHT
                

# =============================================================================
#     Gra
# =============================================================================
    display_surface.fill('#3a2e3f') # Kolor tła 
    
    # Przekazuje wszystkie argumenty metody update i wywołuje ją
    all_sprites.update(dt) # Przekazuje dt lokalnym scope
    display_score()
    all_sprites.draw(display_surface)
    collisions()
    pygame.display.update() # Wyświetlacz