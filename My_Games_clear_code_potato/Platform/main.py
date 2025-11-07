from pytmx.util_pygame import load_pygame
from os.path import join
from os import walk
from sys import exit
from support import *
from settings import * 
from sprites import * 
from random import randint
from groups import AllSprites
from timer import Timer

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        # load game
        self.load_assets()
        self.setup()
        
    def load_assets(self):
        # graphics
        self.player_frames = import_folder('images', 'player')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')

        # sounds
        pygame.mixer.stop() # Stops playing all sounds
        self.audio = audio_importer('audio') # folder name audio
        
        # timers
        self.bee_timer = Timer(2000, func=self.create_bee, repeat=True, autostart=True)
    
    def create_bee(self):
        Bee(
          pos=(self.level_width + WINDOW_WIDTH, randint(0,self.level_height)),
          groups=(self.all_sprites, self.enemy_sprites),
          frames=self.bee_frames,
          speed=randint(300, 500)
        )
     
    def create_bullet(self, pos, direction):
        """Player x + direction of bullet * some_value_pixels for right or left (bullet gets flipped)
        I take surface in front of the player in correct position
        """
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet(self.bullet_surf, (x, pos[1]), direction, (self.all_sprites, self.bullet_sprites))
        Fire(self.fire_surf, pos, self.all_sprites, self.player)
        self.audio['shoot'].play().set_volume(0.008)
        
    def setup(self):
        tmx_map = load_pygame(join('data', 'maps', 'world.tmx'))
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE
        
        for x, y, image in tmx_map.get_layer_by_name('Main').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))
        
        for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames, self.create_bullet)
            elif obj.name == 'Worm':
                Worm(
                  rect=pygame.FRect(obj.x, obj.y, obj.width, obj.height),
                  groups=(self.all_sprites, self.enemy_sprites),
                  frames=self.worm_frames,
                  speed=randint(100, 140)
                )
        self.audio['music'].play(loops = -1).set_volume(0.008)
        
    def collision(self):
        # Bullets -> Enemies
        for bullet in self.bullet_sprites:
            sprite_collision = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collision:
                self.audio['impact'].play().set_volume(0.01)
                bullet.kill()
                for sprite in sprite_collision:
                    sprite.destroy()
                    
        # Enemies -> Player
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            # TODO: Health bar
            self.running = False
        
    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and 
                                                 event.key == pygame.K_ESCAPE):
                    self.running = False 
            
            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collision()

            # draw & camera positioning
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(target_pos=self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()
        exit()

if __name__ == '__main__':
    game = Game()
    game.run()
