import pygame
import random
import time

# Parametry siatki
GRID_SIZE = 80  # Rozmiar siatki (30x30 komórek)
CELL_SIZE = 10  # Rozmiar jednej komórki w pikselach
ALIVE_COLOR = (0, 0, 0)  # Kolor żywej komórki (czarny)
DEAD_COLOR = (255, 255, 255)  # Kolor martwej komórki (biały)

# Ustawienia okna
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Gra w Życie Conwaya")
clock = pygame.time.Clock()

# Tworzenie słownika z komórkami
grid = {}

# Funkcja inicjalizująca siatkę (komórki losowe)
def initialize_grid():
    global grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            # Losowa wartość 0 lub 1 - żywa lub martwa komórka
            grid[(x, y)] = 0  # Wszystkie komórki są martwe na początku
            
            # LOSOWOŚĆ
            # grid[(x, y)] = random.choice([0, 1])

# Funkcja rysująca siatkę
def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = ALIVE_COLOR if grid.get((x, y), 0) == 1 else DEAD_COLOR
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Funkcja sprawdzająca liczbę żywych sąsiadów
def count_alive_neighbors(x, y):
    alive_count = 0
    # Przeszukujemy sąsiednie komórki (8 kierunków)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Pomijamy samą komórkę
            # Pozwala na warunki periodyczne
            nx, ny = (x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE
            alive_count += grid.get((nx, ny), 0)  # Używamy get() aby uniknąć błędu KeyError
            
            # BEZ warunków periodycznych
            # nx, ny = x + dx, y + dy
            # if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            #     alive_count += grid.get((nx, ny), 0)  # Używamy get() aby uniknąć błędu KeyError
            
    return alive_count

# Funkcja do przeprowadzenia jednej tury gry
def next_generation():
    new_grid = {}  # Nowa siatka dla kolejnej generacji

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            alive_neighbors = count_alive_neighbors(x, y)
            current_state = grid.get((x, y), 0)  # Używamy get() aby uniknąć błędu KeyError

            if current_state == 1:
                if alive_neighbors < 2 or alive_neighbors > 3:
                    new_grid[(x, y)] = 0  # Umiera
                else:
                    new_grid[(x, y)] = 1  # Żyje dalej
            else:
                if alive_neighbors == 3:
                    new_grid[(x, y)] = 1  # Ożywa

    return new_grid

# Funkcja do obsługi kliknięć myszy
def handle_mouse_click():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x = mouse_x // CELL_SIZE
    grid_y = mouse_y // CELL_SIZE
    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
        # Zmiana stanu komórki (na żywą lub martwą)
        current_state = grid.get((grid_x, grid_y), 0)
        grid[(grid_x, grid_y)] = 1 - current_state  # Zmiana stanu z 0 na 1 lub z 1 na 0

# Funkcja główna
def game_of_life():
    initialize_grid()  # Inicjalizujemy siatkę
    setting_colony = True  # Tryb ustawiania kolonii przed rozpoczęciem gry
    
    running = True
    while running:
# =============================================================================
#         System Eventów
# =============================================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False  # Zakończ program jeśli okno zostanie zamknięte
                
            elif event.type == pygame.MOUSEBUTTONDOWN and setting_colony:
                handle_mouse_click()  # Obsługuje kliknięcia myszy w trybie ustawiania kolonii
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and setting_colony:
                    setting_colony = False  # Rozpoczęcie gry po naciśnięciu spacji

        # Rysowanie siatki
        screen.fill(DEAD_COLOR)  # Czyścimy ekran na biało
        draw_grid()

        # Jeśli ustawianie kolonii jest zakończone, przechodzimy do następnej generacji
        if not setting_colony:
            global grid
            grid = next_generation()  # Przechodzimy do następnej generacji

        pygame.display.update()  # Aktualizujemy ekran
        clock.tick(10)  # Prędkość animacji - 10 klatek na sekundę

    pygame.quit()

# =============================================================================
#         Uruchomienie gry
# =============================================================================
game_of_life()
