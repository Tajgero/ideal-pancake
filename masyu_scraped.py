class MasyuSolver:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = {}  # (x,y): typ_kółka ('white', 'black', None)
        self.lines = {}  # ((x1,y1), (x2,y2)): bool - czy linia istnieje
        
    def add_circle(self, x, y, circle_type):
        """Dodaje białe ('white') lub czarne ('black') kółko"""
        self.grid[(x, y)] = circle_type
    
    def get_neighbors(self, x, y):
        """Zwraca sąsiadów komórki"""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors
    
    def count_lines(self, x, y):
        """Liczy linie wychodzące z komórki"""
        count = 0
        connected = []
        for nx, ny in self.get_neighbors(x, y):
            edge = tuple(sorted([(x, y), (nx, ny)]))
            if self.lines.get(edge, False):
                count += 1
                connected.append((nx, ny))
        return count, connected
    
    def get_solution_grid(self):
        """Tworzy tablicę 2D z rozwiązaniem - pokazuje krawędzie między komórkami"""
        # Tworzymy większą siatkę aby pokazać krawędzie
        solution_width = self.width * 2 - 1
        solution_height = self.height * 2 - 1
        solution = [['.' for _ in range(solution_width)] for _ in range(solution_height)]
        
        # Zaznacz komórki z kółkami
        for (x, y), circle_type in self.grid.items():
            if circle_type == 'white':
                solution[y*2][x*2] = 'O'
            elif circle_type == 'black':
                solution[y*2][x*2] = '●'
            else:
                solution[y*2][x*2] = '+'
        
        # Zaznacz linie
        for edge, exists in self.lines.items():
            if exists:
                (x1, y1), (x2, y2) = edge
                # Znajdź środek krawędzi
                mid_x = x1 + x2
                mid_y = y1 + y2
                
                if x1 == x2:  # Linia pionowa
                    solution[mid_y][mid_x] = '|'
                else:  # Linia pozioma
                    solution[mid_y][mid_x] = '-'
        
        # Zaznacz pustę komórki bez kółek
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in self.grid:
                    solution[y*2][x*2] = '+'
        
        return solution
    
    def print_solution(self):
        """Wyświetla rozwiązanie w czytelnej formie"""
        solution = self.get_solution_grid()
        print("\nRozwiązanie:")
        print("O = białe kółko, ● = czarne kółko, + = pusta komórka")
        print("| = linia pionowa, - = linia pozioma")
        print()
        
        for row in solution:
            print(' '.join(row))
    
    def validate_white_circle(self, x, y):
        """Sprawdza reguły białego kółka"""
        count, connected = self.count_lines(x, y)
        if count == 0:
            return True  # Nie ma jeszcze linii - dozwolone podczas budowania
        if count != 2:
            return count < 2  # Może mieć mniej niż 2 podczas budowania
        
        # Linia musi przechodzić prosto
        if len(connected) == 2:
            (x1, y1), (x2, y2) = connected
            return (x1 == x2 == x) or (y1 == y2 == y)
        return True
    
    def validate_black_circle(self, x, y):
        """Sprawdza reguły czarnego kółka"""
        count, connected = self.count_lines(x, y)
        if count == 0:
            return True  # Nie ma jeszcze linii - dozwolone podczas budowania
        if count != 2:
            return count < 2  # Może mieć mniej niż 2 podczas budowania
        
        # Linia musi skręcać (nie może być prosta)
        if len(connected) == 2:
            (x1, y1), (x2, y2) = connected
            return not ((x1 == x2 == x) or (y1 == y2 == y))
        return True
    
    def is_valid_partial(self):
        """Sprawdza częściową poprawność podczas budowania rozwiązania"""
        # Sprawdź czy żadna komórka nie ma więcej niż 2 linie
        for x in range(self.width):
            for y in range(self.height):
                count, _ = self.count_lines(x, y)
                if count > 2:
                    return False
        
        # Sprawdź reguły kółek
        for (x, y), circle_type in self.grid.items():
            if circle_type == 'white':
                if not self.validate_white_circle(x, y):
                    return False
            elif circle_type == 'black':
                if not self.validate_black_circle(x, y):
                    return False
        
        return True
    
    def create_simple_puzzle(self):
        """Tworzy prostą łamigłówkę do przetestowania"""
        # Resetuj stan
        self.lines = {}
        
        # Proste rozwiązanie - kwadrat 3x3
        if self.width >= 3 and self.height >= 3:
            # Dodaj białe kółko w środku
            self.grid[(1, 1)] = 'white'
            
            # Ręcznie ustaw poprawne rozwiązanie
            lines_to_add = [
                ((0, 1), (1, 1)),  # lewo do środka
                ((1, 1), (2, 1)),  # środek do prawa
                ((1, 0), (1, 1)),  # góra do środka
                ((1, 1), (1, 2)),  # środek do dołu
                ((0, 0), (0, 1)),  # górny lewy narożnik
                ((0, 1), (0, 2)),  # lewy bok
                ((0, 2), (1, 2)),  # dolny lewy narożnik
                ((1, 2), (2, 2)),  # dolny bok
                ((2, 2), (2, 1)),  # dolny prawy narożnik
                ((2, 1), (2, 0)),  # prawy bok
                ((2, 0), (1, 0)),  # górny prawy narożnik
                ((1, 0), (0, 0)),  # górny bok
            ]
            
            for edge in lines_to_add:
                self.lines[tuple(sorted(edge))] = True
            
            return True
        return False

# Przykład użycia:
solver = MasyuSolver(3, 3)

# Utwórz prostą łamigłówkę
if solver.create_simple_puzzle():
    print("Utworzono przykładową łamigłówkę!")
    solver.print_solution()
else:
    print("Nie udało się utworzyć łamigłówki")

# Test z pustą planszą
print("\n" + "="*40)
print("Test z pustą planszą 4x4:")
empty_solver = MasyuSolver(4, 4)
empty_solver.add_circle(1, 1, 'white')
empty_solver.add_circle(2, 2, 'black')
