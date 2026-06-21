import pygame
from copy import deepcopy
from random import choice, randrange

#constant variables(line 3 to 6)
W, H = 10, 20
TILE = 45
GAME_RES =  W*TILE, H*TILE
RES = 750, 940
FPS = 60

pygame.init()
screen=pygame.display.set_mode(RES)
game_sc= pygame.Surface(GAME_RES)
clock=pygame.time.Clock()

#grid display
grid = [pygame.Rect(x*TILE, y*TILE, TILE, TILE) for x in range(W) for y in range (H)]

#figure positions
figure_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
    [(-1, 0), (-1, 0), (0, 0), (0, -1)],
    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, 0)]]

#this line takes the figures from the array figures we made
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1)for x, y in fig_pos]for fig_pos in figure_pos]
figure_rect = pygame.Rect(0, 0, TILE-2, TILE-2)
field = [[0 for i in range(W)] for j in range (H)]

#this part allows the figures to be in free fall
anim_count, anim_speed, anim_limit = 0,5,2000

#this parts allows to load the image in the game
home_background = pygame.image.load('bg_sakura.jpeg').convert()
game_background = pygame.image.load('bg_tokyo.jpeg').convert()

#this part creates the title page and text fonts for the game
main_font = pygame.font.Font('slkscre.ttf',65)
font = pygame.font.Font('slkscre.ttf',45)
title_tetris=main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))

#this parts puts color on the blocks
get_color = lambda: (randrange(30,256), randrange(30,256), randrange(30,256))
color = get_color()

#this allows you to get the next block you can use
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

#this part allows you to track your score
score, lines = 0, 0
scores = {0:0, 1:100, 2:300, 3:700, 4:1500}

#this function creates the bounds for the figures to stay in
def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

#main loop
while True:
    #dx allows the figures to be moved by its horizontal position
    dx, rotate = 0, False
    screen.blit(home_background,(0,0))
    screen.blit(game_sc,(20,20))
    game_sc.blit(game_background,(0,0))
    
    #delay for full lines
    for i in range(lines):
        pygame.time.wait(200)

    #control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        #controls the x direction
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                dx=-1
            elif event.key==pygame.K_RIGHT:
                dx=1
            #this part allows acceleration of the blocks
            elif event.key==pygame.K_DOWN:
                anim_limit = 100
            elif event.key==pygame.K_UP:
                rotate = True
    #moves the horizontal position
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    #movement for the vertical position
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break

    #rotating function
    center= figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    
    #check and clear filled lines
    line, lines = H - 1, 0
    for row in range(H -1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1 
        else:
            anim_speed += 3 
            lines += 1 
        
    #this part computes the scores
    score += scores[lines]

    #allows grid to be displayed
    [pygame.draw.rect(game_sc, (40,40,40), i_rect, 1) for i_rect in grid]

    #draws the figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color , figure_rect)
    
    #this part draws the field map
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)

    #draws the next block
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(screen, next_color , figure_rect)

    #this part draws the title
    screen.blit(title_tetris, (475, 10))
    screen.blit(title_score, (535,780))
    screen.blit(font.render(str(score),True, pygame.Color('white')), (550, 840))

    pygame.display.flip()
    clock.tick()