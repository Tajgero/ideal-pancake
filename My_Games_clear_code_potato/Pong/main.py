import pygame, sys, json
from os.path import join
from groups import AllSprites
import settings as st
from sprites import Player, Opponent, Ball

class Game():
    def __init__(self):
        # Setup wstępny
        pygame.init()
        self.display_surface = pygame.display.set_mode((st.WINDOW_WIDTH, st.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Pong!')

        # Grupy
        self.all_sprites = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()
        
        # Sprites
        self.ball = Ball(self.all_sprites, (st.WINDOW_WIDTH / 2, st.WINDOW_HEIGHT / 2), self.paddle_sprites, self.update_score)
        self.player = Player((self.all_sprites, self.paddle_sprites), st.POS['player'])
        self.opponent = Opponent((self.all_sprites, self.paddle_sprites), st.POS['opponent'], self.ball)
        
        # Score
        self.font = pygame.font.Font(None, 160) # Domyślny, wielkość
        try:
            with open(join('data', 'score.txt')) as f:
                # Otwiera plik z wynikiem
                self.score = json.load(f)
        except:
            self.score = {'player' : 0, 'opponent' : 0}       
        
    def display_score(self):
        # player - napis, antialias, kolor
        player_surf = self.font.render(str(self.score['player']), True, st.COLORS['bg detail'])
        player_rect = player_surf.get_frect(center = st.POS['score_player'])
        self.display_surface.blit(player_surf, player_rect) # Wyświetla na ekranie - surface, rect
        
        # opponent - napis, antialias, kolor
        opponent_surf = self.font.render(str(self.score['opponent']), True, st.COLORS['bg detail'])
        opponent_rect = player_surf.get_frect(center = st.POS['score_opponent'])
        self.display_surface.blit(opponent_surf, opponent_rect) # Wyświetla na ekranie - surface, rect
        
        # Line seperator - surface, kolor, pozycja start, pozycja koniec, grubość
        pygame.draw.line(self.display_surface, st.COLORS['bg detail'],
                         (st.WINDOW_WIDTH / 2, 0), (st.WINDOW_WIDTH / 2, st.WINDOW_HEIGHT), 8)
        
    def update_score(self, side):
        # Sprawdza warunek i dla odpowiedniej strony dodaje licznik
        self.score['player' if side == 'player' else 'opponent'] += 1
        
    def run(self):
        while True:
            dt = self.clock.tick(59) / 1000
# =============================================================================
#       Event
# =============================================================================
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and 
                                                 event.key == pygame.K_ESCAPE):
                    with open(join('data', 'score.txt'), 'w') as f:
                        # Tworzy plik i zapisuje w formacie json
                        json.dump(self.score, f)
                        
                    pygame.quit()
                    sys.exit()            
# =============================================================================
#       Gra          
# =============================================================================
            # Update
            self.all_sprites.update(dt)

            # Wyświetlanie - wyznaczona kolejność
            self.display_surface.fill(st.COLORS['bg'])
            self.display_score()
            self.all_sprites.draw() # Nie trzeba dawać display_surface, bo zmodyfikowaliśmy grupę
            pygame.display.update()
            
        # Exit - poza loop
        pygame.quit()
        sys.exit()
# =============================================================================
#       Program
# =============================================================================
if __name__ == '__main__':
    game = Game()
    game.run()
    