
import pygame, os, random
pygame.init()

# GAME WINDOW -----------------------------------------------------------------------------------
WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Graveyard Maze')
FPS = 60
SHOW_MOUSECOORDS = False
BG_MUSIC_VOLUME = 0.3

# LEVEL PATHS -----------------------------------------------------------------------------------

PATH_INPUTS = [
    (10, 370, 80, 80),
    (80, 400, 120, 20),
    (200, 400, 20, 200),
    (200, 600, 200, 20),
    (400, 200, 20, 420),
    (400, 180, 800, 20),
    (1200, 180, 20, 100),
    (520, 280, 700, 20),
    (500, 280, 20, 200),
    (500, 480, 910, 20),
    (1410, 450, 80, 80)
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
START_TEXT = FONT_1.render("Move here to start!", 1, RED)
INSTRUCTION_TEXT = FONT_1.render("Stay on the path! Don't step on any graves!", 1, WHITE)
STEPPED_ON_TEXT = FONT_1.render('uuuuuurgh!  Stop stepping on us!', 1, WHITE)

# USER EVENTS ---------------------------------------------------------------------------------
LEFT_PATH = pygame.USEREVENT + 1
START_GAME = pygame.USEREVENT + 2

# SOUND EFFECTS --------------------------------------------------------------------------------
HIT_SOUND = pygame.mixer.Sound(os.path.join('sound/Sound_Effects', 'hit01.wav'))

# IMAGES ---------------------------------------------------------------------------------------
INTRO_BG_IMG = pygame.image.load(
    os.path.join('assets', 'intro.jpg'))
INTRO_BG = pygame.transform.scale(INTRO_BG_IMG, (WIDTH, HEIGHT))

# DRAWING -------------------------------------------------------------------------------------------
def draw_intro(level):
    BG = select_background(level)
    WIN.blit(BG, (0, 0))
    pygame.draw.rect(WIN, RED, PATH_RECTANGLES[0])
    WIN.blit(START_TEXT, (10, 340))

    if SHOW_MOUSECOORDS:
        coords = get_mousecoords()
        WIN.blit(coords, (10, 10))

    pygame.display.update()
    return

def draw_level(level):
    BG = select_background(level)
    WIN.blit(BG, (0, 0))
    if level == 0:
        WIN.blit(BG, (0, 0))
        pygame.draw.rect(WIN, RED, PATH_RECTANGLES[0])
        # WIN.blit(START_TEXT, (10, 340))
        WIN.blit(STEPPED_ON_TEXT, (500, 500))
    else:
        for rect in PATH_RECTANGLES:
            pygame.draw.rect(WIN, WHITE, rect)
        pygame.draw.rect(WIN, RED, PATH_RECTANGLES[0])
        pygame.draw.rect(WIN, RED, PATH_RECTANGLES[-1])
        # WIN.blit(START_TEXT, (10, 340))
        WIN.blit(INSTRUCTION_TEXT, (10, 40))

    if SHOW_MOUSECOORDS:
        coords = get_mousecoords()
        WIN.blit(coords, (10, 10))

    pygame.display.update()
    return

def play_bg_music():
    SONGS = [
        'Boneyard_waltz.ogg',
        'Crypt_loop.wav',
        'Ghost_waltz.ogg',
        'intro.mp3',
        'Paranoid_piano.ogg'
    ]
    bg_music = random.choice(SONGS)
    pygame.mixer.music.load(os.path.join('sound/BG_Music', bg_music))
    pygame.mixer.music.set_volume(BG_MUSIC_VOLUME)
    pygame.mixer.music.play(1)
    return


def get_mousecoords():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return FONT_1.render(f'Mouse Position = {mouse_x}, {mouse_y}', 1, WHITE)

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

def check_start():
    mouse = pygame.mouse.get_pos()
    rect = PATH_RECTANGLES[0]
    if rect.collidepoint(mouse):
        pygame.event.post(pygame.event.Event(START_GAME))
    return


def select_background(level):
    bgs_by_level = {
        -1: 'intro.jpg',
        0: 'graveyard_hand.jpg',
        1: 'graveyard3.jpg'
    }
    bg = pygame.image.load(
        os.path.join('assets', bgs_by_level[level]))
    bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    return bg_scaled


# MAIN LOOP -------------------------------------------------------------------------------------------
def main():
    clock = pygame.time.Clock()
    run = True
    level = -1
    select_background(level)
    play_bg_music()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == LEFT_PATH:
                print('BRRRRRRR')
                pygame.mixer.Sound.play(HIT_SOUND)  # todo hit sound doesn't work
                level = 0
            if event.type == START_GAME:
                if level == -1:
                    level += 2
                else:
                    level += 1
        if level == -1:
            draw_intro(level)
            check_start()
        if level == 0:
            draw_level(level)
            check_start()
        if level == 1:
            check_collision()
            draw_level(level)

if __name__ == '__main__':
    main()