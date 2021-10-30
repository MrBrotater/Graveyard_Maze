
import pygame
import os
import random
pygame.init()

# GAME WINDOW -----------------------------------------------------------------------------------
WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Graveyard Maze')
FPS = 15
BG_MUSIC_VOLUME = 0.1
GHOST_SIZE = 125

# COLORS --------------------------------------------------------------------------------------
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# TEXT ----------------------------------------------------------------------------------------
FONT_1 = pygame.font.SysFont('comicsans', int(HEIGHT/25))
FONT_2 = pygame.font.SysFont('comicsans', int(HEIGHT/15))
START_TEXT = FONT_1.render("START", True, RED)
INTRO_TXT = FONT_1.render("Enter the graveyard and stay on the path!", True, WHITE)
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
START_LEVEL = pygame.USEREVENT + 1
LEFT_PATH = pygame.USEREVENT + 2
GHOSTED = pygame.USEREVENT + 3
NEXT_LEVEL = pygame.USEREVENT + 4
WINNER = pygame.USEREVENT + 5

# BACKGROUND IMAGES -----------------------------------------------------------------------------
BG_IMAGES = {
    'Intro': pygame.image.load(os.path.join('assets', 'intro.jpg')),
    'Buffer': pygame.image.load(os.path.join('assets', 'intro.jpg')),
    'Winner': pygame.image.load(os.path.join('assets', 'win.jpg')),
    'Ghosted': pygame.image.load(os.path.join('assets', 'ghosted.jpg')),
    'Zombie': pygame.image.load(os.path.join('assets', 'graveyard_hand.jpg')),
    1: pygame.image.load(os.path.join('assets', 'graveyard1.jpg')),
    2: pygame.image.load(os.path.join('assets', 'graveyard2.jpg')),
    3: pygame.image.load(os.path.join('assets', 'graveyard3.jpg'))
}

BG_IMAGES_SCALED = {
    'Intro': pygame.transform.scale(BG_IMAGES['Intro'], (WIDTH, HEIGHT)),
    'Buffer': pygame.transform.scale(BG_IMAGES['Buffer'], (WIDTH, HEIGHT)),
    'Winner': pygame.transform.scale(BG_IMAGES['Winner'], (WIDTH, HEIGHT)),
    'Ghosted': pygame.transform.scale(BG_IMAGES['Ghosted'], (WIDTH, HEIGHT)),
    'Zombie': pygame.transform.scale(BG_IMAGES['Zombie'], (WIDTH, HEIGHT)),
    1: pygame.transform.scale(BG_IMAGES[1], (WIDTH, HEIGHT)),
    2: pygame.transform.scale(BG_IMAGES[2], (WIDTH, HEIGHT)),
    3: pygame.transform.scale(BG_IMAGES[3], (WIDTH, HEIGHT))
}

# SOUND EFFECTS --------------------------------------------------------------------------------
ZOMBIE_FILES = ['zombie-1.wav', 'zombie-2.wav', 'zombie-3.wav', 'zombie-4.wav']
ZOMBIE_SOUNDS = [pygame.mixer.Sound(os.path.join('sound', 'Sound_Effects', x)) for x in ZOMBIE_FILES]
for sound in ZOMBIE_SOUNDS:
    sound.set_volume(BG_MUSIC_VOLUME)

GHOST_LAUGH = pygame.mixer.Sound(os.path.join('sound', 'Sound_Effects', 'laugh-evil-1.ogg'))

WIN_SOUND = pygame.mixer.Sound(os.path.join('sound', 'Sound_Effects', 'win.ogg'))
WIN_SOUND.set_volume(1)

# GHOST FRAME IMAGES --------------------------------------------------------------------------------
GHOST_FILES = os.listdir(os.path.join('assets', 'animated ghost'))
GHOST_FRAMES = [pygame.image.load(os.path.join('assets', 'animated ghost', file)) for file in GHOST_FILES]


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

    rectangles = [pygame.Rect(x[0], x[1], x[2], x[3]) for x in level_definitions[level]]

    return rectangles


# GHOST ---------------------------------------------------------------------------------------------
class Ghost(pygame.sprite.Sprite):

    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        level_x = {
            1: 750,
            2: 500,
            3: 1000
        }
        level_y = {
            1: 200,
            2: 600,
            3: 200
        }
        level_speed = {
            1: 3,
            2: 1,
            3: 2
        }

        self.rect = pygame.Rect(level_x[level], level_y[level], GHOST_SIZE, GHOST_SIZE)
        self.frame = 0
        self.image = pygame.transform.scale(GHOST_FRAMES[self.frame], self.rect.size)
        self.speed = level_speed[level]

    def update(self):
        target_x, target_y = pygame.mouse.get_pos()
        ghost_x, ghost_y = self.rect.centerx, self.rect.centery

        if target_x > ghost_x:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        if target_y > ghost_y:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed

        self.frame += 1
        if self.frame > 12:
            self.frame = 0

        self.image = pygame.transform.scale(GHOST_FRAMES[self.frame], (GHOST_SIZE, GHOST_SIZE))
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update()


