import sys, os, glob, random, pygame

def clear_line(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)
        
        
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, book):
        self.frontier.append(book)
        
    def top(self):
        if self.empty():
            return print("empty frontier")
        else:
            return self.frontier[-1]

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            return print("empty frontier")
        else:
            book = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return book
        

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, display):
        super().__init__(groups)
        self.image = pygame.transform.scale_by(pygame.image.load("images/desk.png"), 0.8).convert_alpha()
        self.rect = self.image.get_frect(midbottom = (WIDTH / 2, HEIGHT))
        self.desk = StackFrontier()
        self.exp = 0
        self.health = 100
        self.level = 1
        self.exp_cap = 5
        self.promotion_chance = 0.7
        
    def gain_exp(self, amount):
        self.exp += amount
        
    def lose_exp(self, amount):
        self.exp -= amount
        
    def gain_health(self, amount):
        self.health += amount
        
    def lose_health(self, amount):
        self.health -= amount
        
    def promotion(self) -> bool:
        if self.exp >= self.exp_cap:
            check_chance = random.random()
            if check_chance <= self.promotion_chance:
                self.exp = 0
                self.level += 1
                self.exp_cap += 5
                self.promotion_chance -= 0.1
                return True
            else:
                print("\nGame Over")
                return False
        
    def stat(self):
        return [
        f"Level: {self.level} | chance: {self.promotion_chance * 100}%",
        f"Health: {self.health}",
        f"Experience: {self.exp}/{self.exp_cap}"
        ]


class Book(pygame.sprite.Sprite):
    def __init__(self, groups, surface, color, on_top_rect, player, progress_cap=10, rand=True):
        super().__init__(groups)
        self.image = surface[color]
        self.rect = self.image.get_frect(midbottom=on_top_rect.midtop)
        self.player = player
        if rand:
            self.rect.centerx = self.player.rect.centerx + random.uniform(-20, 20)
        self.progress_cap = progress_cap
        self.progress = 0
        
    def reading(self, amount=1):
        if self.progress < self.progress_cap:
            self.progress += amount
        else:
            self.player.desk.remove()
            self.kill()
            self.player.gain_exp(2)
            
        print(f"{self.progress} / {self.progress_cap}")


if __name__ == "__main__":
    pygame.init()
    WHITE = (255, 255, 255)
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    running = True
    
    # Player and desk
    all_sprites = pygame.sprite.Group()

    player = Player(all_sprites, screen)
    player.desk.add(player)
    player.stat()    
    
    # Fonts
    font = pygame.font.SysFont("consolas", 28)
    
    # Book
    books_frames = {os.path.basename(path).split("_")[0] : pygame.transform.scale_by(pygame.image.load(path), 0.2).convert_alpha() for path in glob.glob("images/*_book.png")}
    exp_show_rect = False
    
    # Custom Events
    reading_event = pygame.event.custom_type()
    pygame.time.set_timer(reading_event, 1100)
    
    
    # Game Loop
    while running:
        
        # BACKGROUND
        screen.fill("#413c4f")
        
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == reading_event:
                if len(player.desk.frontier) > 1:
                    book = player.desk.top()
                    book.reading()
                    exp_show_rect = pygame.Rect(book.rect.x - 30, book.rect.y, 10, 10)
            
        # Keys
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_COMMA]:
            if len(player.desk.frontier) > 1:
                book = player.desk.remove()
                book.kill()
        if recent_keys[pygame.K_PERIOD]:
            if len(player.desk.frontier) < 9:
                player.desk.add(
                    Book(
                        all_sprites,
                        books_frames,
                        random.choice(list(books_frames.keys())),
                        player.desk.top().rect,
                        player
                    )
                )

        # Ending
        if player.level >= 4:
            running = False

        # Game plays
        player.promotion()
        
        # Render objects
        all_sprites.draw(screen)
        
        if len(player.desk.frontier) > 1 and exp_show_rect:
            pygame.draw.rect(screen, "green", exp_show_rect)

        for i, stat in enumerate(player.stat()):
            line = font.render(stat, True, WHITE)
            line_rect = line.get_rect()
            line_rect.center = (WIDTH / 2, (HEIGHT / 2) * ((i + 1) / 8))
            screen.blit(line, line_rect)

        # Render display
        pygame.display.flip()
        dt = clock.tick(59) / 1000  # limits FPS to 59
        
    # Game stops
    pygame.quit()
    sys.exit()
