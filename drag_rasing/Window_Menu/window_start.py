import sys
import pygame
from drag_rasing.Window_Menu.window_designer import Button

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Драг рейсинг")
screen.fill((255, 127, 80))
font2 = pygame.font.Font(None, 40)
button_off_color = (240, 230, 210)
button_on_color = (255, 245, 225)

text_welcome = font2.render("!Добро пожаловать в игру про Драг Рейсинг!", True, button_on_color)
button_start = Button(screen, 150, 300, 200, 100
           , 2, 15, button_on_color, button_off_color, "Начать игру!", None, "continue")

button_exit = Button(screen, 450, 300, 200, 100
           , 2, 15, button_on_color, button_off_color, "Выйти из игры :(", None, "continue")

is_running = True
clock = pygame.time.Clock()
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    screen.blit(text_welcome, (100, 200))
    button_start.button_with_text()
    button_exit.button_with_text()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

