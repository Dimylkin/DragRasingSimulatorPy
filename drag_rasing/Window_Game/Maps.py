import pygame
import math
import datetime
from time import sleep


class Background(pygame.sprite.Sprite):
    def __init__(self, image, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()
        self.image_path = image
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.load_image()


    def load_image(self):
        self.original_image = pygame.image.load(self.image_path).convert()
        self.image = pygame.transform.scale(self.original_image,
                                            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()

    def draw_hud(screen, car, x, y, width, height):
        info = car.get_engine_info()
        FONT = pygame.font.Font(None, 30)
        gear_text = FONT.render(f"Текущая передача: {info['gear']}", True, (255, 255, 255))
        speed_text = FONT.render(f"Скорость: {info['speed_kmh']} км/ч", True, (255, 255, 255))

        rpm = car.engine.revolutions
        max_rpm = car.max_revolutions
        min_rpm = car.min_revolutions
        progress = rpm / max_rpm

        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))

        fill_width = int(width * progress)

        if rpm < min_rpm + min_rpm or rpm > max_rpm - min_rpm:
            color = (255, 0, 0)
        else:
            color = (0, 255, 0)

        pygame.draw.rect(screen, color, (x, y, fill_width, height))

        pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), 2)

        text = FONT.render(f"Обороты: {math.ceil(rpm)}", True, (255, 255, 255))

        redline_start = (max_rpm - min_rpm) / max_rpm
        redline_end = (min_rpm + min_rpm) / max_rpm
        redline_x = x + int(width * redline_start)
        redline_x1 = x + int(width * redline_end)
        pygame.draw.line(screen, (255, 0, 0), (redline_x, y), (redline_x, y + height), 2)
        pygame.draw.line(screen, (255, 0, 0), (redline_x1, y), (redline_x1, y + height), 2)

        screen.blit(text, (x, y - 25))
        screen.blit(gear_text, (10, 60))
        screen.blit(speed_text, (10, 90))

    def draw_not_good_shift(screen, width, height):
        FONT = pygame.font.Font(None, 30)
        text_not_good_shift = FONT.render("!Плохое переключение передачи! Потеря мощности!", True, (255, 0, 0))
        screen.blit(text_not_good_shift, ((width / 4) + 100, (height / 4) + 200))
        pygame.display.flip()

    def draw_finish(screen, width, height, time_start_race, speeds):
        time_end_race = datetime.datetime.now()
        spend_time = (time_end_race - time_start_race).total_seconds()
        average_speed = sum(speeds) / len(speeds)
        FONT = pygame.font.Font(None, 30)
        pygame.draw.rect(screen, (224,224,224), (width / 4, height / 4, 400, 300), border_radius= 25)
        pygame.draw.rect(screen, (0, 0, 0), (width / 4, height / 4, 400, 300), border_radius=25, width=2)

        text_finish = FONT.render("!ГОНКА ЗАВЕРШЕНА!", True, (0, 255, 0))
        text_spend_time = FONT.render(f"Время заезда {round(spend_time, 2)} секунд",
                                      True, (0, 0, 0))
        text_average_speed = FONT.render(f"Средняя скорость {round(average_speed, 2)} км/ч",
                                      True, (0, 0, 0))

        screen.blit(text_finish, ((width / 4) + 85, (height / 4) + 20))
        screen.blit(text_spend_time, ((width / 4) + 35, (height / 4) + 70))
        screen.blit(text_average_speed, ((width / 4) + 35, (height / 4) + 130))

        pygame.display.flip()
        sleep(5)


class LongRoad:
    def __init__(self, image, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.segments = pygame.sprite.Group()
        self.segment_width = SCREEN_WIDTH
        self.total_segments = 5

        for i in range(self.total_segments):
            segment = Background(image, SCREEN_WIDTH, SCREEN_HEIGHT)
            segment.rect.x = i * SCREEN_WIDTH
            self.segments.add(segment)

        self.distance_traveled = 0
        self.total_distance = 4020
        self.finished = False
        self.font = pygame.font.Font(None, 36)

    def update(self, car_speed):
        if self.finished:
            return

        self.distance_traveled += car_speed * 0.1

        if self.distance_traveled >= self.total_distance:
            self.finished = True
            return True

        for segment in self.segments:
            segment.rect.x -= car_speed

            if segment.rect.x <= -self.segment_width:
                max_x = max(s.rect.x for s in self.segments)
                segment.rect.x = max_x + self.segment_width

        return False

    def draw(self, screen):
        self.segments.draw(screen)

    def is_finished(self):
        return self.finished