# DRAWING -------------------------------------------------------------------------------------------
def draw_intro():
    WIN.blit(BG_IMAGES_SCALED['Intro'], (0, 0))
    start_rect = pygame.Rect((10, 370, 80, 80))
    pygame.draw.rect(WIN, RED, start_rect)
    WIN.blit(START_TEXT, (10, 310))
    WIN.blit(INTRO_TXT, (WIDTH / 2 - INTRO_TXT.get_width() / 2, HEIGHT / 2 - INTRO_TXT.get_width() / 2))
    pygame.display.update()
    return


def draw_level(level, rectangles):
    WIN.blit(BG_IMAGES_SCALED[level], (0, 0))
    level_text = FONT_2.render(f"LEVEL {level}", True, WHITE)
    WIN.blit(level_text, (1490 - level_text.get_width(), 10))
    for rect in rectangles:
        pygame.draw.rect(WIN, WHITE, rect)
    pygame.draw.rect(WIN, RED, rectangles[0])
    pygame.draw.rect(WIN, RED, rectangles[-1])
    pygame.display.update()
    return


def draw_left_path(ztext):
    WIN.blit(BG_IMAGES_SCALED['Zombie'], (0, 0))
    start_rect = pygame.Rect((10, 370, 80, 80))
    pygame.draw.rect(WIN, RED, start_rect)
    WIN.blit(ztext, (WIDTH / 2 - ztext.get_width() / 2, HEIGHT / 2 - ztext.get_height() / 2))
    pygame.display.update()
    return


def draw_ghosted():
    WIN.blit(BG_IMAGES_SCALED['Ghosted'], (0, 0))
    start_rect = pygame.Rect((10, 370, 80, 80))
    pygame.draw.rect(WIN, RED, start_rect)
    pygame.display.update()
    return


def draw_buffer(level):
    WIN.blit(BG_IMAGES_SCALED['Buffer'], (0, 0))
    start_rect = pygame.Rect((10, 370, 80, 80))
    pygame.draw.rect(WIN, RED, start_rect)
    level_text = FONT_2.render(f"LEVEL {level}", True, WHITE)
    WIN.blit(level_text, (WIDTH / 2 - level_text.get_width() / 2, HEIGHT / 2 - level_text.get_height() / 2))
    pygame.display.update()
    return


def draw_winner():
    WIN.blit(BG_IMAGES_SCALED['Winner'], (0, 0))
    pygame.display.update()
    return


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
def check_collision_start():
    start_rect = pygame.Rect((10, 370, 80, 80))
    mouse = pygame.mouse.get_pos()
    if start_rect.collidepoint(mouse):
        pygame.event.post(pygame.event.Event(START_LEVEL))
    return


def check_collision_next_level(level, rectangles):
    end_rect = rectangles[-1]
    mouse = pygame.mouse.get_pos()
    if end_rect.collidepoint(mouse):
        if level == 3:
            pygame.event.post(pygame.event.Event(WINNER))
        else:
            pygame.event.post(pygame.event.Event(NEXT_LEVEL))
    return


def check_collision(rectangles):
    mouse = pygame.mouse.get_pos()

    safe = False
    for rect in rectangles:
        if rect.collidepoint(mouse):
            safe = True
    if not safe:
        pygame.event.post(pygame.event.Event(LEFT_PATH))
    return


def check_collision_ghost(ghost):
    mouse = pygame.mouse.get_pos()
    ghost_rect = ghost.rect
    if ghost_rect.collidepoint(mouse):
        pygame.event.post(pygame.event.Event(GHOSTED))
    return


# MAIN LOOP -------------------------------------------------------------------------------------------
def main():
    clock = pygame.time.Clock()
    run = True
    level = 1
    game_state = 'Intro'
    play_bg_music()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == START_LEVEL:
                ghost = Ghost(level)
                rectangles = get_level_rectangles(level)
                game_state = 'Level'

            if event.type == LEFT_PATH:
                game_state = 'Zombie'
                pygame.mixer.Sound.play(random.choice(ZOMBIE_SOUNDS))
                ztext = random.choice(STEPPED_ON_TEXTS)

            if event.type == GHOSTED:
                game_state = 'Ghosted'
                pygame.mixer.Sound.play(GHOST_LAUGH)

            if event.type == NEXT_LEVEL:
                level += 1
                game_state = 'Buffer'
                play_bg_music()

            if event.type == WINNER:
                game_state = 'Won'
                draw_winner()
                pygame.mixer.Sound.play(WIN_SOUND)
                pygame.time.delay(3000)
                run = False

        if game_state == 'Intro':
            draw_intro()
            check_collision_start()

        if game_state == 'Zombie':
            draw_left_path(ztext)
            check_collision_start()

        if game_state == 'Ghosted':
            draw_ghosted()
            check_collision_start()

        if game_state == 'Buffer':
            draw_buffer(level)
            check_collision_start()

        if game_state == 'Level':
            draw_level(level, rectangles)
            check_collision(rectangles)
            check_collision_next_level(level, rectangles)
            ghost.update()
            check_collision_ghost(ghost)

    main()
    return


if __name__ == '__main__':
    main()
