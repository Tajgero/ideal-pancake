import settings as st
import pygame, sys
from player import Player
from sprites import CollisionSprite, Sprite, Gun, Bullet, Enemies
from os.path import join 
from os import walk
from pytmx.util_pygame import load_pygame # Do importu map .tmx
from groups import AllSprites
from random import choice

class Game():
    def __init__(self):
        # Setup wstępny
        pygame.init()
        self.display_surface = pygame.display.set_mode((st.WINDOW_WIDTH, st.WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire shooter')
        self.clock = pygame.time.Clock() # Zegar
    
        # Grupy
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group() # Grupa kolizyjna
        self.bullet_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()

        # Gun timer - setup liczników
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100 # 9-10 kuli na sekundę
        
        # Event enemy
        self.enemies_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemies_event, 2000)
        self.enemy_spawn_points = [] # Lista spawnpointów dla Enemy

        # Audio
        self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.02)
        
        self.impact_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        self.impact_sound.set_volume(0.02)
        
        self.music = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.music.set_volume(0.01)
        self.music.play(loops = -1)
        # Uruchamia mapę, postaci 
        self.setup_graphics()
        self.load_images()
        
    def input(self):
        # Kliknięcie LMB
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            # Pozycja zmienna dla broni z offsetem gdzie patrzymy
            # ustawiamy centrum kuli w centrum końcówki broni * offset
            gun_head_pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, gun_head_pos,
                   self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    def gun_timer(self):
        """Pozwala zrobić cooldown dla strzałów"""
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True
    
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        
        # [0] Uzyskuję informację o ścieżce, folderach, plikach -> [1] folderach bat, blob, skeleton
        # uzyskaliśmy nazwy folderów
        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders: # W tych subfolderach bat, blob, skeleton
            # Teraz wypiszemy ścieżkę folderów i łączymy z plikami
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)
        
    def setup_graphics(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))      
        # Dla każdego kafelka w gridzie - background
        for x, y, image in map.get_layer_by_name('Ground').tiles(): # Wyciągamy kafelki
            # Mnożenie pozwala uzyskać środek mapy    
            Sprite((x * st.TILE_SIZE,y * st.TILE_SIZE), image, self.all_sprites)

        # Dostęp do kolizji w mapie - border collisions
        for collision in map.get_layer_by_name('Collisions'):
            CollisionSprite((collision.x,collision.y),
                            pygame.Surface((collision.width, collision.height)),
                            (self.collision_sprites))

        # Dostęp do elementów w mapie - objects
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x,obj.y), obj.image, (self.all_sprites,self.collision_sprites))
        # Dla każdego markera w grze dla postaci - entities
        for marker in map.get_layer_by_name('Entities'):
            if marker.name == 'Enemy':
                self.enemy_spawn_points.append((marker.x, marker.y))
            else: # marker.name == 'Player':
                # Gracz w grupie sprites, ale nie jest w kolizyjnej!!!
                # tworzy go w markerze na mapie
                self.player = Player((marker.x,marker.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
        
    def bullet_kill(self):
        if self.bullet_sprites: # By miało sens
            for bullet in self.bullet_sprites:
                collided_sprites = pygame.sprite.spritecollide(bullet, self.enemies_sprites, False, pygame.sprite.collide_mask)
                # Własny licznik zniszczenia sprite
                if collided_sprites:
                    self.impact_sound.play()
                    for sprite in collided_sprites:
                        sprite.destroy()
                    bullet.kill()
                    
    def player_kill(self):
        if pygame.sprite.spritecollide(self.player, self.enemies_sprites, False, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()
            
    def run(self):
        while True:
            dt = self.clock.tick(59) / 1000 # Pomiar czasu [s] do wytworzenia 1 klatki czas/liczbę klatek
# =============================================================================
#       Event
# =============================================================================
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and 
                                                 event.key == pygame.K_ESCAPE): # Wyłącza grę przy kliknięciu X
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == self.enemies_event:
                    # choice(self.enemy_spawn_points)
                    Enemies(choice(list(self.enemy_frames.values())), choice(self.enemy_spawn_points), self.player,
                            (self.all_sprites, self.enemies_sprites), self.collision_sprites)
# =============================================================================
#       Gra          
# =============================================================================
            # Update
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_kill()
            self.player_kill()
            
            # Wyświetlanie
            self.all_sprites.draw(self.player.rect.center) # Follow gracza
            pygame.display.update() # Wyświetlacz
            
        # Exit
        pygame.quit()
        sys.exit()
# =============================================================================
#       Program
# =============================================================================
if __name__ == '__main__': # Upewnia się że tylko ten plik jest teraz aktywny
    game = Game()
    game.run()
    