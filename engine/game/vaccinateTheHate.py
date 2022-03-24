import pygame
import pygame_menu

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_f,
    K_d
)


import random

from time import sleep

data_root = "engine/data/game"

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


pygame.init()


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 600)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 2000)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Init Mixer
pygame.mixer.init()
pygame.mixer.music.load(f"{data_root}/sounds/E2-new.ogg")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.9)


move_up_sound = pygame.mixer.Sound(f"{data_root}/sounds/highend.ogg")
move_down_sound = pygame.mixer.Sound(f"{data_root}/sounds/lowend.ogg")
collission_sound = pygame.mixer.Sound(f"{data_root}/sounds/injectionSnd.ogg")
afd_hits_you_sound = pygame.mixer.Sound(f"{data_root}/sounds/explosion.wav")


move_up_sound.set_volume(0.1)
move_down_sound.set_volume(0.1)
collission_sound.set_volume(0.9)
afd_hits_you_sound.set_volume(1.0)

# Start state


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(f"{data_root}/images/faust.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -3)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 3)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-3, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(3, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(bullet, self).__init__()
        self.surf = pygame.image.load(f"{data_root}/images/vaccine.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -3)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 3)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-3, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(3, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if pressed_keys[K_f]:
            self.rect.move_ip(5, 0)
            self.speed = 5


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(f"{data_root}/images/AFD.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(
            random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
            random.randint(0, SCREEN_HEIGHT),
        )
        )
        self.speed = random.randint(0, 3)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(f"{data_root}/images/hildmann.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+10, SCREEN_WIDTH + 80),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()


# Create Game Objects
player = Player()
bullet = bullet()
enemies = pygame.sprite.Group()
cloud = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(bullet)

start = 'waiting'


def start_the_game():
    global start
    print("Start the game")
    start = 'game'
    menu.disable()


def end_the_game():
    global start
    print("End the game")
    start = 'waiting'
    menu.enable()


# Init Menu
menu = pygame_menu.Menu(
    height=300,
    width=400,
    title='VACCINATE THE HATEVIRUS',
    theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name: ', default='Drosten')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)


def menu_func(events):

    if menu.is_enabled():
        menu.update(events)

    if menu.is_enabled():
        menu.draw(screen)


def game_loop(events):

    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                end_the_game()
        elif event.type == QUIT:
            end_the_game()
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            cloud.add(new_cloud)
            all_sprites.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    enemies.update()
    cloud.update()

    bullet.update(pressed_keys)

    screen.fill((255, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_down_sound.stop()
        move_up_sound.stop()
        pygame.mixer.music.stop()
        pygame.time.delay(50)
        afd_hits_you_sound.play()
        pygame.time.delay(500)

        end_the_game()

    for enemy in enemies:
        if pygame.sprite.spritecollideany(bullet, enemies):
            collission_sound.play()
            enemy.kill()


def mainloop():
    global start

    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if start == 'waiting':
            print('waiting')
            menu_func(events)

        elif start == 'game':
            print('game')
            game_loop(events)

        pygame.display.update()
        clock.tick(200)

    pygame.mixer.quit()
    print('finish')


if __name__ == '__main__':
    mainloop()
