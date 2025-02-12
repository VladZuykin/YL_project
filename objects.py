import pygame
import os
import sys
from random import randrange

FPS = 60


# Функция, возвращающая рандомный цвет
def generate_color():
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


# Функция,загружающая картинку, фон которой должен быть прозрачным
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


# Класс - наследник от Sprite, хранящий в себе массив спрайтов, для анимации,
# релизующий получение этого массива через картинку, перемещение спрайта на
# какие-то координаты и смену активного изображения спрайта.
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, group, sheet, columns, rows, x, y, size, begin_frame_num=0):
        super().__init__(group)
        self.size = list(map(lambda s: int(0.95 * s), size))
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


# Класс - наследник от AnimatedSprite, который реализует общие функции обоих
# персонажей, а именно: перемещение с учётом физики и взаимодействия с другими
# объектами, смерть, заглушка для анимации и проверка на жизнеспособность
class Character(AnimatedSprite):
    def __init__(self, group, coords, size, sheet, columns, rows, is_heavy):
        super().__init__(group, sheet, columns, rows, *coords, size, 0)
        self.is_heavy = is_heavy

        self.frame_num = 0
        self.sprite_timer = 0

        self.V = 100
        self.G = 100
        self.J = 100

        self.vert_vel = 0
        self.hor_vel = 0
        self.x, self.y = coords
        self.is_falling = True
        self.alive = True

    def is_alive(self, deadline):
        return self.alive and self.y < deadline

    def die(self):
        self.alive = False

    def update(self, action_list, objects_groups):
        if action_list["move_right"]:
            self.hor_vel += self.V
        if action_list["move_left"]:
            self.hor_vel -= self.V
        self.sprite_changing()
        self.change_frame(self.frame_num)
        self.x += self.hor_vel / FPS
        self.move(self.x, self.y)
        if self.is_heavy:
            if pygame.sprite.spritecollideany(self, objects_groups["boxes"]):
                pygame.sprite.spritecollide(self, objects_groups["boxes"], False)[0].try_to_move(self.hor_vel / FPS,
                                                                                                 objects_groups,
                                                                                                 "light")
        else:
            if pygame.sprite.spritecollideany(self, objects_groups["light_boxes"]):
                pygame.sprite.spritecollide(self, objects_groups["light_boxes"], False)[0].try_to_move(
                    self.hor_vel / FPS,
                    objects_groups,
                    "heavy")
        while pygame.sprite.spritecollideany(self, objects_groups["walls"]) or \
                pygame.sprite.spritecollideany(self, objects_groups["boxes"]):
            self.x -= self.hor_vel / abs(self.hor_vel)
            self.move(self.x, self.y)
        self.hor_vel = 0

        self.move(self.x, self.y + 1)
        if not pygame.sprite.spritecollideany(self, objects_groups["walls"]) and not \
                pygame.sprite.spritecollideany(self, objects_groups["boxes"]):
            self.is_falling = True
        self.move(self.x, self.y)

        if action_list["jump"] and not self.is_falling:
            self.vert_vel = -self.J
        self.y += self.vert_vel / FPS
        self.move(self.x, self.y)
        if pygame.sprite.spritecollideany(self, objects_groups["walls"]) or \
                pygame.sprite.spritecollideany(self, objects_groups["boxes"]):
            self.is_falling = False
            self.y = int(self.y)
            self.move(self.x, self.y)
            while pygame.sprite.spritecollideany(self, objects_groups["walls"]) or \
                    pygame.sprite.spritecollideany(self, objects_groups["boxes"]):
                self.y -= self.vert_vel / abs(self.vert_vel)
                self.move(self.x, self.y)
            self.vert_vel = 0
        if self.is_falling:
            self.vert_vel += self.G / FPS

        if pygame.sprite.spritecollideany(self, objects_groups["spikes"]):
            self.die()

    def sprite_changing(self):
        pass


# Класс, ревлизующий особенности сильного персонажа, а именно анимацию,
# проверку на нахождение в выходе, физ. величины и изображения
class HighWeighter(Character):
    DIR = 'animation'
    IMG_NAME = 'HighWeighter.png'

    ANIM_VEL = 20

    def __init__(self, group, coords, size):
        super().__init__(group, coords, size, load_image(self.IMG_NAME, self.DIR), 1, 1, True)
        self.frames.append(pygame.transform.scale(load_image('HighWeighter1.png', self.DIR), size))
        self.frames.append(pygame.transform.scale(load_image('HighWeighter3.png', self.DIR), size))
        self.frames.append(pygame.transform.scale(load_image('HighWeighter2.png', self.DIR), size))
        self.frames.append(pygame.transform.scale(load_image('HighWeighter3.png', self.DIR), size))
        self.rev = False
        for i in range(5):
            self.frames.append(pygame.transform.flip(self.frames[i].copy(), True, False))


        self.V = size[0] // 1.2
        self.G = size[1] * 7
        self.J = size[1] * 4

    def is_in_exit(self, objects_groups):
        return pygame.sprite.spritecollideany(self, objects_groups["h_exit"])

    def sprite_changing(self):
        if self.hor_vel > 0 and self.rev:
            self.rev = False
            self.frame_num = 1
            self.sprite_timer = 0
            return
        if self.hor_vel < 0 and not self.rev:
            self.rev = True
            self.frame_num = 6
            self.sprite_timer = 0
            return
        if self.hor_vel == 0:
            self.frame_num = self.rev * 5
            return
        if self.frame_num % 5 == 0:
            self.sprite_timer = 0
            self.frame_num = self.rev * 5 + 1
            return
        if self.sprite_timer == self.ANIM_VEL:
            self.sprite_timer = 0
            self.frame_num = self.frame_num % 5 % 4 + 1 + self.rev * 5
        self.sprite_timer += 1


