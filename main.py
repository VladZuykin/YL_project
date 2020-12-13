import pygame


class MainMenu:
    DEFAULT_WIN_SIZE = 800, 600
    GAME_NAME = "Yandex.Lyceum Project"
    # Настройки элементов меню.
    MENU_BORDER_RADIUS = 10
    BUTTONS_AMOUNT = 4
    BUTTON_TITLES = ("Новая игра", "Продолжить", "Настройки", "Выйти")

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(self.GAME_NAME)
        self.win_size = self.DEFAULT_WIN_SIZE
        self.screen = pygame.display.set_mode(self.DEFAULT_WIN_SIZE)

        self.running = True
        while self.running:
            self.screen.fill(pygame.Color("#8bdeff"))
            self.event_processing()
            self.update()
            pygame.display.flip()
        pygame.quit()

    def event_processing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.draw_title()
        self.draw_menu()

    def draw_title(self):
        title_font = pygame.font.SysFont('Calibri', int(self.win_size[1] * 0.1), True)
        title = title_font.render(self.GAME_NAME, True, pygame.Color("#50505F"))
        title_place = title.get_rect(center=(self.win_size[0] * 0.5, self.win_size[1] * 0.15))
        self.screen.blit(title, title_place)

    def draw_menu(self):
        # Определение границ главного прямоугольника меню, его рисование.
        menu_border_coords = (self.win_size[0] * 0.05, self.win_size[1] * 0.36)
        menu_border_size = (self.win_size[0] * 0.3, self.win_size[1] * 0.6)
        menu_rect = pygame.Rect(*menu_border_coords, *menu_border_size)
        pygame.draw.rect(self.screen, pygame.Color("#FFFFFF"),
                         menu_rect, 3, self.MENU_BORDER_RADIUS)

        # Определение границ и размера кнопок.
        outer_margins = (self.win_size[0] * 0.015, self.win_size[1] * 0.02)
        between_buttons_margins = self.win_size[1] * 0.02
        button_size = menu_border_size[0] - outer_margins[0] * 2, \
            (menu_border_size[1] -
                (outer_margins[1] * 2 +
                    between_buttons_margins * (self.BUTTONS_AMOUNT - 1)
                 )
             ) // self.BUTTONS_AMOUNT

        # Рисование кнопок меню.
        for btn_number in range(self.BUTTONS_AMOUNT):
            button_coords = menu_border_coords[0] + outer_margins[0], \
                            menu_border_coords[1] + outer_margins[1] + \
                            between_buttons_margins * btn_number + button_size[1] * btn_number
            pygame.draw.rect(self.screen, pygame.Color("#FFFFFF"),
                             (*button_coords, *button_size), 0, self.MENU_BORDER_RADIUS)
            pygame.draw.rect(self.screen, pygame.Color("#FCFCFC"),
                             (*button_coords, *button_size), 3, self.MENU_BORDER_RADIUS)

            title_font = pygame.font.SysFont('Calibri', int(self.win_size[1] * 0.05))
            title = title_font.render(self.BUTTON_TITLES[btn_number], True, pygame.Color("#60607F"))
            title_center_coords = button_coords[0] + button_size[0] // 2,\
                button_coords[1] + button_size[1] // 2
            title_place = title.get_rect(center=title_center_coords)
            self.screen.blit(title, title_place)


if __name__ == '__main__':
    game = MainMenu()
