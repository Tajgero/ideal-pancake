import pygame
import settings as st
from random import choice, uniform

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups, position):
        super().__init__(groups)
    
        # Obraz
        self.image = pygame.Surface(st.SIZE['paddle'], pygame.SRCALPHA)
        # Rysowanie na niewidzialnym obrazie platformy; (0,0) to topleft, size, width, border_radius
        pygame.draw.rect(self.image, st.COLORS['paddle'], 
                         pygame.FRect((0,0), st.SIZE['paddle']), 0, 4)
        
        # Shadow surf
        self.shadow_surf = self.image.copy()
        pygame.draw.rect(self.shadow_surf, st.COLORS['paddle shadow'], 
                         pygame.FRect((0,0), st.SIZE['paddle']), 0, 4)
        
        # Rect
        self.rect = self.image.get_frect(center = position)
        self.old_rect = self.rect.copy()
        self.direction = 0

    def move(self, dt):
       self.rect.centery +=  self.direction * self.speed * dt
       self.rect.top = 0 if self.rect.top < 0 else self.rect.top
       self.rect.bottom = st.WINDOW_HEIGHT if self.rect.bottom > st.WINDOW_HEIGHT else self.rect.bottom

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)


class Player(Paddle):
    # Update i tak będzie działać, bo zostaje wywołana metoda w
    # main.py jako grupa odziedziczona
    def __init__(self, groups, position):
        super().__init__(groups, position)
        self.speed = st.SPEED['player']
        
    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN]) or keys[pygame.K_s] - int(keys[pygame.K_UP] or keys[pygame.K_w])

    
class Opponent(Paddle):
    def __init__(self, groups, position, ball):
        super().__init__(groups, position)
        self.ball = ball
        self.speed = st.SPEED['opponent']
    
    def get_direction(self):
        # Tutaj wykorzystuje się metodę move, zmiana kierunku wywołuje
        # dążenie za piłką
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1
            
        
class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, position, collision, update_score):
        super().__init__(groups)
        self.paddle_sprites = collision
        self.update_score = update_score
        
        # Obraz - SRCALPHA zezwala na wartości alfa dla obrazu
        self.image = pygame.Surface(st.SIZE['ball'], pygame.SRCALPHA)
        # Rysowanie na niewidzialnym obrazie krążka
        pygame.draw.circle(self.image, st.COLORS['ball'],
                           (st.SIZE['ball'][0]/2, st.SIZE['ball'][1]/2), st.SIZE['ball'][0]/2)
        
        # Shadow of a ball
        self.shadow_surf = self.image.copy()
        pygame.draw.circle(self.shadow_surf, st.COLORS['ball shadow'],
                           (st.SIZE['ball'][0]/2, st.SIZE['ball'][1]/2), st.SIZE['ball'][0]/2)
        
        # Rect
        self.rect = self.image.get_frect(center = position)
        self.old_rect = self.rect.copy()
        self.direction = pygame.Vector2(choice((-1, 1)), uniform(0.7, 0.8) * choice((-1, 1)))
        self.speed = st.SPEED['ball']
        self.speed_modifier = 0
        
        # Timer
        self.start_time = pygame.time.get_ticks()
        self.duration = 1200
        
    def move(self, dt):
        # Dzielę na poszczególne składowe, żeby sprawdzić kolizje z kulką
        self.rect.x += self.direction.x * self.speed * dt * self.speed_modifier
        self.collision('horizontal') # Kolizje z paddle horyzontalne
        
        self.rect.y += self.direction.y * self.speed * dt * self.speed_modifier
        self.collision('vertical') # Kolizje z paddle wertykalne
        
    def wall_collision(self):
        if self.rect.top < 0 or self.rect.bottom > st.WINDOW_HEIGHT:
            self.direction.y = -self.direction.y
            
            if self.rect.top < 0: self.rect.top = 0
            else: self.rect.bottom = st.WINDOW_HEIGHT
        
        elif self.rect.right >= st.WINDOW_WIDTH or self.rect.left <= 0:
            # Wybór stron
            self.update_score('player' if self.rect.x < st.WINDOW_WIDTH / 2 else 'opponent')
            self.reset()
            
    def reset(self):
        self.rect.center = (st.WINDOW_WIDTH / 2, st.WINDOW_HEIGHT / 2)
        self.direction = pygame.Vector2(choice((-1, 1)), uniform(0.7, 0.8) * choice((-1, 1)))
        self.start_time = pygame.time.get_ticks()
        
    def timer(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            self.speed_modifier = 1
        else:
            self.speed_modifier = 0
        
    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    # Test gdy obiekt nadlatuje z lewej sprawdzamy 2 klatki nowe i stare
                    # gdy nachodzi mocno z prawej, a stare klatki są daleko z lewej
                    # test na overlap i test na badanie strony
                    # Uderzenie z lewej paddle
                    if self.rect.right > sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x = -self.direction.x
                    # Uderzenie z prawej paddle
                    elif self.rect.left < sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x = -self.direction.x
                else: # Kolizja vertical
                    # Uderzenie z góry paddle
                    if self.rect.bottom > sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = -self.direction.y
                    # Uderzenie z dołu paddle
                    elif self.rect.top < sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = -self.direction.y
                        
    def update(self, dt):
        self.old_rect = self.rect.copy() # Najpierw pobieramy klatkę
        self.timer() # Timer dla poruszania kuli - resetu
        self.wall_collision() # Kolizje ze ścianami
        self.move(dt) # Poruszamy kolejne klatki
