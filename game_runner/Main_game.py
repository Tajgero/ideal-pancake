import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound_value = 0.03
        self.jump_sound.set_volume(self.jump_sound_value)
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.jump_sound_switch

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
            
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.x < -100:
            self.kill() # Usuwa klasę Obstacle

def display_score():
    zegar = pygame.time.get_ticks() - start_time
    zegar = int(zegar / 100)
    score_surf = my_font.render(f'Score: {zegar}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (width/2,50))
    screen.blit(score_surf,score_rect)
    return zegar

def collision_sprite():
    # Bool określa usunięcie grupy lub nie    
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False): # Returnuje listę    
        obstacle_group.empty()
        return False
    else: return True



pygame.init()
# =============================================================================
# Inicjalizacja
# =============================================================================
width, height = 800, 400

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
my_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music_value = 0.01
bg_music.set_volume(bg_music_value)
bg_music.play(loops = -1)

# Dodaje nową klasę do grupy sprite
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Surfaces tła
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# Intro screen
player_stand_surf = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf,0,2)
player_stand_rect = player_stand_surf.get_rect(center = (width/2,height - 195))

game_name_start_surf = my_font.render('You are playing Runner',False,(111,196,169))
game_name_start_rect = game_name_start_surf.get_rect(center = (width/2,50))

game_name_end_surf = my_font.render('Thanks for playing Runner',False,(111,196,169))
game_name_end_rect = game_name_end_surf.get_rect(center = (width/2,50))

game_message = my_font.render('Press space to play Runner',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (width/2,height - 40))


# Timers
obstacle_timer = pygame.USEREVENT + 1 # Avoid conflict with some built-in events or something
pygame.time.set_timer(obstacle_timer,1500)


# =============================================================================
# Event system
# =============================================================================
while True:
    for event in pygame.event.get():
        # Wyłącza grę po escape lub X
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        elif event.type == pygame.KEYDOWN: # Kliknięcia klawiszy
            if event.key == pygame.K_UP:
                bg_music_value += 0.01
                bg_music.set_volume(bg_music_value)
                if bg_music_value > 0.2:
                    bg_music_value = 0.2
                    
            elif event.key == pygame.K_DOWN:
                bg_music_value -= 0.01
                bg_music.set_volume(bg_music_value)
                if bg_music_value < 0:
                    bg_music_value = 0
                
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
                
        if game_active:            
            # Dodaje randomowy obstacle
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail']))) # 75% na ślimaka
                
        else:  
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()
# =============================================================================
# Aktywna gra
# =============================================================================
    if game_active:  
        # Tło
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))
        
        # Wyświetla scoring  
        score = display_score()
        
        # Wyświetla player
        player.draw(screen)
        player.update()
        
        # Wyświetla obiekty
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        # Sprawdza aktywność gry przy kolizji
        game_active = collision_sprite()
# =============================================================================
# Nieaktywna gra
# =============================================================================
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand_surf,player_stand_rect)
        
        bg_music_text = my_font.render(f'BG volume: {int(round(bg_music_value*500,2))}',False,(111,196,169))
        screen.blit(bg_music_text,(10, height // 2))
        
        score_message = my_font.render(f'Wynik: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (width // 2, height - 40))
        
        # Ustawianie wyniku
        if score == 0:
            screen.blit(game_name_start_surf,game_name_start_rect)
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(game_name_end_surf,game_name_end_rect)
            screen.blit(score_message,score_message_rect)      

        
    # Update ekranu w FPS
    pygame.display.update()
    clock.tick(59)