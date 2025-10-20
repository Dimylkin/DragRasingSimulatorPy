import sys
import pygame
import Drag

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Драг рейсинг")
screen.fill((255, 127, 80))
font = pygame.font.Font(None, 24)
font2 = pygame.font.Font(None, 40)
radius = 15

button_start_game = pygame.Surface((200, 60), pygame.SRCALPHA)
button_exit = pygame.Surface((200, 60), pygame.SRCALPHA)

text_welcome = font2.render("!Добро пожаловать в игру про Драг Рейсинг!", True, (255,255,255))

text_start_game = font.render("Начать игру", True, (0, 0, 0))
text_rect_start_game = text_start_game.get_rect(
    center=(button_start_game.get_width() / 2, button_start_game.get_height() / 2))

text_exit = font.render("Выйти", True, (0, 0, 0))
text_rect_exit = text_exit.get_rect(center=(button_exit.get_width() / 2, button_exit.get_height() / 2))

button_rect_start_game = pygame.Rect(280, 250, 200, 60)
button_rect_exit = pygame.Rect(280, 400, 200, 60)

is_running = True
clock = pygame.time.Clock()

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect_start_game.collidepoint(event.pos):
                print("Button clicked!")
            if button_rect_exit.collidepoint(event.pos):
                is_running = False

    button_start_game.fill((0, 0, 0, 0))
    button_exit.fill((0, 0, 0, 0))

    if button_rect_start_game.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_start_game, (255, 169, 138, 255), (0, 0, 200, 60), border_radius=radius)
        pygame.draw.rect(button_start_game, (0, 0, 0), (0, 0, 200, 60), border_radius=radius, width=1)
    else:
        pygame.draw.rect(button_start_game, (224, 224, 224, 255), (0, 0, 200, 60), border_radius=radius)
        pygame.draw.rect(button_start_game, (0, 0, 0), (0, 0, 200, 60), border_radius=radius, width=1)

    if button_rect_exit.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_exit, (255, 169, 138, 255), (0, 0, 200, 60), border_radius=radius)
        pygame.draw.rect(button_exit, (0, 0, 0), (0, 0, 200, 60), border_radius=radius, width=1)
    else:
        pygame.draw.rect(button_exit, (224, 224, 224, 255), (0, 0, 200, 60), border_radius=radius)
        pygame.draw.rect(button_exit, (0, 0, 0), (0, 0, 200, 60), border_radius=radius, width=1)

    button_start_game.blit(text_start_game, text_rect_start_game)
    button_exit.blit(text_exit, text_rect_exit)

    screen.blit(text_welcome, (90, 100))
    screen.blit(button_start_game, (button_rect_start_game.x, button_rect_start_game.y))
    screen.blit(button_exit, (button_rect_exit.x, button_rect_exit.y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
