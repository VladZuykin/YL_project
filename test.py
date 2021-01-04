from main import Level
from objects import load_image, Box
import pygame

FPS = 50

pygame.init()
size = 1280, 720
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color("#8bdeff"))

timer = pygame.time.Clock()

level = Level("test_lvl.dat", size, 'DEFAULT')

actions = [{"move_left": False, "move_right": False, "jump": False},
           {"move_left": False, "move_right": False, "jump": False}]
running = True
while running:
    screen.fill(pygame.Color("#8bdeff"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                actions[0]["jump"] = True
            elif event.key == pygame.K_w:
                actions[1]["jump"] = True

            elif event.key == pygame.K_LEFT:
                actions[0]["move_left"] = True
            elif event.key == pygame.K_a:
                actions[1]["move_left"] = True

            elif event.key == pygame.K_RIGHT:
                actions[0]["move_right"] = True
            elif event.key == pygame.K_d:
                actions[1]["move_right"] = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                actions[0]["move_left"] = False

            elif event.key == pygame.K_a:
                actions[1]["move_left"] = False

            elif event.key == pygame.K_RIGHT:
                actions[0]["move_right"] = False

            elif event.key == pygame.K_d:
                actions[1]["move_right"] = False

    timer.tick(FPS)
    level.draw(screen)
    level.update(actions)
    actions[0]["jump"] = actions[1]["jump"] = False
    pygame.display.flip()
pygame.quit()
