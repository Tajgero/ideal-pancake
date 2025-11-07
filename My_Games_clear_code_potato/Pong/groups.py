import pygame

class AllSprites(pygame.sprite.Group):
    """Zmodyfikowana grupa AllSprites"""
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
                
    def draw(self):
        # Wyświetla shadow - surface, pozycja + offset
        for sprite in self:
            for i in range(5): # Tworzy 5 surface cieni na każdą klatkę
                self.display_surface.blit(sprite.shadow_surf, sprite.rect.topleft + pygame.Vector2(i,i))
        
        # Wyświetla wszystko
        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect)