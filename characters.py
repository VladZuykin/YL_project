import pygame
import os


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


FPS = 60


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