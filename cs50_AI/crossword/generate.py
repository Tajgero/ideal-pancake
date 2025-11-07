import sys
from collections import deque, Counter
from crossword import *


class CrosswordCreator():
    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())


    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var, words in self.domains.items():
            words = words.copy()
            for word in words:
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.
        
        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Conflict is made ONLY when 2 letters in same square
        # Overlap index for each word (square on board = word[i])
        overlap_x, overlap_y = self.crossword.overlaps[x, y]
        domains_x = self.domains[x].copy()
        
        # constraint x(overlap) == y(overlap)
        revised = False
        for word_x in domains_x:
            for word_y in self.domains[y]:
                # If at least one word in Y satisfies constraint:
                # DON'T REMOVE IT and find next word_x
                if word_x[overlap_x] == word_y[overlap_y]:
                    break
            
            # When no y in Y satisfies constraint:
            # REMOVE IT (break doesn't happen)
            else:
                self.domains[x].remove(word_x)
                revised = True
                    
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
    
        (Each arc is a tuple (x, y) of a variable x and a different variable y).
        """
        # Consider all arcs (overlapping tuples of variables)
        if arcs == None:
            filtered = [arc for arc, overlap in self.crossword.overlaps.items() if overlap != None]
            queue = deque(filtered)
        else:
            queue = deque(arcs)
            
        # All arcs are given beforehand
        while len(queue) != 0:
            x, y = queue.popleft()

            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                
                    # Problem is impossible to solve
                    return False
                
                # Add neighboring arcs of x
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) != len(self.crossword.variables):
            return False
        
        for var in self.crossword.variables:
            if not isinstance(assignment[var], str):
                return False
        
        return True
        
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Correct length
        for var, word in assignment.items():
            if len(word) != var.length:
                return False
        
        # Correct distinct words -> (len of assignment must == len of words)
        distinct_words = set(assignment.values())
        if len(assignment) != len(distinct_words):
            return False
        
        # Conflicts beetween var neighbors
        for var1 in assignment:
            for var2 in self.crossword.neighbors(var1):
                if var2 not in assignment:
                    continue
                
                overlap1, overlap2 = self.crossword.overlaps[var1, var2]
                
                # There is only one word in each variable in this step
                letter1 = assignment[var1][overlap1]
                letter2 = assignment[var2][overlap2]
                if letter1 != letter2:
                    return False
        
        return True

    def order_domain_values(self, var, assignment):
        """     ~~~Least-Constraining Values~~~
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Each neighbors' `v` count for conflicted words with `var`
        counter = Counter()

        for word1 in self.domains[var]:
            for v in self.crossword.neighbors(var):
                if v in assignment:
                    continue

                words_neighbor = self.domains[v]
                overlap1, overlap2 = self.crossword.overlaps[var, v]

                # Takes letters and check for conflicts!!! to count in all neighbors
                for word2 in words_neighbor:
                    if word1[overlap1] != word2[overlap2]:
                        counter[word1] += 1
        
        domains = list(self.domains[var])
        
        return sorted(domains, key=lambda word: counter[word])

    def select_unassigned_variable(self, assignment):
        """     ~~~Minimum Remaining Value + Degree~~~
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        words_l = float("inf")
        var_list = list()
        
        for v in self.crossword.variables:
            if v in assignment:
                continue
            
            # Minimum Remaining Value heuristic - iteration
            domain_l = len(self.domains[v])
            if domain_l < words_l:
                words_l = domain_l
                var_list.clear()
                var_list.append(v)
            elif domain_l == words_l:
                var_list.append(v)
        
        # Degree heuristic - sorting
        return sorted(var_list, key=lambda var: len(self.crossword.neighbors(var)))[-1]
            
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        # Try a new variable - optimized with Minimum Remaining Value + Degree heuristics
        var = self.select_unassigned_variable(assignment)
        
        # Check for word - optimized with Least-Constraining Values heuristics
        for word in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            
            # Check correctness word in crossword
            if self.consistent(new_assignment):
                new_assignment[var] = word
                
                # Efficient inference after new_assignment
                if self.ac3():

                    # Recursive to find good assignment
                    result = self.backtrack(new_assignment)
                    if result is not None:
                        return result
                
                # Remove var and find next solution
                new_assignment.pop(var)
        
        return None
    
def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
    
