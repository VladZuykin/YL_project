import pygame
import os
import sys


FPS = 50  # TODO


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
    def __init__(self, group, sheet, columns, rows, x, y, size, begin_frame_num=0):
        super().__init__(group)
        self.size = size
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.rect.w, self.rect.h = self.size
        self.change_frame(begin_frame_num)
        self.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(
                    pygame.transform.scale(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)),
                                           self.size))

    def move(self, x, y, frame_num=None):
        self.rect = self.rect.move(int(x) - self.rect.x, int(y) - self.rect.y)
        if frame_num is not None:
            self.change_frame(frame_num)

    def change_frame(self, frame_num):
        self.image = self.frames[frame_num]


class OverWeighter(AnimatedSprite):
    DIR = 'animation'
    IMG_NAME = 'HighWeighter.png'

    def __init__(self, group, coords, size):
        super().__init__(group, load_image(self.IMG_NAME, self.DIR), 5, 1, *coords, size,  0)
        self.frame_num = 0

        self.V = size[0] // 1.2
        self.G = size[1] * 7
        self.J = size[1] * 4

        self.vert_vel = 0
        self.hor_vel = 0
        self.x, self.y = coords
        self.is_falling = True

    def update(self, action_list, objects_groups):
        if action_list["move_right"]:
            self.hor_vel += self.V
        if action_list["move_left"]:
            self.hor_vel -= self.V
        self.sprite_changing()
        self.change_frame(self.frame_num)
        self.x += self.hor_vel / FPS
        self.move(self.x, self.y)
        if pygame.sprite.spritecollide(self, objects_groups["box"], False):
            pygame.sprite.spritecollide(self, objects_groups["box"], False)[0].try_to_move(self.hor_vel / FPS,
                                                                                           objects_groups)
        while pygame.sprite.spritecollide(self, objects_groups["wall"], False) or\
                pygame.sprite.spritecollide(self, objects_groups["box"], False):
            self.x -= self.hor_vel / abs(self.hor_vel)
            self.move(self.x, self.y)
        self.hor_vel = 0

        self.move(self.x, self.y + 1)
        if not pygame.sprite.spritecollide(self, objects_groups["wall"], False) and not\
                pygame.sprite.spritecollide(self, objects_groups["box"], False):
            self.is_falling = True
        self.move(self.x, self.y)

        if action_list["jump"] and not self.is_falling:
            self.vert_vel = -self.J
        self.y += self.vert_vel / FPS
        self.move(self.x, self.y)
        if pygame.sprite.spritecollide(self, objects_groups["wall"], False) or \
                pygame.sprite.spritecollide(self, objects_groups["box"], False):
            self.is_falling = False
            self.y = int(self.y)
            self.move(self.x, self.y)
            while pygame.sprite.spritecollide(self, objects_groups["wall"], False) or \
                    pygame.sprite.spritecollide(self, objects_groups["box"], False):
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
    IMG_NAME = 'LightWeighter.png'

    ANIM_VEL = 5

    def __init__(self, group, coords, size):
        super().__init__(group, load_image(self.IMG_NAME, self.DIR), 4, 4, *coords, size, 0)
        self.frames = [self.frames[0], *self.frames[4:12]]
        self.frame_num = 0
        self.sprite_timer = 0

        self.V = size[0] * 2
        self.G = size[1] * 6
        self.J = size[1] * 5

        self.vert_vel = 0
        self.hor_vel = 0
        self.x, self.y = coords
        self.is_falling = True

    def update(self, action_list, objects_groups):
        if action_list["move_right"]:
            self.hor_vel += self.V
        if action_list["move_left"]:
            self.hor_vel -= self.V
        self.sprite_changing()
        self.change_frame(self.frame_num)
        self.x += self.hor_vel / FPS
        self.move(self.x, self.y)
        if pygame.sprite.spritecollide(self, objects_groups["box"], False):
            pygame.sprite.spritecollide(self, objects_groups["box"], False)[0].try_to_move(self.hor_vel / FPS,
                                                                                           objects_groups)
        while pygame.sprite.spritecollide(self, objects_groups["wall"], False) or\
                pygame.sprite.spritecollide(self, objects_groups["box"], False):
            self.x -= self.hor_vel / abs(self.hor_vel)
            self.move(self.x, self.y)
        self.hor_vel = 0

        self.move(self.x, self.y + 1)
        if not pygame.sprite.spritecollide(self, objects_groups["wall"], False) and not\
                pygame.sprite.spritecollide(self, objects_groups["box"], False):
            self.is_falling = True
        self.move(self.x, self.y)

        if action_list["jump"] and not self.is_falling:
            self.vert_vel = -self.J
        self.y += self.vert_vel / FPS
        self.move(self.x, self.y)
        if pygame.sprite.spritecollide(self, objects_groups["wall"], False) or\
                pygame.sprite.spritecollide(self, objects_groups["box"], False):
            self.is_falling = False
            self.y = int(self.y)
            self.move(self.x, self.y)
            while pygame.sprite.spritecollide(self, objects_groups["wall"], False) or\
                    pygame.sprite.spritecollide(self, objects_groups["box"], False):
                self.y -= self.vert_vel / abs(self.vert_vel)
                self.move(self.x, self.y)
            self.vert_vel = 0
        if self.is_falling:
            self.vert_vel += self.G / FPS

    def sprite_changing(self):
        if self.hor_vel == 0:
            self.frame_num = 0
            return
        elif self.hor_vel > 0:
            if self.frame_num < 5:
                self.frame_num = 5
                self.sprite_timer = 0
            elif self.sprite_timer == self.ANIM_VEL:
                self.frame_num = (self.frame_num - 4) % 4 + 5
                self.sprite_timer = 0
            self.sprite_timer += 1
        elif self.hor_vel < 0:
            if self.frame_num == 0 or self.frame_num > 4:
                self.frame_num = 1
                self.sprite_timer = 0
            elif self.sprite_timer == self.ANIM_VEL:
                self.frame_num = self.frame_num % 4 + 1
                self.sprite_timer = 0
            self.sprite_timer += 1


