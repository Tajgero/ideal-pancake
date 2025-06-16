from sys import exit
import pygame, time, json
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

def preprocess(path: list, n=64) -> list:
    xy = np.array([p[0] for p in path]).astype("float32") # (x, y) without time
    xy -= xy.mean(axis=0)               # Centrowanie
    xy /= xy.max()                      # Skalowanie [-1, 1]
    idx = np.linspace(0, len(xy) - 1, n).astype(int)
    return xy[idx]

# Load pattern like symbols
with open('template_square.json', 'r') as f:
    template_square = json.load(f)[0]
with open('template_triangle.json', 'r') as f:
    template_triangle = json.load(f)[0]
with open('template_circle.json', 'r') as f:
    template_circle = json.load(f)

templates = {'square' : preprocess(template_square),
              'triangle' : preprocess(template_triangle),
              'circle' : preprocess(template_circle)}

def classify_dtw(points):
    test = preprocess(points)
    best, best_cost = None, float('inf')
    for name, ref in templates.items():
        dist, _ = fastdtw(test, ref, dist=euclidean)
        if dist < best_cost:
            best, best_cost = name, dist
            
    # Return name if treshold under this number
    return best if best_cost < 20 else None # 20 = próg empiryczny


# =============================================================================
#                           GAME
# =============================================================================
pygame.init()
W, H = 500, 700

screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

drawing, points, gesture = False, list(), list()
recognized_shape = None
display_until = 0
clear_screen = False

while True:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            
            # For making files with gestures
            # if gesture:
            #     with open("template.json", "w") as f:
            #         dump = json.dumps(gesture)
            #         f.write(dump)
                    
            pygame.quit()
            exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing, points = True, [(event.pos, time.time())]
            clear_screen = False
            
        if event.type == pygame.MOUSEMOTION and drawing:
            points.append((event.pos, time.time()))
            pygame.draw.circle(screen, "white", event.pos, radius=5)
            
        elif event.type == pygame.MOUSEBUTTONUP:
            clear_screen = True
            drawing = False
            gesture = points

            recognized_shape = classify_dtw(points)

            points = list() # Reset
            
            display_until = time.time() + 3 # 3 seconds cooldown
            
            
    if time.time() > display_until and clear_screen:
        screen.fill("black")
    
    # Will display title with recognized shape
    if recognized_shape and time.time() < display_until:
        text = font.render(f"Identified: {recognized_shape}", True, "white")
        rect = text.get_rect(center=(W / 2, H - 25))
        screen.blit(text, rect)
    
    pygame.display.flip()
    clock.tick(60)
