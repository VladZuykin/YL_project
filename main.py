import pygame


class MainMenu:
    DEFAULT_WIN_SIZE = 800, 600
    GAME_NAME = "Названия нет"
    # Настройки элементов меню.
    MENU_BORDER_RADIUS = 10
    BUTTON_TITLES = ("Новая игра", "Продолжить", "Настройки", "Выйти")

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(self.GAME_NAME)
        self.win_size = self.DEFAULT_WIN_SIZE
        self.screen = pygame.display.set_mode(self.DEFAULT_WIN_SIZE)
        self.menu_definition()

        self.running = True
        while self.running:
            self.screen.fill(pygame.Color("#8bdeff"))
            self.event_processing()
            self.update()
            pygame.display.flip()
        pygame.quit()

    def update(self):
        self.draw_title()
        self.draw_menu()

    def event_processing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                button_number = self.check_for_button_clicked(event.pos)
                if button_number == 0:
                    pass
                elif button_number == 1:
                    pass
                elif button_number == 2:
                    pass
                elif button_number == 3:
                    self.running = False

    def check_for_button_clicked(self, mouse_coords):
        mouse_x, mouse_y = mouse_coords
        button_clicked_number = -1
        for button_number in range(len(self.buttons_coords)):
            button_x, button_y = self.buttons_coords[button_number]
            if button_x <= mouse_x <= button_x + self.button_size[0] and \
                    button_y <= mouse_y <= button_y + self.button_size[1]:
                button_clicked_number = button_number
        return button_clicked_number

    def draw_title(self):
        title = self.title_font.render(self.GAME_NAME, True, pygame.Color("#50505F"))
        title_place = title.get_rect(center=(self.win_size[0] * 0.5, self.win_size[1] * 0.15))
        self.screen.blit(title, title_place)

    def draw_menu(self):
        # Рисование главного прямоугольника меню.
        pygame.draw.rect(self.screen, pygame.Color("#FFFFFF"),
                         self.menu_rect, 3, self.MENU_BORDER_RADIUS)

        # Рисование кнопок меню.
        for button_number in range(len(self.buttons_coords)):
            button_coords = self.buttons_coords[button_number]
            pygame.draw.rect(self.screen, pygame.Color("#FFFFFF"),
                             (*button_coords, *self.button_size), 0, self.MENU_BORDER_RADIUS)
            pygame.draw.rect(self.screen, pygame.Color("#FCFCFC"),
                             (*button_coords, *self.button_size), 3, self.MENU_BORDER_RADIUS)

            title = self.button_title_font.render(self.BUTTON_TITLES[button_number],
                                                  True, pygame.Color("#60607F"))
            title_center_coords = button_coords[0] + self.button_size[0] // 2, \
                button_coords[1] + self.button_size[1] // 2
            title_place = title.get_rect(center=title_center_coords)
            self.screen.blit(title, title_place)

    def menu_definition(self):
        # Определение границ главного прямоугольника меню.
        self.menu_border_coords = (self.win_size[0] * 0.05, self.win_size[1] * 0.36)
        self.menu_border_size = (self.win_size[0] * 0.3, self.win_size[1] * 0.6)
        self.menu_rect = pygame.Rect(*self.menu_border_coords, *self.menu_border_size)

        # Определение границ и размера кнопок.
        self.outer_margins = (self.win_size[0] * 0.015, self.win_size[1] * 0.02)
        self.between_buttons_margins = self.win_size[1] * 0.02
        self.button_size = self.menu_border_size[0] - self.outer_margins[0] * 2,\
            (self.menu_border_size[1] -
             (self.outer_margins[1] * 2 + self.between_buttons_margins *
              (len(self.BUTTON_TITLES) - 1))) // len(self.BUTTON_TITLES)

        # Определение координат кнопок.
        self.buttons_coords = []
        for button_number in range(len(self.BUTTON_TITLES)):
            button_x = self.menu_border_coords[0] + self.outer_margins[0]
            button_y = self.menu_border_coords[1] + self.outer_margins[1] + \
                self.between_buttons_margins * button_number + self.button_size[1] * button_number
            self.buttons_coords.append((button_x, button_y))

        # Определение размера шрифтов.
        self.button_title_font = pygame.font.SysFont('Calibri', int(self.win_size[1] * 0.05))
        self.title_font = pygame.font.SysFont('Calibri', int(self.win_size[1] * 0.1), True)


if __name__ == '__main__':
    game = MainMenu()