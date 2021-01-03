import pygame
import os
import sys
from main import FPS


def load_image(name, dir, colorkey=None):
    fullname = os.path.join(dir, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, group, sheet, columns, rows, x, y, begin_frame_num=0):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.change_frame(begin_frame_num)
        self.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def move(self, x, y, frame_num=None):
        self.rect = self.rect.move(int(x) - self.rect.x, int(y) - self.rect.y)
        if frame_num is not None:
            self.change_frame(frame_num)

    def change_frame(self, frame_num):
        self.image = self.frames[frame_num]


class OverWeighter:
    DIR = 'animation'
    IMG_NAME = 'HighWeigher.png'
    ANIM_DESC = {'stand': 0, 'move_left': 1, 'move_down': 2, 'move_up': 3, 'move_right': 4}
    V = 100
    G = V * 3

    def __init__(self, group, coords):
        self.coords = list(coords)
        self.group = group
        self.sprite = AnimatedSprite(group,
                                     load_image(self.IMG_NAME, self.DIR),
                                     5, 1,
                                     *coords, 4)
        self.vertical_vel = 0

    def update(self, move_left, move_right, jump):
        if move_left:
            self.move_left()
        if move_right:
            self.move_right()
        if jump:
            self.jump()
        self.fall()

    def move_left(self):
        self.coords = self.coords[0] - self.V / FPS,\
                      self.coords[1]  # FPS - const
        self.sprite.move(*self.coords, self.ANIM_DESC['move_left'])

    def move_right(self):
        self.coords = (self.coords[0] + self.V / FPS,
                       self.coords[1])
        self.sprite.move(*self.coords, self.ANIM_DESC['move_right'])

    def jump(self):
        if self.vertical_vel == 0:
            self.vertical_vel = self.V * 3
            self.coords = (self.coords[0], self.coords[1] + self.vertical_vel / FPS)
            self.sprite.move(*self.coords)

    def fall(self):
        self.vertical_vel -= self.G / FPS
        self.coords = (self.coords[0], self.coords[1] - self.vertical_vel / FPS)
        self.sprite.move(*self.coords)


class LightWeighter(AnimatedSprite):
    DIR = 'animation'
    IMG_NAME = 'LightWeight.png'
    V = 100
    G = V * 2
    MOVES_VEL = 5

    def __init__(self, group, coords):
        super().__init__(group, load_image(self.IMG_NAME, self.DIR), 4, 4, *coords, 0)
        self.x, self.y = coords
        self.frames = [self.frames[0], *self.frames[4:12]]
        self.frame_num = 0
        self.vert_vel = 0
        self.hor_vel = 0
        self.is_falling = False
        self.sprite_timer = 0

    def update(self, left, right, jump):
        if right:
            self.hor_vel += self.V
        if left:
            self.hor_vel -= self.V
        self.sprite_changing()
        self.change_frame(self.frame_num)
        self.x += self.hor_vel / FPS
        self.move(self.x, self.y)
        while pygame.sprite.spritecollide(self, surfaces, False):
            self.x -= self.hor_vel / abs(self.hor_vel)
            self.move(self.x, self.y)
        self.hor_vel = 0

        self.move(self.x, self.y + 1)
        if not pygame.sprite.spritecollide(self, surfaces, False):
            self.is_falling = True
        self.move(self.x, self.y)

        if jump and not self.is_falling:
            self.vert_vel = -self.V * 3
        self.y += self.vert_vel / FPS
        self.move(self.x, self.y)
        if pygame.sprite.spritecollide(self, surfaces, False):
            self.is_falling = False
            self.y = int(self.y)
            while pygame.sprite.spritecollide(self, surfaces, False):
                self.y -= self.vert_vel / abs(self.vert_vel)
                self.move(self.x, self.y)
            self.is_falling = False
            self.vert_vel = 0
        if self.is_falling:
            self.vert_vel += self.G / FPS

    def sprite_changing(self):
        if self.hor_vel == 0:
            self.frame_num = 0
            return
        if self.hor_vel > 0:
            if self.frame_num < 5:
                self.frame_num = 5
                self.sprite_timer = 0
            elif self.sprite_timer == self.MOVES_VEL:
                self.frame_num = (self.frame_num - 4) % 4 + 5
                self.sprite_timer = 0
            self.sprite_timer += 1
        if self.hor_vel < 0:
            if self.frame_num == 0 or self.frame_num > 4:
                self.frame_num = 1
                self.sprite_timer = 0
            elif self.sprite_timer == self.MOVES_VEL:
                self.frame_num = self.frame_num % 4 + 1
                self.sprite_timer = 0
            self.sprite_timer += 1




pygame.init()
size = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

timer = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
surfaces = pygame.sprite.Group()
floor = pygame.sprite.Sprite(surfaces)
floor.image = pygame.surface.Surface([500, 1])
floor.image.fill((255, 255, 255))
floor.rect = floor.image.get_rect()
floor.rect.x = 10
floor.rect.y = 500
move_right = False
move_left = False
jump = False
person = LightWeighter(all_sprites, (100, 100))
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                jump = True
            elif event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
    timer.tick(FPS)
    person.update(move_left, move_right, jump)
    jump = False
    all_sprites.draw(screen)
    surfaces.draw(screen)
    pygame.display.flip()
pygame.quit()