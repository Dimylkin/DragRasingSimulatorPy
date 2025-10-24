import sys
import pygame
import os
from drag_rasing.Window_Menu.window_designer import Button

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Драг рейсинг")
screen.fill((255, 127, 80))
font = pygame.font.Font(None, 40)
button_off_color = (240, 230, 210)
button_on_color = (255, 245, 225)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
image_map = pygame.image.load(os.path.join(BASE_DIR, "Images", "Roads", "road.jpg")).convert_alpha()
image_car = pygame.image.load(os.path.join(BASE_DIR, "Images", "Cars", "audi_rs6.png")).convert_alpha()

button_map = Button(screen, 290, 80, 200, 100
                            , 2, 15, button_on_color
                            , button_off_color, None, image_map, "continue")

button_car = Button(screen, 290, 280, 200, 100
                            , 2, 15, button_on_color
                            , button_off_color, None, image_car, "continue")

button_mode_bot = Button(screen, 200, 480, 200, 100
                            , 2, 15, button_on_color
                            , button_off_color, "Игра с ботом", None, "continue")

button_mode_alone = Button(screen, 450, 480, 200, 100
                            , 2, 15, button_on_color
                            , button_off_color, "Одиночная игра", None, "continue")

text_choice_map = font.render("Выберите карту", True, button_on_color)
text_choice_car = font.render("Выберите машину", True, button_on_color)
text_choice_mode = font.render("Выберите режим игры", True, button_on_color)

is_running = True
clock = pygame.time.Clock()

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    screen.blit(text_choice_map, (280, 20))
    button_map.button_with_image()
    screen.blit(text_choice_car, (280, 220))
    button_car.button_with_image()
    screen.blit(text_choice_mode, (280, 420))
    button_mode_bot.button_with_text()
    button_mode_alone.button_with_text()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()