# Класс, реализующий особенности ловкого персонажа, а именно анимацию,
# проверку на нахождение в выходе, физ. величины и изображения
class LightWeighter(Character):
    DIR = 'animation'
    IMG_NAME = 'LightWeighter.png'

    ANIM_VEL = 20

    def __init__(self, group, coords, size):
        super().__init__(group, coords, size, load_image(self.IMG_NAME, self.DIR), 1, 1, False)
        self.frames.append(pygame.transform.scale(load_image('LightWeighter1.png', self.DIR), size))
        self.frames.append(pygame.transform.scale(load_image('LightWeighter2.png', self.DIR), size))
        self.rev = False
        for i in range(3):
            self.frames.append(pygame.transform.flip(self.frames[i], True, False))

        self.V = size[0] * 2
        self.G = size[1] * 6
        self.J = size[1] * 5

    def is_in_exit(self, objects_groups):
        return pygame.sprite.spritecollideany(self, objects_groups["l_exit"])

    def sprite_changing(self):
        if self.hor_vel > 0 and self.rev:
            self.rev = False
            self.frame_num = 1
            self.sprite_timer = 0
            return
        if self.hor_vel < 0 and not self.rev:
            self.rev = True
            self.frame_num = 4
            self.sprite_timer = 0
            return
        if self.hor_vel == 0:
            self.frame_num = self.rev * 3
            return
        if self.frame_num % 3 == 0:
            self.sprite_timer = 0
            self.frame_num = self.rev * 3 + 1
            return
        if self.sprite_timer == self.ANIM_VEL:
            self.sprite_timer = 0
            self.frame_num = self.frame_num % 3 % 2 + 1 + self.rev * 3
        self.sprite_timer += 1


# Класс, реализующий коробку, а именно её отображение, перемещение спрайта,
# перемещение с учётом физику, попытку пермещения персножей этой коробки.
class Box(pygame.sprite.Sprite):
    def __init__(self, objects_groups, coords, size, is_heavy):
        super().__init__()
        self.G = size[1] * 5
        self.add(objects_groups['boxes'])
        self.is_heavy = is_heavy
        if is_heavy:
            self.image = pygame.transform.scale(load_image('HeavyBox.png', 'pictures'), size)
            self.add(objects_groups['heavy_boxes'])
        else:
            self.image = pygame.transform.scale(load_image('Box.png', 'pictures'), size)
            self.add(objects_groups['light_boxes'])
        self.rect = self.image.get_rect()
        self.x, self.y = coords
        self.rect.x, self.rect.y = coords
        self.is_falling = True
        self.vert_vel = 0

    def move(self, x, y):
        self.rect.x = int(x)
        self.rect.y = int(y)

    def try_to_move(self, vel, objects_groups, oth_p):
        self.move(self.x, self.y - 1)
        if len(pygame.sprite.spritecollide(self, objects_groups["boxes"], False)) > 1:
            self.move(self.x, self.y)
            return
        self.move(self.x, self.y)
        for i in range(round(abs(vel))):
            self.x += vel / abs(vel)
            self.move(self.x, self.y)
            if len(pygame.sprite.spritecollide(self, objects_groups["boxes"], False)) > 1 or \
                    pygame.sprite.spritecollideany(self, objects_groups["walls"]) or \
                    (pygame.sprite.spritecollideany(self, objects_groups["vanished"]) and not self.is_heavy) or \
                    pygame.sprite.spritecollideany(self, objects_groups[oth_p]):
                self.x -= vel / abs(vel)
                self.move(self.x, self.y)
                return
        return

    def update(self, objects_groups):
        if pygame.sprite.spritecollideany(self, objects_groups["walls"]):
            self.kill()
            return
        self.move(self.x, self.y + 1)
        if not pygame.sprite.spritecollideany(self, objects_groups["walls"]) and \
                not len(pygame.sprite.spritecollide(self, objects_groups["boxes"], False)) > 1 and \
                not (pygame.sprite.spritecollideany(self, objects_groups["vanished"]) and not self.is_heavy):
            self.is_falling = True
        self.move(self.x, self.y)

        self.y += self.vert_vel / FPS
        self.move(self.x, self.y)

        if pygame.sprite.spritecollideany(self, objects_groups["heavy"]):
            objects_groups["heavy"].sprites()[0].die()
        if pygame.sprite.spritecollideany(self, objects_groups["light"]):
            objects_groups["light"].sprites()[0].die()

        if pygame.sprite.spritecollideany(self, objects_groups["walls"]) or \
                len(pygame.sprite.spritecollide(self, objects_groups["boxes"], False)) > 1 or \
                (pygame.sprite.spritecollideany(self, objects_groups["vanished"]) and not self.is_heavy):
            self.is_falling = False
            self.y = int(self.y)
            self.move(self.x, self.y)
            while pygame.sprite.spritecollideany(self, objects_groups["walls"]) or \
                    len(pygame.sprite.spritecollide(self, objects_groups["boxes"], False)) > 1 or \
                    (pygame.sprite.spritecollideany(self, objects_groups["vanished"]) and not self.is_heavy):
                self.y -= 1
                self.move(self.x, self.y)
            self.vert_vel = 0
        if self.is_falling:
            self.vert_vel += self.G / FPS


# Класс, реализующий кнопку и дверь, а именно их отображение, взаимодействие
# между собой, нажатие кнопки каким-то объектом, физику двери и её открытие
class KeyAndDoor(pygame.sprite.Sprite):
    def __init__(self, objects_groups, k_coords, k_size, d_coords, d_size):
        super().__init__(objects_groups["keys"])
        if k_size[1] < 2:
            k_size[1] = 2
        self.width, self.height = k_size
        self.cur_height = self.height
        self.color = generate_color()
        self.coords = list(k_coords)

        self.image = pygame.Surface(k_size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = k_coords
        self.image.fill(self.color)

        self.door = pygame.sprite.Sprite(objects_groups["walls"])
        self.door.image = self.scale_door(load_image("Door.png", "pictures", (255, 255, 255)), d_size)
        self.door.rect = self.door.image.get_rect()
        self.door.rect.x, self.door.rect.y = d_coords[0] + (d_size[0] - self.door.rect[2]) // 2, \
            d_coords[1]

    def scale_door(self, img, size_need):
        # Окрашивает часть двери в цвет кнопки.
        img.fill(pygame.Color(self.color), (40, 4, 8, 141))
        img.fill(pygame.Color(self.color), (35, 47, 18, 20))
        # Масштабирование изображения.
        src_size = img.get_rect()[2:]
        new_width = src_size[0] * size_need[1] // src_size[1]
        new_size = new_width, size_need[1]
        return pygame.transform.scale(img, new_size)

    def update(self, objects_groups):
        if self.cur_height == 1:
            was_pushed = True
        else:
            was_pushed = False
        while self.cur_height != 1 and (pygame.sprite.spritecollideany(self, objects_groups["walls"]) or
                                        pygame.sprite.spritecollideany(self, objects_groups["heavy"]) or
                                        pygame.sprite.spritecollideany(self, objects_groups["light"]) or
                                        pygame.sprite.spritecollideany(self, objects_groups["heavy_boxes"]) or
                                        pygame.sprite.spritecollideany(self, objects_groups["light_boxes"])):
            self.cur_height -= 1
            self.image = pygame.Surface((self.width, self.cur_height))
            self.rect = self.image.get_rect()
            self.coords[1] += 1
            self.rect.x, self.rect.y = self.coords
            self.image.fill(self.color)

        while self.cur_height != self.height and not \
                (pygame.sprite.spritecollideany(self, objects_groups["walls"]) or
                 pygame.sprite.spritecollideany(self, objects_groups["heavy"]) or
                 pygame.sprite.spritecollideany(self, objects_groups["light"]) or
                 pygame.sprite.spritecollideany(self, objects_groups["heavy_boxes"]) or
                 pygame.sprite.spritecollideany(self, objects_groups["light_boxes"])):
            self.cur_height += 1
            self.image = pygame.Surface((self.width, self.cur_height))
            self.rect = self.image.get_rect()
            self.coords[1] -= 1
            self.rect.x, self.rect.y = self.coords
            self.image.fill(self.color)

        if self.cur_height == 1 and not was_pushed:
            objects_groups["walls"].remove(self.door)
            pygame.sprite.spritecollide(self.door, objects_groups["boxes"], True)
        if self.cur_height != 1 and was_pushed:
            self.door.add(objects_groups["walls"])
            if pygame.sprite.spritecollideany(self.door, objects_groups["heavy"]):
                objects_groups["heavy"].sprites()[0].die()
            if pygame.sprite.spritecollideany(self.door, objects_groups["light"]):
                objects_groups["light"].sprites()[0].die()