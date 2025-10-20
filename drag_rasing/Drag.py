import datetime
from time import sleep
import pygame
import sys
import Car
from Window_Game import Maps


pygame.init()

FONT = pygame.font.Font(None, 36)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 6006

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Драг рейсинг")

road = Maps.LongRoad("Images/Roads/road.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
car = Car.Car("lamborghini_murcielago")
cars = pygame.sprite.Group()
cars.add(car)
car.start_engine()

speeds = [0]
warning_frames = 0
warning_revolutions = 0
is_running = True
is_good_shift = True

clock = pygame.time.Clock()
time_start_race = datetime.datetime.now()

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_gear = car.current_gear
                if current_gear < car.engine.count_gear:
                    new_gear = current_gear + 1
                    is_good_shift = car.shift_gear(new_gear)

                    if not is_good_shift:
                        warning_frames = 60
    car.update(is_good_shift)
    speeds.append(car.engine.get_current_speed())

    if warning_frames > 0:
        warning_frames -= 1
        Maps.Background.draw_not_good_shift(screen, 200, 20)

    road.draw(screen)
    cars.draw(screen)

    Maps.Background.draw_hud(screen, car, 10, 30, 200, 20)

    finished = road.update(car.speed)
    if finished:
        Maps.Background.draw_finish(screen, SCREEN_WIDTH, SCREEN_HEIGHT, time_start_race, speeds)
        is_running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()