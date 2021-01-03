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


class OverWeighter(AnimatedSprite):
    DIR = 'animation'
    IMG_NAME = 'HighWeigher.png'
    ANIM_DESC = {'stand': 0, 'move_left': 1, 'move_down': 2, 'move_up': 3, 'move_right': 4}
    V = 100
    G = V * 3
    J = V * 2

    def __init__(self, group, coords):
        super().__init__(group, load_image(self.IMG_NAME, self.DIR), 5, 1, *coords, 0)
        self.x, self.y = coords
        self.frame_num = 0
        self.vert_vel = 0
        self.hor_vel = 0
        self.is_falling = True

    def update(self, left, right, jump):
        if right:
            self.hor_vel += self.V
        if left:
            self.hor_vel -= self.V
        self.sprite_changing()
        self.change_frame(self.frame_num)
        self.x += self.hor_vel / FPS
        self.move(self.x, self.y)
        if pygame.sprite.spritecollide(self, boxes, False):
            pygame.sprite.spritecollide(self, boxes, False)[0].try_to_move(self.hor_vel / FPS, surfaces)
        while pygame.sprite.spritecollide(self, surfaces, False) or\
                pygame.sprite.spritecollide(self, boxes, False):
            self.x -= self.hor_vel / abs(self.hor_vel)
            self.move(self.x, self.y)
        self.hor_vel = 0

        self.move(self.x, self.y + 1)
        if not pygame.sprite.spritecollide(self, surfaces, False) and not\
                pygame.sprite.spritecollide(self, boxes, False):
            self.is_falling = True
        self.move(self.x, self.y)

        if jump and not self.is_falling:
            self.vert_vel = -self.J
        self.y += self.vert_vel / FPS
        self.move(self.x, self.y)
        if pygame.sprite.spritecollide(self, surfaces, False) or \
                pygame.sprite.spritecollide(self, boxes, False):
            self.is_falling = False
            self.y = int(self.y)
            self.move(self.x, self.y)
            while pygame.sprite.spritecollide(self, surfaces, False) or \
                    pygame.sprite.spritecollide(self, boxes, False):
                self.y -= self.vert_vel / abs(self.vert_vel)
                self.move(self.x, self.y)
            self.vert_vel = 0
        if self.is_falling:
            self.vert_vel += self.G / FPS

    def sprite_changing(self):
        if self.hor_vel == 0:
            self.frame_num = 0
            return
        if self.hor_vel > 0:
            self.frame_num = 4
        if self.hor_vel < 0:
            self.frame_num = 1


class LightWeighter(AnimatedSprite):
    DIR = 'animation'
    IMG_NAME = 'LightWeight.png'
    V = 100
    G = V * 3
    J = V * 3
    MOVES_VEL = 5

    def __init__(self, group, coords):
        super().__init__(group, load_image(self.IMG_NAME, self.DIR), 4, 4, *coords, 0)
        self.x, self.y = coords
        self.frames = [self.frames[0], *self.frames[4:12]]
        self.frame_num = 0
        self.vert_vel = 0
        self.hor_vel = 0
        self.is_falling = True
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
        if pygame.sprite.spritecollide(self, boxes, False):
            pygame.sprite.spritecollide(self, boxes, False)[0].try_to_move(self.hor_vel / FPS, surfaces)
        while pygame.sprite.spritecollide(self, surfaces, False) or\
                pygame.sprite.spritecollide(self, boxes, False):
            self.x -= self.hor_vel / abs(self.hor_vel)
            self.move(self.x, self.y)
        self.hor_vel = 0

        self.move(self.x, self.y + 1)
        if not pygame.sprite.spritecollide(self, surfaces, False) and not\
                pygame.sprite.spritecollide(self, boxes, False):
            self.is_falling = True
        self.move(self.x, self.y)

        if jump and not self.is_falling:
            self.vert_vel = -self.J
        self.y += self.vert_vel / FPS
        self.move(self.x, self.y)
        if pygame.sprite.spritecollide(self, surfaces, False) or\
                pygame.sprite.spritecollide(self, boxes, False):
            self.is_falling = False
            self.y = int(self.y)
            self.move(self.x, self.y)
            while pygame.sprite.spritecollide(self, surfaces, False) or\
                    pygame.sprite.spritecollide(self, boxes, False):
                self.y -= self.vert_vel / abs(self.vert_vel)
                self.move(self.x, self.y)
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


class Box(pygame.sprite.Sprite):
    G = 300

    def __init__(self, group, coords):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('box.png', 'pictures'), (50, 50))
        self.rect = self.image.get_rect()
        self.x, self.y = coords
        self.rect.x, self.rect.y = coords
        self.is_falling = True
        self.vert_vel = 0

    def move(self, x, y):
        self.rect.x = int(x)
        self.rect.y = int(y)

    def try_to_move(self, vel, group):
        self.move(self.x, self.y - 1)
        if len(pygame.sprite.spritecollide(self, boxes, False)) > 1:
            self.move(self.x, self.y)
            return
        self.move(self.x, self.y)
        for i in range(int(abs(vel))):
            self.x += vel / abs(vel)
            self.move(self.x, self.y)
            if len(pygame.sprite.spritecollide(self, boxes, False)) > 1 or\
                    pygame.sprite.spritecollide(self, surfaces, False) or\
                    pygame.sprite.spritecollide(self, group, False):
                self.x -= vel / abs(vel)
                self.move(self.x, self.y)
                return
        return

    def update(self):
        self.move(self.x, self.y + 1)
        if not pygame.sprite.spritecollide(self, surfaces, False) or\
                not len(pygame.sprite.spritecollide(self, boxes, False)) > 1:
            self.is_falling = True
        self.move(self.x, self.y)

        self.y += self.vert_vel / FPS
        self.move(self.x, self.y)
        if pygame.sprite.spritecollide(self, surfaces, False) or\
                len(pygame.sprite.spritecollide(self, boxes, False)) > 1:
            self.is_falling = False
            self.y = int(self.y)
            self.move(self.x, self.y)
            while pygame.sprite.spritecollide(self, surfaces, False) or\
                    len(pygame.sprite.spritecollide(self, boxes, False)) > 1:
                self.y -= 1
                self.move(self.x, self.y)
            self.vert_vel = 0
        if self.is_falling:
            self.vert_vel += self.G / FPS


pygame.init()
size = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

timer = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
surfaces = pygame.sprite.Group()
boxes = pygame.sprite.Group()
box = Box(boxes, (400, 200))
box1 = Box(boxes, (400, 300))
floor = pygame.sprite.Sprite(surfaces)
floor.image = pygame.surface.Surface([500, 1])
floor.image.fill((255, 255, 255))
floor.rect = floor.image.get_rect()
floor.rect.x = 10
floor.rect.y = 500
move_right = False
move_left = False
jump = False
person = OverWeighter(all_sprites, (100, 100))
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
    boxes.update()
    boxes.draw(screen)
    surfaces.draw(screen)
    pygame.display.flip()
pygame.quit()