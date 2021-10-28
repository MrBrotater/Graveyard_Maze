
import pygame, os
pygame.init()

# GAME WINDOW -----------------------------------------------------------------------------------
WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Graveyard Maze')
FPS = 60

# LEVEL PATHS -----------------------------------------------------------------------------------
# ((x,y), (a, b))
#   x, y = coords of top left point
#   a, b = width, height of the branch

PATH_INPUTS = [
    (0, 370, 80, 80),
    (80, 400, 120, 20),      # top left coords = 200, 400
    (200, 400, 20, 200),    # top left coords = 200, 600
    (200, 600, 200, 20),    # top left coords = 400, 600
    (400, 200, 20, 420)
]

PATH_RECTANGLES = []

for x in PATH_INPUTS:
    path_leg = pygame.Rect(x[0], x[1], x[2], x[3])
    PATH_RECTANGLES.append(path_leg)

# COLORS --------------------------------------------------------------------------------------
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# TEXT ----------------------------------------------------------------------------------------
FONT_1 = pygame.font.SysFont('comicsans', 25)
START_TEXT = FONT_1.render("Click Here to Start", 1, RED)


# USER EVENTS ---------------------------------------------------------------------------------
LEFT_PATH = pygame.USEREVENT + 1
START_GAME = pygame.USEREVENT + 2

# BACKGROUND MUSIC ----------------------------------------------------------------------------
MUSIC = True
if MUSIC:
    pygame.mixer.music.load(os.path.join('sound', 'Bone Yard Waltz - Loopable.ogg'))
    pygame.mixer.music.play(-1, 0.0)
    # JUMP_SCARE_SOUND = pygame.mixer.Sound(os.path.join('sound', 'jump_scare.mp3'))

# SOUND EFFECTS --------------------------------------------------------------------------------
HIT_SOUND = pygame.mixer.Sound(os.path.join('sound', 'hit01.wav'))

# IMAGES ---------------------------------------------------------------------------------------
INTRO_BG_IMG = pygame.image.load(
    os.path.join('assets', 'intro.jpg'))
INTRO_BG = pygame.transform.scale(INTRO_BG_IMG, (WIDTH, HEIGHT))

# DRAWING -------------------------------------------------------------------------------------------
def draw_window():
    WIN.blit(INTRO_BG, (0, 0))
    for rect in PATH_RECTANGLES:
        pygame.draw.rect(WIN, WHITE, rect)
    pygame.draw.rect(WIN, RED, PATH_RECTANGLES[0])
    pygame.draw.rect(WIN, RED, PATH_RECTANGLES[-1])
    WIN.blit(START_TEXT, (10, 340))

    pygame.display.update()

# CHECK COLLISION -----------------------------------------------------------------------------------
def check_collision():
    mouse = pygame.mouse.get_pos()
    safe = False
    for rect in PATH_RECTANGLES:
        if rect.collidepoint(mouse):
            safe = True
    if not safe:
        pygame.event.post(pygame.event.Event(LEFT_PATH))
    return safe



# MAIN LOOP -------------------------------------------------------------------------------------------
def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == LEFT_PATH:
                print('BRRRRRRR')
        draw_window()
        check_collision()

if __name__ == '__main__':
    main()