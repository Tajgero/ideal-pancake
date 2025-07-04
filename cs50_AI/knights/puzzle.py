from logic import *

# Characters A, B, C which could be Knight or Knave
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# =============================================================================
# # Puzzle 0
# =============================================================================
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),        # Only Knight or Knave could character be
    Not(And(AKnight, AKnave)),  # But not both of them could character be
    
    # Implication(AKnight, And(AKnight, AKnave)),     # Knight only tells truth statement
    # Implication(AKnave, Not(And(AKnight, AKnave)))  # Knave only tells lie statement
    Biconditional(AKnight, And(AKnight, AKnave))    # Knight and only Knight is telling truth !!!
)
# print(knowledge0.formula())

# =============================================================================
# # Puzzle 1
# =============================================================================
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),        # Only Knight or Knave could character be
    Not(And(AKnight, AKnave)),  # But not both of them could character be
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    
    Biconditional(AKnight, And( # AKnight says is a Knave and B is a Knave
        AKnave, 
        BKnave)
    ) 
)

# =============================================================================
# # Puzzle 2
# =============================================================================
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),        # Only Knight or Knave could character be
    Not(And(AKnight, AKnave)),  # But not both of them could character be
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    
    Biconditional(AKnight, Or(  # AKnight says A,B are Knights or A,B are Knaves
        And(AKnight, BKnight), 
        And(AKnave, BKnave)
    )),
    
    Biconditional(BKnight, Or(  # BKnight says A,B are Knight and Knave or A,B are Knave and Knight
        And(AKnight, BKnave), 
        And(AKnave, BKnight)
    ))
)

# =============================================================================
# # Puzzle 3
# =============================================================================
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),        # Only Knight or Knave could character be
    Not(And(AKnight, AKnave)),  # But not both of them could character be
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    
    Biconditional(AKnight, Or(  # AKnight says is a Knight or Knave
        AKnight,
        AKnave
    )),
    
    Biconditional(BKnight,      # BKnight says that AKnight says is a Knave
        Biconditional(AKnight, AKnave)
    ),
    
    Biconditional(BKnight,      # BKnight says CKnave
        CKnave
    ),
    
    Biconditional(CKnight,      # CKnight says AKnight
        AKnight
    )
)

# =============================================================================
#   MAIN
# =============================================================================
def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
