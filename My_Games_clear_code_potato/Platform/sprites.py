from settings import *
from timer import Timer
from math import sin
from random import randint

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)


class Bullet(Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(pos, surf, groups)

        # Adjustment
        # only true when bullet is going to the left
        self.image = pygame.transform.flip(self.image, direction == -1, False)

        # Movement
        self.direction = direction
        self.speed = 850
        
    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt


class Fire(Sprite):
    def __init__(self, surf, pos, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
        self.flip = player.flip_side
        self.timer = Timer(100, autostart=True, func=self.kill)
        self.y_offset = pygame.Vector2(0, 10)

        if self.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset
            
    def update(self, _):
        self.timer.update()
        
        if self.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset
        
        # when player turn around after shoot, kill object
        if self.flip != self.player.flip_side:
            self.kill()


class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]


class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames, create_bullet):
        super().__init__(frames, pos, groups)

        # Movement & Collision
        self.start_point = pos # topleft point
        self.flip_side = False
        self.direction = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.create_bullet = create_bullet
        self.speed = 400
        self.grav = 50
        self.on_floor = False
        
        # Timer
        self.shoot_timer = Timer(500)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        
        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -20
            
        if keys[pygame.K_f] and not self.shoot_timer:
            self.create_bullet(self.rect.center, -1 if self.flip_side else 1)
            self.shoot_timer.activate()
            
        if keys[pygame.K_r]:
            self.rect.topleft = self.start_point
            
    def move(self, dt):
        # horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        # vertical
        self.direction.y += self.grav * dt
        self.rect.y += self.direction.y
        self.collision('vertical')
        
    def collision(self, direction):
        # TODO HITBOXES
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def check_floor(self):
        """
        Checks if rectangle below player collides with floor elements
        """
        bottom_rect = pygame.FRect((0,0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
        level_rects = [sprite.rect for sprite in self.collision_sprites]
        
        # Returns index of collided level rect (-1 if None)
        self.on_floor = True if bottom_rect.collidelist(level_rects) >= 0 else False

    def animate(self, dt):
        if self.direction.x: # If I move somewhere
            self.frame_index += self.animation_speed * dt
            self.flip_side = self.direction.x < 0 # Updates ONLY when I change direction (CLEVER SOULUTION)
        else:
            self.frame_index = 0
            
        self.frame_index = 1 if not self.on_floor else self.frame_index
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip_side, False)

    def update(self, dt):
        self.shoot_timer.update()
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)


class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
        self.death_timer = Timer(200, func = self.kill)
        
    def destroy(self):
        """Destroy enemy with making them white silhouette"""
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')

    def update(self, dt):
        """Used only in targeted enemies"""
        self.death_timer.update()
        if not self.death_timer:
            self.move(dt)
            self.animate(dt)
            self.constraint()


class Bee(Enemy):
    def __init__(self, pos, groups, frames, speed):
        super().__init__(frames, pos, groups)
        self.speed = speed
        self.amplitude = randint(500,600)
        self.frequency = randint(300,600)
        
    def move(self, dt):
        """For rect.y in all timeline get fluctuation motion"""
        self.rect.x -= self.speed * dt
        self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt
    
    def constraint(self):
        """If bee is far left of game window"""
        if self.rect.right <= 0:
            self.kill()
        
    
class Worm(Enemy):
    def __init__(self, rect, groups, frames, speed):
        super().__init__(frames, rect.topleft, groups)
        self.flipped_frames = [pygame.transform.flip(surf, True, False) for surf in self.frames]
        self.normal_frames = self.frames.copy()
        self.enemy_area = rect
        self.animation_speed = 5
        self.speed = speed
        self.direction = 1 # 1: Right; -1: Left
        
        # Place worm on the ground
        self.rect.bottomleft = self.enemy_area.bottomleft
        
    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt

    def constraint(self):
        self.frames = self.normal_frames if self.direction == 1 else self.flipped_frames
        if not self.enemy_area.contains(self.rect):
            self.direction *= -1
