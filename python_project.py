import pygame
#constant variables(line 3 to 6)
W, H = 10, 20
TILE = 45
GAME_RES =  W*TILE, H*TILE
FPS=60

pygame.init()
game_sc= pygame.display.set_mode(GAME_RES)
clock=pygame.time.Clock()

#grid display
grid = [pygame.Rect(x*TILE, y*TILE, TILE, TILE) for x in range(W) for y in range (H)]

#figure positions
figure_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
    [(0, -1), (-1, -1), (-1, 0), (0, 1)],
    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
    [(0, 0), (0, 1), (0, 1), (1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, 0)]]

#this line takes the figures from the array figures we made
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1)for x, y in fig_pos]for fig_pos in figure_pos]
figure_rect = pygame.Rect(0, 0, TILE-2, TILE-2)
figure = figures[0]

#main loop
while True:
    #dx allows the figures to be moved by its horizontal position
    dx = 0
    game_sc.fill(pygame.Color('black'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        #controls the x direction
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                dx=-1
            elif event.key==pygame.K_RIGHT:
                dx=1
    for i in range(4):
        figure[i].x += dx
    #allows grid to be displayed
    [pygame.draw.rect(game_sc, (40,40,40), i_rect, 1) for i_rect in grid]

    #draws the figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc,pygame.Color('white'), figure_rect)

    pygame.display.flip()
    clock.tick()