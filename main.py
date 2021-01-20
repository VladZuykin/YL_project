import pygame
from objects import HighWeighter, LightWeighter, Box, load_image, KeyAndDoor, FPS


MAIN_COLOR = "#8BDEFF"
SECOND_COLOR = "#FFFFFF"
TITLE_COLOR = "#50505F"
SECOND_TITLE_COLOR = "#60607F"


class MainMenu:

    DEFAULT_WIN_SIZE = 800, 600
    MAX_LEVELS_AMOUNT = 10
    GAME_NAME = "Названия нет"
    MENU_BORDER_RADIUS = 10
    LVL_FILE_FORMAT = "lvl_{}.dat"
    SETTINGS_FILE = "settings.dat"

    def __init__(self):
        self.BUTTON_TITLES = (
            (
                ("Играть", "Настройки", "Выйти"),
            ),
            (
                tuple([f"Уровень {level_num}" for level_num in self.find_lvls_avaible()]),
                ("Разрешение", "Управление")
            ),
            (
                (
                    "800x600", "1024x768", "1152x864", "1280x720", "1280x768",
                    "1280x800", "1280x1024", "1360x768", "1366x768", "1400x1050",
                    "1440x900", "1600x900", "1600x1024", "1680x1050", "1920x1080"
                ),
                ("Обычное", "Обратное")
            )
        )
        self.res = self.DEFAULT_WIN_SIZE
        self.control_scheme = "DEFAULT"
        self.levels = self.find_lvls_avaible()
        pygame.init()
        pygame.display.set_caption(self.GAME_NAME)
        self.window_definition()

        self.menu_num = [0, -1, -1]
        self.menu_scroll = [0] * 3
        self.clock = pygame.time.Clock()

        self.running = True
        while self.running:
            self.screen.fill(pygame.Color(MAIN_COLOR))
            self.event_processing()
            self.clock.tick(FPS)
            self.update()
            pygame.display.flip()
        pygame.quit()

    def show_message(self):
        if self.msg_sec_showed <= self.msg_sec_must:
            message = self.message_font.render(self.message, True, pygame.Color(SECOND_TITLE_COLOR))
            dest = self.res[0] * 0.03, self.res[1] * 0.95
            rect = message.get_rect(topleft=dest)
            self.screen.blit(message, rect)
            self.msg_sec_showed += 1 / FPS
        else:
            self.message_drop()

    def message_drop(self):
        self.message = ""
        self.msg_sec_showed = 0
        self.msg_sec_must = -1

    def find_lvls_avaible(self):
        levels_avaible = []
        for level_num in range(1, self.MAX_LEVELS_AMOUNT + 1):
            try:
                f = open(self.LVL_FILE_FORMAT.format(level_num))
                f.close()
                levels_avaible.append(level_num)
            except FileNotFoundError:
                pass
        return levels_avaible

    def window_definition(self):
        self.import_settings()
        self.screen = pygame.display.set_mode(self.res)
        self.menu_definition()

    def import_settings(self):
        try:
            with open(self.SETTINGS_FILE, "r", encoding="UTF-8") as f:
                lines = f.readlines()
            if len(lines) != 2:
                raise FileNotFoundError
            self.res = [int(num) for num in lines[0].split("x")]
            self.control_scheme = lines[1].rstrip()
        except FileNotFoundError or ValueError:
            pass

    def update(self):
        self.draw_menu()
        self.draw_main_title()
        self.show_message()

    def event_processing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    btn_num = self.check_for_button_clicked(event.pos)
                    if self.check_for_menu_clicked(event.pos) == 0:
                        self.first_menu_processing(btn_num)
                    elif self.menu_num[1] != -1 and self.check_for_menu_clicked(event.pos) == 1:
                        self.second_menu_processing(btn_num, event.pos)
                    elif self.menu_num[2] != -1 and self.check_for_menu_clicked(event.pos) == 2:
                        self.third_menu_processing(btn_num)
                elif event.button == 4 or event.button == 5:
                    self.scroll_processing(event.pos, event.button)

    def run_level(self, num):
        self.message_drop()
        Level(self.LVL_FILE_FORMAT.format(num), self.res, self.screen, self.control_scheme)

    def first_menu_processing(self, btn_num):
        if btn_num in (0, 1):
            if self.menu_num[1] != btn_num:
                self.menu_num[1] = btn_num
                self.menu_num[2] = -1
                self.menu_scroll[1] = self.menu_scroll[2] = 0
            else:
                self.menu_num[1] = self.menu_num[2] = -1
        elif btn_num == 2:
            self.running = False

    def second_menu_processing(self, btn_num, pos):
        if btn_num != -1:
            if self.menu_num[1] == 0:
                self.run_level(self.levels[(self.check_for_button_clicked(pos))])  # Запуск уровня
            elif self.menu_num[1] == 1:
                self.menu_scroll[2] = 0
                if self.menu_num[2] != btn_num:
                    self.menu_num[2] = btn_num
                else:
                    self.menu_num[2] = -1

    def third_menu_processing(self, btn_num):
        if btn_num != -1:
            f = open(self.SETTINGS_FILE, "w", encoding="UTF-8")
            if self.menu_num[2] == 0:  # Изменение разрешения.
                res_str = self.BUTTON_TITLES[2][self.menu_num[2]][btn_num]
                f.write(res_str + "\n" + self.control_scheme)
                f.close()
                self.window_definition()
                self.message = "Разрешение изменено."
            elif self.menu_num[2] == 1:
                res_str = "x".join([str(num) for num in self.res])
                if btn_num == 0:
                    self.control_scheme = "DEFAULT"
                    self.message = "Схема управления изменена на стандартную:" + \
                        " WASD - тяжелый персонаж, ←→↑↓ - легкий персонаж."

                else:
                    self.control_scheme = "REVERSED"
                    self.message = "Схема управления изменена на обратную:" + \
                        " WASD - легкий персонаж, ←→↑↓ - тяжелый персонаж."
                f.write(res_str + "\n" + self.control_scheme)
                f.close()

            self.msg_sec_showed = 0
            self.msg_sec_must = 5

    def scroll_processing(self, pos, btn_num):
        if self.check_for_menu_clicked(pos) is not None:
            menu_num = self.check_for_menu_clicked(pos)
            last_btn_coords = self.btns_coords[menu_num][self.menu_num[menu_num]][-1]
            btn_size = self.btn_size[menu_num]
            if last_btn_coords[1] + btn_size[1] < \
                    self.menu_border_coords[menu_num][1] + self.menu_border_size[1]:
                return  # Если все кнопки влезают в рамки меню, скролл не работает.
            if btn_num == 4:
                scroll = min(0, self.menu_scroll[menu_num] + self.res[1] * 0.05)
            else:
                scroll = max(-self.menu_max_scroll[menu_num][self.menu_num[menu_num]],
                             self.menu_scroll[menu_num] - self.res[1] * 0.05)
            self.menu_scroll[menu_num] = scroll

    def check_for_menu_clicked(self, mouse_coords):
        mouse_x, mouse_y = mouse_coords
        for menu_num in range(len(self.BUTTON_TITLES)):
            if self.menu_border_coords[menu_num][0] <= mouse_x <= \
                    self.menu_border_coords[menu_num][0] + self.menu_border_size[0] and \
                    self.menu_border_coords[menu_num][1] <= mouse_y <= \
                    self.menu_border_coords[menu_num][1] + self.menu_border_size[1]:
                return menu_num
        return None

    def check_for_button_clicked(self, mouse_coords):
        mouse_x, mouse_y = mouse_coords
        button_clicked_number = -1
        if self.check_for_menu_clicked(mouse_coords) is None:
            return button_clicked_number
        for menu_num in range(len(self.BUTTON_TITLES)):
            for btn_num in range(len(self.btns_coords[menu_num][self.menu_num[menu_num]])):
                btn_x, btn_y = self.btns_coords[menu_num][self.menu_num[menu_num]][btn_num]
                if btn_x <= mouse_x <= btn_x + self.btn_size[menu_num][0] and \
                        btn_y + self.menu_scroll[menu_num] <= mouse_y <= \
                        btn_y + self.menu_scroll[menu_num] + self.btn_size[menu_num][1]:
                    return btn_num
        return button_clicked_number

    def draw_main_title(self):
        title = self.title_font.render(self.GAME_NAME, True, pygame.Color(TITLE_COLOR))
        title_place = title.get_rect(center=(int(self.res[0] * 0.5), int(self.res[1] * 0.15)))
        self.screen.blit(title, title_place)

    def draw_menu(self):
        for menu_num in range(len(self.BUTTON_TITLES)):
            if self.menu_num[menu_num] == -1:
                continue
            for btn_num in range(len(self.btns_coords[menu_num][self.menu_num[menu_num]])):
                btn_src_coords = self.btns_coords[menu_num][self.menu_num[menu_num]][btn_num]
                btn_coords = btn_src_coords[0], btn_src_coords[1] + self.menu_scroll[menu_num]
                if btn_coords[1] + self.btn_size[menu_num][1] < self.menu_border_coords[menu_num][1] or \
                        btn_coords[1] > self.menu_border_coords[menu_num][1] + self.menu_border_size[1]:
                    continue
                # Прямоугольники кнопки
                pygame.draw.rect(self.screen, pygame.Color(SECOND_COLOR),
                                 (*btn_coords, *self.btn_size[menu_num]),
                                 0,
                                 self.MENU_BORDER_RADIUS)
                pygame.draw.rect(self.screen, pygame.Color(SECOND_COLOR),
                                 (*btn_coords, *self.btn_size[menu_num]),
                                 3,
                                 self.MENU_BORDER_RADIUS)

                title = self.button_title_font.render(
                    str(self.BUTTON_TITLES[menu_num][self.menu_num[menu_num]][btn_num]),
                    True,
                    pygame.Color(SECOND_TITLE_COLOR)
                )
                title_center_coords = btn_coords[0] + self.btn_size[menu_num][0] // 2,\
                    btn_coords[1] + self.btn_size[menu_num][1] // 2
                title_place = title.get_rect(center=title_center_coords)
                self.screen.blit(title, title_place)

            # Вспомогательные прямоугольники для скролла.
            pygame.draw.rect(self.screen, pygame.Color(MAIN_COLOR), (
                (self.menu_rect[menu_num][0],
                    self.menu_rect[menu_num][1] - self.btn_size[menu_num][1]),
                (self.menu_rect[menu_num][2],
                    self.btn_size[menu_num][1])))
            pygame.draw.rect(self.screen, pygame.Color(MAIN_COLOR), (
                (self.menu_rect[menu_num][0],
                    self.menu_rect[menu_num][1] + self.menu_rect[menu_num][3]),
                (self.menu_rect[menu_num][2],
                    self.btn_size[menu_num][1])))
            # Прямоугольик меню.
            pygame.draw.rect(self.screen, pygame.Color(SECOND_COLOR),
                             self.menu_rect[menu_num], 3, self.MENU_BORDER_RADIUS)

    def menu_definition(self):
        # Определение границ и размеров прямоугольников меню.
        self.menu_border_size = (self.res[0] * 0.3, self.res[1] * 0.6)

        self.menu_border_coords = []
        self.menu_rect = []
        for menu_num in range(3):
            self.menu_border_coords.append((self.res[0] * (0.02 + menu_num * 0.33),
                                           self.res[1] * 0.33))
            self.menu_rect.append(pygame.Rect(*self.menu_border_coords[menu_num],
                                              *self.menu_border_size))

        # Определение границ и размера кнопок прямоугольников меню.
        self.outer_margins = (self.res[0] * 0.015, self.res[1] * 0.02)

        self.between_buttons_margin = self.res[1] * 0.02
        self.btn_size = []
        self.btn_size.append((self.menu_border_size[0] - self.outer_margins[0] * 2,
                              (self.menu_border_size[1] -
                               (self.outer_margins[1] * 2 + self.between_buttons_margin *
                                (len(self.BUTTON_TITLES[0][0]) - 1))) // len(self.BUTTON_TITLES[0][0])))
        for _ in range(2):
            self.btn_size.append((self.btn_size[0][0], int(self.res[1] * 0.1)))

        # Определение координат кнопок прямоугольников меню.
        self.btns_coords = []
        for menu_num in range(3):
            btn_x = int(self.menu_border_coords[menu_num][0] + self.outer_margins[0])
            menu_btns_coords = []
            for sub_menu_num in range(len(self.BUTTON_TITLES[menu_num])):
                point_btn_coords = []
                for btn_num in range(len(self.BUTTON_TITLES[menu_num][sub_menu_num])):
                    btn_y = int(self.menu_border_coords[menu_num][1] + self.outer_margins[1] +
                                (self.between_buttons_margin + self.btn_size[menu_num][1]) * btn_num)
                    point_btn_coords.append((btn_x, btn_y))
                menu_btns_coords.append(point_btn_coords.copy())
            self.btns_coords.append(menu_btns_coords.copy())

        # Определение скроллов и максимальных скроллов меню.
        self.menu_max_scroll = []
        for menu_num in range(3):
            self.menu_max_scroll.append([(self.between_buttons_margin + 1 + self.btn_size[menu_num][1]) *
                                         len(self.BUTTON_TITLES[menu_num][sub_menu_num]) -
                                         self.menu_border_size[1]
                                         for sub_menu_num in range(len(self.BUTTON_TITLES[menu_num]))])

        # Определение размера шрифтов.
        self.button_title_font = pygame.font.SysFont('Calibri', int(self.res[0] * 0.05))
        self.title_font = pygame.font.SysFont('Calibri', int(self.res[0] * 0.1), True)
        self.message_font = pygame.font.SysFont('Calibri', int(self.res[0] * 0.02), True)

        # Инииализация сообщения
        self.message_drop()


class Level:
    FIELD_SIZE = 16, 12
    DEFAULT_ACTIONS = {"move_left": False, "move_right": False, "jump": False}

    def __init__(self, lvl_file_name, res, surface, control_scheme):  # res - разрешение окна.
        self.res = res
        self.message = ""
        self.sub_message = "Нажмите Q, чтобы вернуться в меню."
        self.message_font = pygame.font.SysFont("Calibri", self.res[0] // 8, True)
        self.sub_message_font = pygame.font.SysFont("Calibri", self.res[0] // 20, True)

        self.block_size = self.res[0] // self.FIELD_SIZE[0], \
            self.res[1] // self.FIELD_SIZE[1]
        self.persons = []
        self.objects_groups = {"walls": pygame.sprite.Group(),
                               "boxes": pygame.sprite.Group(),
                               "light_boxes": pygame.sprite.Group(),
                               "heavy_boxes": pygame.sprite.Group(),
                               "spikes": pygame.sprite.Group(),
                               "vanished": pygame.sprite.Group(),
                               "keys": pygame.sprite.Group(),
                               "doors": pygame.sprite.Group(),
                               "l_exit": pygame.sprite.Group(),
                               "h_exit": pygame.sprite.Group(),
                               "light": pygame.sprite.Group(),
                               "heavy": pygame.sprite.Group(),
                               "portals": pygame.sprite.Group()}

        self.get_from_file(lvl_file_name)

        if control_scheme == "DEFAULT" and type(self.persons[0]) == HighWeighter or \
                control_scheme != "DEFAULT" and type(self.persons[0]) == LightWeighter:
            self.persons.reverse()

        self.surface = surface
        self.surface.fill(pygame.Color(MAIN_COLOR))
        self.persons_actions = [self.DEFAULT_ACTIONS.copy(),
                                self.DEFAULT_ACTIONS.copy()]

        timer = pygame.time.Clock()
        self.running = True
        self.freeze = False
        while self.running:
            self.surface.fill(pygame.Color(MAIN_COLOR))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.running = False
                if not self.freeze:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.persons_actions[0]["jump"] = True
                        elif event.key == pygame.K_w:
                            self.persons_actions[1]["jump"] = True
                        elif event.key == pygame.K_LEFT:
                            self.persons_actions[0]["move_left"] = True
                        elif event.key == pygame.K_a:
                            self.persons_actions[1]["move_left"] = True

                        elif event.key == pygame.K_RIGHT:
                            self.persons_actions[0]["move_right"] = True
                        elif event.key == pygame.K_d:
                            self.persons_actions[1]["move_right"] = True

                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                           self.persons_actions[0]["move_left"] = False
                        elif event.key == pygame.K_a:
                            self.persons_actions[1]["move_left"] = False

                        elif event.key == pygame.K_RIGHT:
                            self.persons_actions[0]["move_right"] = False
                        elif event.key == pygame.K_d:
                            self.persons_actions[1]["move_right"] = False
            timer.tick(FPS)
            self.draw()
            if not self.freeze:
                self.update(self.persons_actions)
                self.persons_actions[0]["jump"] = self.persons_actions[1]["jump"] = False
            else:
                self.show_message()
            pygame.display.flip()

    def draw(self):
        self.objects_groups["walls"].draw(self.surface)
        self.objects_groups["boxes"].draw(self.surface)
        self.objects_groups["heavy"].draw(self.surface)
        self.objects_groups["light"].draw(self.surface)
        self.objects_groups["keys"].draw(self.surface)
        self.objects_groups["h_exit"].draw(self.surface)
        self.objects_groups["l_exit"].draw(self.surface)
        self.objects_groups["spikes"].draw(self.surface)
        self.objects_groups["vanished"].draw(self.surface)
        self.objects_groups["portals"].draw(self.surface)

    def update(self, action_list):  # Принимает коллекцию с кортежами действий персонажей.
        for person_num, person in enumerate(self.persons):
            person.update(action_list[person_num], self.objects_groups)
        self.objects_groups["boxes"].update(self.objects_groups)
        self.objects_groups["keys"].update(self.objects_groups)

        win = True
        for person in self.persons:
            if not person.is_in_exit(self.objects_groups):
                win = False
                break
        if win:
            self.win()

        for person in self.persons:
            if not person.is_alive(self.FIELD_SIZE[1] * self.block_size[1]):
                self.lose()

    def get_from_file(self, file_name):
        # S - незаполненное место, K - кнопка, B - коробка, HB - тяжелая коробка,
        # H - тяжелый персонаж, L - легкий персонаж, D - дверь, W - опорные блоки(стены),
        # HE - выход тяжелого персонажа, LE - выход легкого персонажа,
        # V - прозрачные облака, SP - шипы.
        with open(file_name, "r", encoding="UTF-8") as f:
            for row_num, row in enumerate(f.readlines()):
                for col_num, sign in enumerate(row.split()):
                    absolute_coords = col_num * self.block_size[0], \
                                      row_num * self.block_size[1]
                    if sign.upper()[0] == "K":
                        door_coords = [int(num) for num in sign[2:len(sign) - 1].split(";")]
                        door_absolute_coords = door_coords[0] * self.block_size[0], \
                            door_coords[1] * self.block_size[1]

                        key_size = self.block_size[0], self.block_size[1] // 4
                        key_absolute_coords = absolute_coords[0], \
                            absolute_coords[1] + self.block_size[1] - key_size[1]

                        KeyAndDoor(self.objects_groups,
                                   key_absolute_coords, key_size,
                                   door_absolute_coords, self.block_size)

                    elif sign.upper() == "SP":
                        spikes = pygame.sprite.Sprite(self.objects_groups["spikes"])
                        spikes_size = self.block_size[0], self.block_size[1] // 2
                        spikes_coords = absolute_coords[0],\
                            absolute_coords[1] + self.block_size[1] - spikes_size[1]
                        spikes.rect = *spikes_coords, *spikes_size
                        spikes.image = pygame.transform.scale(load_image(
                            "spikes.png",
                            "pictures"),
                            spikes_size)

                    elif sign.upper() == "B":
                        Box(self.objects_groups, absolute_coords, self.block_size, False)
                    elif sign.upper() == "HB":
                        Box(self.objects_groups, absolute_coords, self.block_size, True)
                    elif sign.upper() == "H":
                        self.persons.append(HighWeighter(self.objects_groups["heavy"],
                                                         absolute_coords, self.block_size))
                    elif sign.upper() == "L":
                        self.persons.append(LightWeighter(self.objects_groups["light"],
                                                          absolute_coords, self.block_size))

                    elif sign.upper() in ("HE", "LE", "W", "V"):
                        if sign.upper() in ("HE", "LE"):
                            if sign.upper() == "HE":
                                exit_name = "h_exit"
                                picture = "HighWeighterPortal.png"
                            else:
                                exit_name = "l_exit"
                                picture = "LightWeighterPortal.png"

                            sprite = pygame.sprite.Sprite(self.objects_groups[exit_name])
                            sprite.image = pygame.Surface((int(self.block_size[0] * 0.1),
                                                          int(self.block_size[1] * 0.5)))
                            sprite.image.fill(pygame.Color("#fcf8cb"))
                            sprite.rect = sprite.image.get_rect()
                            sprite.rect.x = absolute_coords[0] + (self.block_size[0] -
                                                                  sprite.image.get_size()[0]) // 2
                            sprite.rect.y = absolute_coords[1] + (self.block_size[1] -
                                                                  sprite.image.get_size()[1])
                            group = "portals"
                        elif sign.upper() == "W":
                            group = "walls"
                            picture = "Wall.png"
                        elif sign.upper() == "V":
                            group = "vanished"
                            picture = "Vanished.png"
                        obj = pygame.sprite.Sprite(self.objects_groups[group])
                        obj.rect = absolute_coords, self.block_size
                        obj.image = pygame.transform.scale(load_image(
                            picture,
                            "pictures"),
                            self.block_size)

    def show_message(self):
        message = self.message_font.render(self.message,
                                           True, pygame.Color(TITLE_COLOR))
        sub_message = self.sub_message_font.render(self.sub_message,
                                                   True, pygame.Color(SECOND_TITLE_COLOR))
        message_dest = message.get_rect(center=(self.res[0] // 2,
                                                self.res[1] // 3))
        sub_message_dest = sub_message.get_rect(center=(self.res[0] // 2,
                                                        self.res[1] // 2))
        self.surface.blit(message, message_dest)
        self.surface.blit(sub_message, sub_message_dest)

    def win(self):
        self.freeze = True
        self.message = "Победа"

    def lose(self):
        self.freeze = True
        self.message = "Проигрыш"


if __name__ == '__main__':
    game = MainMenu()
