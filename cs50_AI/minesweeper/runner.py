import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 8
WIDTH = 8
MINES = 8

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (97, 97, 97)
WHITE = (255, 255, 255)

# Create game
pygame.init()
size = width, height = 1000, 700
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
resizer = height / 400
smallerFont = pygame.font.Font(OPEN_SANS, int(8 * resizer))
smallFont = pygame.font.Font(OPEN_SANS, int(20 * resizer))
mediumFont = pygame.font.Font(OPEN_SANS, int(28 * resizer))
largeFont = pygame.font.Font(OPEN_SANS, int(40 * resizer))

# Sounds
enable_boom_sound = True
mine_sound = pygame.mixer.Sound("assets/audio/boom.mp3")
mine_sound.set_volume(0.05) # x*100 % volume

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False
clicked_matrix = [[False for height in range(WIDTH)] for width in range(HEIGHT)]

# Show instructions initially
instructions = True
show_indexes = False

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # Show game instructions
    if instructions:

        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50 * resizer)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Mark all mines successfully to win!"
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i * resizer)
            screen.blit(line, lineRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, DARK_GRAY if clicked_matrix[i][j] else GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, width=3)

            # Shows indexes on board
            if show_indexes:
                currentCellText = smallerFont.render(f"({i},{j})", True, BLACK)
                currentCellRect = currentCellText.get_rect()
                currentCellRect.midbottom = rect.midbottom
                screen.blit(currentCellText, currentCellRect)

            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and lost:
                screen.blit(mine, rect)
                mine_sound.play() if enable_boom_sound else None
                enable_boom_sound = False
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                clicked_matrix[i][j] = True
                neighbors = smallFont.render(
                    str(game.nearby_mines((i, j))),
                    True, BLACK
                )
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)
                
            row.append(rect)
        cells.append(row)

    # AI Move button
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50 * resizer
    )
    buttonText = mediumFont.render("AI Move", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiButton.center
    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(buttonText, buttonRect)

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, aiButton.bottom + 20,
        (width / 3) - BOARD_PADDING * 2, 50 * resizer
    )
    buttonText = mediumFont.render("Reset", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)

    # Show cells index button
    cellsIndexButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING,
        (width / 3) - BOARD_PADDING * 2, 35 * resizer
    )
    buttonText = smallFont.render("Show cell index", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = cellsIndexButton.center
    pygame.draw.rect(screen, WHITE, cellsIndexButton)
    screen.blit(buttonText, buttonRect)

    # Display text
    text = "Lost" if lost else "Won" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height)
    screen.blit(text, textRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    # Check for a right-click to toggle flagging
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # If AI button clicked, make an AI move
        if aiButton.collidepoint(mouse) and not lost:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        # Reset game state
        elif resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            enable_boom_sound = True
            clicked_matrix = [[False for height in range(WIDTH)] for width in range(HEIGHT)]
            continue

        # Prints cell indexes
        elif cellsIndexButton.collidepoint(mouse):
            show_indexes = not show_indexes
            time.sleep(0.2)

        # User-made move
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    # Make move and update AI knowledge
    if move:
        if game.is_mine(move):
            lost = True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)

    pygame.display.flip()
