import pygame
import settings as st

# Pozwoli na modyfikację całego Sprite przez dziedziczenie
# oraz odziedziczenie wszystkich atrybutów
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()
        
    def draw(self, target_pos):
        """Pozwala śledzić gracza"""
        # target pos pobiera z vector2 pozycję dla
        # x, jako [0] oraz y, jako [1]
        self.offset.x = -target_pos[0] + st.WINDOW_WIDTH / 2
        self.offset.y = -target_pos[1] + st.WINDOW_HEIGHT / 2
        
        # Tworzy listę sprites jeśli mają atrybut 'ground'
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        # Tworzy listę sprites jeśli nie mają atrybutu 'ground'
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]
        
        # Dzięki loop layer, sortowanie zachodzi w obrębie ground i object sprites.
        for layer in [ground_sprites, object_sprites]: # Ważna kolejność!
            # Sortuje centery wszystkie sprite według klucza w celu uzyskania efektu
            # postaci występującej przed/za obiektami na podstawie wartości centery.
            # Wszystkie Sprite wchodzą w skład funkcji lambda i wyciąga wartość.
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery): # Pobieramy wszystko ze Sprite
                # Wyświetla wszystko jak było
                # oraz dodatkowy offset image i rect
                # w zależności od pozycji gracza!
                self.display_surface.blit(sprite.image,
                                          sprite.rect.topleft
                                          + self.offset)
