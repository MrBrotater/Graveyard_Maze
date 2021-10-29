
import pygame
pygame.init()

# GAME WINDOW -----------------------------------------------------------------------------------
WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Graveyard Maze Editor')
FPS = 60
SHOW_MOUSECOORDS = True

# COLORS --------------------------------------------------------------------------------------
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# TEXT ----------------------------------------------------------------------------------------
FONT_1 = pygame.font.SysFont('comicsans', int(HEIGHT/25))

# LEVEL PATHS -----------------------------------------------------------------------------------
def get_level_rectangles(level):
    level_definitions = {
        1: [
            (10, 370, 80, 80),
            (80, 390, 1330, 40),
            (1410, 370, 80, 80)
        ]
    }

    rectangles = []

    for x in level_definitions[level]:
        path_leg = pygame.Rect(x[0], x[1], x[2], x[3])
        rectangles.append(path_leg)
    return rectangles






# DRAWING -------------------------------------------------------------------------------------------
def draw_level(rectangles):
    WIN.fill([0, 0, 0])
    for rect in rectangles:
        pygame.draw.rect(WIN, WHITE, rect)

    if SHOW_MOUSECOORDS:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coords = FONT_1.render(f'Mouse Position = {mouse_x}, {mouse_y}', 1, WHITE)
        WIN.blit(coords, (10, 10))

    pygame.display.update()
    return





# MAIN LOOP -------------------------------------------------------------------------------------------
def main():
    clock = pygame.time.Clock()
    run = True
    rectangles = get_level_rectangles(1)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        draw_level(rectangles)
    return


if __name__ == '__main__':
    main()