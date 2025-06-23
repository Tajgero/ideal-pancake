import random

class Minesweeper():
    """
    Minesweeper game representation
    """
    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """
        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    
    Sentence only consider cells which are with unknown bomb/safe status
    
    sentence = tuple(set{str}, count: int)
    self.cells = set(tuple, tuple ...)
    self.count = int
    
    sentence_0 = Sentence({(1,5), (2,6), ...}, 2)
    """
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other): # Same sentence <-> True
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        If count equals number of cells then all of the are mines.
        """
        return self.cells if len(self.cells) == self.count else set()
        
    def known_safes(self) -> set:
        """
        Returns the set of all cells in self.cells known to be safe.
        If count equals 0 then all cells are safe
        """
        return self.cells if self.count == 0 else set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine. (count decreases)
        """
        # If cell is one of the cells included in the sentence
        if cell in self.cells:
            # Function updates the sentence so that cell is no longer in the sentence,
            # but still is logically correct given that cell is known to be a mine.
            self.cells.remove(cell)
            self.count -= 1
            
        # No action needed otherwise

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        Same as mark_mine but with safe cells (count remains)
        """
        if cell in self.cells:
            self.cells.remove(cell)
            
            
class MinesweeperAI():
    """
    Minesweeper game player
    """
    def __init__(self, height=8, width=8):

        # Set initial height and width of a board
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        In sentence this mine cell is discarded, but will be in
        self.mines inside AI class
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        In sentence this safe cell is discarded, but will be in
        self.mines inside AI class
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        
        |  1  |  1  |  1  |
        |  A  |  B  |  C  | => {A,B,C,D,E} = 2
        |  D  | (2) |  E  |
                
        This function should:
        1) mark the cell as a move that has been made
        2) mark the cell as safe
        3) add a new sentence to the AI's knowledge base
           based on the value of `cell` and `count`
        4) mark any additional cells as safe or as mines
           if it can be concluded based on the AI's knowledge base
        5) add any new sentences to the AI's knowledge base
           if they can be inferred from existing knowledge
        """
        # 1) Adding move to made moves
        self.moves_made.add(cell)


        # 2) If this move has been made then it is safe cell (no game over yet)
        #    and updates any sentencess that contain this cell
        self.mark_safe(cell)
        
        
        # 3) Add new sentence to knowledge with only
        #    undeterminated states (mine or safe)
        # I know count, and I need all possible neighbors
        neighbors = self.get_neighbors(cell)
        
        # ONLY UNDETERMINATED STATES
        # New copy of set to not modify while iterating it
        neighbors_to_check = neighbors.copy()
        for neighbor in neighbors:
            
            if neighbor in (self.mines | self.safes):
                neighbors_to_check.remove(neighbor)
        
        # NEWLY CREATED SENTENCE FOR FUTURE USE
        new_sentence = Sentence(neighbors_to_check, count)
        self.knowledge.append(new_sentence)
        
        
        # 4) Inference to mark additional cells as safe or mine
        #    based on sentence internal knowledge 
        # Iterate through without changed knowledge list
        knowledge = self.knowledge.copy()
        for sentence in knowledge:
            
            # First make sure to delete all blank sentences in knowledge
            if sentence.cells == set():
                self.knowledge.remove(sentence)
                continue
            
            # Conclude safe cells
            if sentence.known_safes():
                cells = [cell for cell in sentence.known_safes()]
                for cell in cells:
                    self.mark_safe(cell)

            # Conclude mine cells
            if sentence.known_mines():
                cells = [cell for cell in sentence.known_mines()]
                for cell in cells:
                    self.mark_mine(cell)

                
        # 5) Inference by checking subsets of newly created sentence to
        #    create new sentences for knowledge (I think self.knowledge)
        if len(self.knowledge) > 1:
            
            for sentence in knowledge:
                
                sentence_1, sentence_2 = new_sentence, sentence
                if sentence_1 == sentence_2:
                    continue
                
                # If I find subset in pair of sentences
                # then I can inference some new logic
                # New sentence with cells and different count
                if sentence_1.cells <= sentence_2.cells:
                    new_cells = sentence_2.cells - sentence_1.cells
                    new_count = sentence_2.count - sentence_1.count
                    new_sentence = Sentence(new_cells, new_count)
                    
                    # If sentence already in knowledge skip it
                    if any(new_sentence == sentence for sentence in self.knowledge):
                        continue
                    
                    self.knowledge.append(
                        Sentence(new_cells, new_count)
                    )
        
        
        # Shows what is going on in knowledge base, safe and mine cells
        for i, sentence in enumerate(self.knowledge):
            print(f"Se_{i}: {sentence}")
        print(f"Safe: {self.safes}")        
        print(f"Mine: {self.mines}")        
        print("\n")
        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made:
                return move
            
        return None
        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board
        if safe move is not possible.
        
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # For user's own safety ;>
        if self.make_safe_move() == None:
            
            # Makes list(tuples) of possible moves for now
            possible_moves = [(i, j) for i in range(self.height) for j in range(self.width)]
            
            # Modifies possible moves based on: mines and moves_made cells
            for cell in (self.mines | self.moves_made):
                possible_moves.remove(cell)

            # Pick random move from possible moves list
            return random.choice(possible_moves)
            
        return None

    def get_neighbors(self, cell):
        """
        Helper function that returns all neighbors
        of a given cell in 3x3 grid in set
        based on height and width of a board
        """
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                
                # Add neighbors of cell in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))
                
        # Do not include cell itself
        neighbors.remove(cell)
        
        return neighbors
