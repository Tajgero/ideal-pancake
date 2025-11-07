import pygame
from os.path import join 
import settings as st
from math import atan2, degrees

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True # Pozwala na exclusion z sortowania centery


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)
     
        
class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # Player
        self.player = player
        self.distance = 140 # Długość wektora
        self.player_direction = pygame.Vector2()
        
        # Sprite setup
        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surf
        # Kładzie broń w odległości distance od player
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)
        
    def get_vector(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(st.WINDOW_WIDTH / 2,st.WINDOW_HEIGHT / 2)
        # Uzyskujemy wektor znormalizowany kierunkowy dla broni
        self.player_direction = (mouse_pos - player_pos).normalize()
        
    def rotate(self):
        # atan2(y, x) zwraca kąt θ między dodatnią osią x
        # a promieniem od początku do punktu (x, y)
        # -90 żeby poprawnie kierować broń
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        # Flipnie broń przy lewej stronie
        if self.player_direction.x >= 0:
            # Rotozoom zapewnia jakość przy obrocie
            # surface, kąt, skala
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            # abs() naprawia problem odwrotnego obrotu broni
            # dla lewej części -90 do -270, potrzeba dodatnich wartości
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)
        
    def update(self, _):
        self.get_vector()
        self.rotate()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance


class Bullet(pygame.sprite.Sprite):
    def __init__(self, surface, pos, direction, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center = pos)
        self.bullet_speed = 1200
        self.direction = direction
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000

    def update(self, dt):
        self.rect.center += self.direction * self.bullet_speed * dt

        # Zapewnia usunięcie kuli po czasie
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()


class Enemies(pygame.sprite.Sprite):
    def __init__(self, frames, pos, target, groups, collisions):
        super().__init__(groups)
        
        # Klatki
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6
        
        # Ruch
        self.rect = self.image.get_frect(center = pos)
        self.hitbot_rect = self.rect.inflate(-20, -40)
        self.speed = 300
        self.enemy_direction = pygame.Vector2()
        self.collisions = collisions
        self.target = target # Punkt zaczepu wektora, w którą idzie enemy
        
        # Timers
        self.death_time = 0
        self.death_duration = 400
        
    def move(self, dt):
        # Get direction
        player_pos = pygame.Vector2(self.target.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.enemy_direction = (player_pos - enemy_pos).normalize()
        
        # Update rect position + collision logic
        self.hitbot_rect.x += self.enemy_direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbot_rect.y += self.enemy_direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbot_rect.center
    
    def collision(self, direction):
        for sprite in self.collisions:
            if sprite.rect.colliderect(self.hitbot_rect):
                if direction == 'horizontal':
                    if self.enemy_direction.x > 0: # Zderzenie z lewej obiektu
                        self.hitbot_rect.right = sprite.rect.left
                    if self.enemy_direction.x < 0: # Zderzenie z prawej obiektu
                        self.hitbot_rect.left = sprite.rect.right
                else:
                    if self.enemy_direction.y > 0: # Zderzenie z góry obiektu
                        self.hitbot_rect.bottom = sprite.rect.top
                    if self.enemy_direction.y < 0: # Zderzenie z dołu obiektu
                        self.hitbot_rect.top = sprite.rect.bottom
        
    def destroy(self):
        # Timer
        self.death_time = pygame.time.get_ticks()
        # Zmiana obrazu - tworzenie maski z 1 klatki czarno-białej
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf
        
    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()
            
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        
    def update(self, dt):
        # Możliwe tylko gdy nie dostał kulki
        if self.death_time == 0:
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()
        