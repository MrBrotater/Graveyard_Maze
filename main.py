
import pygame
import os
import random
pygame.init()

# GAME WINDOW -----------------------------------------------------------------------------------
WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Graveyard Maze')
FPS = 15
SHOW_MOUSECOORDS = False
BG_MUSIC_VOLUME = 0.1

# COLORS --------------------------------------------------------------------------------------
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# TEXT ----------------------------------------------------------------------------------------
FONT_1 = pygame.font.SysFont('comicsans', int(HEIGHT/25))
FONT_2 = pygame.font.SysFont('comicsans', int(HEIGHT/15))
START_TEXT = FONT_1.render("START", True, RED)
INTRO_TXT = FONT_2.render("Enter the graveyard and stay on the path!", True, WHITE)
ZOMBIE_TEXTS = [
    'Uuuuuuuuurgh!  Get off me!',
    'Brains!!!!',
    "Be more careful!  I'm trying to rest!",
    'How rude...',
    'Fresh meat!!!!',
    'You hear fingernails scraping wood from below',
    'You hear a muffled moan'
]

STEPPED_ON_TEXTS = [FONT_2.render(x, True, WHITE) for x in ZOMBIE_TEXTS]

# USER EVENTS ---------------------------------------------------------------------------------
LEFT_PATH = pygame.USEREVENT + 1
START_GAME = pygame.USEREVENT + 2
NEXT_LEVEL = pygame.USEREVENT + 3

# BACKGROUND MUSIC -----------------------------------------------------------------------------

# SOUND EFFECTS --------------------------------------------------------------------------------
ZOMBIE_FILES = [file for file in os.listdir('sound/Sound_Effects')]
ZOMBIE_SOUNDS = [pygame.mixer.Sound(os.path.join('sound/Sound_Effects', x)) for x in ZOMBIE_FILES]
for sound in ZOMBIE_SOUNDS:
    sound.set_volume(BG_MUSIC_VOLUME)

WIN_SOUND = pygame.mixer.Sound(os.path.join('sound/Sound_Effects', 'win.ogg'))
WIN_SOUND.set_volume(1)


# LEVEL PATHS -----------------------------------------------------------------------------------
def get_level_rectangles(level):
    level_definitions = {
        1: [
            (10, 370, 80, 80),
            (80, 390, 1330, 40),
            (1410, 370, 80, 80)],
        2: [
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
            (1410, 450, 80, 80)],
        3: [
            (10, 370, 80, 80),
            (80, 400, 120, 20),
            (200, 400, 20, 120),
            (200, 520, 150, 20),
            (350, 525, 50, 10),
            (400, 520, 150, 20),
            (550, 200, 20, 340),
            (550, 180, 150, 20),
            (700, 185, 150, 10),
            (850, 180, 100, 20),
            (950, 180, 20, 50),
            (950, 230, 50, 20),
            (1000, 235, 100, 10),
            (1100, 200, 80, 80)],
        4: []
    }

    rectangles = []

    for x in level_definitions[level]:
        path_leg = pygame.Rect(x[0], x[1], x[2], x[3])
        rectangles.append(path_leg)
    return rectangles


# DRAWING -------------------------------------------------------------------------------------------
def draw_level(true_level, display_level, rectangles, ztext):
    bg = select_background(display_level)
    WIN.blit(bg, (0, 0))

    if display_level == -1:
        pygame.draw.rect(WIN, RED, rectangles[0])
        WIN.blit(START_TEXT, (10, 340))
        WIN.blit(INTRO_TXT, (WIDTH / 2 - INTRO_TXT.get_width() / 2, HEIGHT / 2 - INTRO_TXT.get_width() / 2))
    elif display_level == 0:
        pygame.draw.rect(WIN, RED, rectangles[0])
        WIN.blit(ztext, (WIDTH / 2 - ztext.get_width() / 2, HEIGHT / 2 - ztext.get_height() / 2))
    elif display_level == 'buffer':
        pygame.draw.rect(WIN, RED, rectangles[0])
        WIN.blit(START_TEXT, (10, 340))
        level_text = FONT_2.render(f"LEVEL {true_level+1}", True, WHITE)
        WIN.blit(level_text, (WIDTH/2 - level_text.get_width()/2, HEIGHT/2 - level_text.get_height()/2))
    else:
        level_text = FONT_2.render(f"LEVEL {display_level}", True, WHITE)
        WIN.blit(level_text, (1490 - level_text.get_width(), 10))
        for rect in rectangles:
            pygame.draw.rect(WIN, WHITE, rect)
        pygame.draw.rect(WIN, RED, rectangles[0])
        pygame.draw.rect(WIN, RED, rectangles[-1])

    if SHOW_MOUSECOORDS:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coords = FONT_1.render(f'Mouse Position = {mouse_x}, {mouse_y}', True, WHITE)
        WIN.blit(coords, (10, 10))

    pygame.display.update()
    return


