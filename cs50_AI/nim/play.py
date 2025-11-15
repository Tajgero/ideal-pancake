from nim import train, play
# import pygame, sys

ai = train(10000)
play(ai)

# pygame.init()
# W, H = 600, 500

# running = True
# screen = pygame.display.set_mode((W, H))
# font = pygame.font.SysFont(None, 60)
# clock = pygame.time.Clock()

# # Circle parameters
# radius = 30
# offset = radius * 2

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 running = False
    
#     # BACKGROUND
#     screen.fill("#413c4f")
    
#     # Piles
#     for row in range(5):
#         width = W // 2
#         height = H // 3 + offset * row
#         circle = pygame.draw.circle(screen, "white", (width,height), radius)
#         pygame.draw.circle(screen, "black", circle.center, radius, 4)
    
#     # Render display
#     pygame.display.flip()
#     dt = clock.tick(60) / 1000  # limits FPS to 60
                
# pygame.quit()
# sys.exit()