class Box(pygame.sprite.Sprite):
    def __init__(self, group, coords, size):
        super().__init__(group)
        self.G = size[1] * 5
        self.image = pygame.transform.scale(load_image('box.png', 'pictures'), size)
        self.rect = self.image.get_rect()
        self.x, self.y = coords
        self.rect.x, self.rect.y = coords
        self.is_falling = True
        self.vert_vel = 0

    def move(self, x, y):
        self.rect.x = int(x)
        self.rect.y = int(y)

    def try_to_move(self, vel, objects_groups):
        self.move(self.x, self.y - 1)
        if len(pygame.sprite.spritecollide(self, objects_groups["box"], False)) > 1:
            self.move(self.x, self.y)
            return
        self.move(self.x, self.y)
        for i in range(int(abs(vel))):
            self.x += vel / abs(vel)
            self.move(self.x, self.y)
            if len(pygame.sprite.spritecollide(self, objects_groups["box"], False)) > 1 or\
                    pygame.sprite.spritecollide(self, objects_groups["wall"], False):
                self.x -= vel / abs(vel)
                self.move(self.x, self.y)
                return
        return

    def update(self, objects_groups):
        self.move(self.x, self.y + 1)
        if not pygame.sprite.spritecollide(self, objects_groups["wall"], False) or\
                not len(pygame.sprite.spritecollide(self, objects_groups["box"], False)) > 1:
            self.is_falling = True
        self.move(self.x, self.y)

        self.y += self.vert_vel / FPS
        self.move(self.x, self.y)
        if pygame.sprite.spritecollide(self, objects_groups["wall"], False) or\
                len(pygame.sprite.spritecollide(self, objects_groups["box"], False)) > 1:
            self.is_falling = False
            self.y = int(self.y)
            self.move(self.x, self.y)
            while pygame.sprite.spritecollide(self, objects_groups["wall"], False) or\
                    len(pygame.sprite.spritecollide(self, objects_groups["box"], False)) > 1:
                self.y -= 1
                self.move(self.x, self.y)
            self.vert_vel = 0
        if self.is_falling:
            self.vert_vel += self.G / FPS


class Key(pygame.sprite.Sprite):
    pass


class Door(pygame.sprite.Sprite):
    pass