# SELECT BACKGROUND IMG -------------------------------------------------------------------
def select_background(level):
    bgs_by_level = {
        -1: 'intro.jpg',
        0: 'graveyard_hand.jpg',
        1: 'graveyard1.jpg',
        2: 'graveyard2.jpg',
        3: 'graveyard3.jpg',
        4: 'win.jpg',
        'buffer': 'intro.jpg'
    }
    bg = pygame.image.load(
        os.path.join('assets', bgs_by_level[level]))
    bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    return bg_scaled


# SELECT BACKGROUND MUSIC ---------------------------------------------------------------------------
def play_bg_music():
    songs = [
        'Boneyard_waltz.ogg',
        'Crypt_loop.wav',
        'Ghost_waltz.ogg',
        'intro.mp3',
        'Paranoid_piano.ogg'
    ]
    bg_music = random.choice(songs)
    pygame.mixer.music.load(os.path.join('sound/BG_Music', bg_music))
    pygame.mixer.music.set_volume(BG_MUSIC_VOLUME)
    pygame.mixer.music.play(loops=1)
    return


# CHECK COLLISION -----------------------------------------------------------------------------------
def check_collision(level, switch, rectangles):
    mouse = pygame.mouse.get_pos()
    if level == 'buffer' or level <= 0:
        if switch:
            rect = rectangles[0]
            if rect.collidepoint(mouse):
                pygame.event.post(pygame.event.Event(START_GAME))
    else:
        rect = rectangles[-1]
        if rect.collidepoint(mouse):
            pygame.event.post(pygame.event.Event(NEXT_LEVEL))
            return
        safe = False
        for rect in rectangles:
            if rect.collidepoint(mouse):
                safe = True
        if not safe:
            pygame.event.post(pygame.event.Event(LEFT_PATH))
    return


# MAIN LOOP -------------------------------------------------------------------------------------------
def main():
    clock = pygame.time.Clock()
    run = True
    start_switch = True
    true_level = -1
    display_level = true_level
    rectangles = get_level_rectangles(1)
    select_background(true_level)
    play_bg_music()
    ztext = STEPPED_ON_TEXTS[0]

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == LEFT_PATH:
                pygame.mixer.Sound.play(random.choice(ZOMBIE_SOUNDS))
                true_level = 0
                display_level = 0
                start_switch = True
                ztext = random.choice(STEPPED_ON_TEXTS)
            if event.type == START_GAME:
                start_switch = False
                if true_level == -1:
                    true_level += 2
                    rectangles = get_level_rectangles(true_level)
                else:
                    true_level += 1
                    rectangles = get_level_rectangles(true_level)
                display_level = true_level
            if event.type == NEXT_LEVEL:
                display_level = 'buffer'
                start_switch = True
                play_bg_music()
                if true_level == 3:
                    true_level += 1
                    run = False
        if run:
            draw_level(true_level, display_level, rectangles, ztext)
            check_collision(display_level, start_switch, rectangles)

    WIN.blit(select_background(true_level), (0, 0))
    pygame.display.update()
    pygame.mixer.Sound.play(WIN_SOUND)
    pygame.time.delay(3000)
    main()
    return


if __name__ == '__main__':
    main()
