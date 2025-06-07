import pygame
import random
import sys
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRID_SIZE = 80
GRID_WIDTH = 9
GRID_HEIGHT = 5
LAWN_LEFT = 100
LAWN_TOP = 100

# Цвета
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plants vs Zombies")
clock = pygame.time.Clock()


# Классы
class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

    def update(self):
        pass


class PeaShooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cooldown = 0
        self.color = (0, 200, 0)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        # Рисуем "голову" гороха
        pygame.draw.circle(screen, GREEN, (self.x + GRID_SIZE - 10, self.y + GRID_SIZE // 2), 15)

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            # Проверяем, есть ли зомби в ряду
            for zombie in zombies:
                if zombie.y == self.y and zombie.x > self.x:
                    # Создаем горошину
                    peas.append(Pea(self.x + GRID_SIZE, self.y + GRID_SIZE // 2 - 5))
                    self.cooldown = 60  # 1 секунда при 60 FPS
                    break


class Sunflower(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cooldown = 0
        self.color = (200, 200, 0)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        # Рисуем подсолнух
        pygame.draw.circle(screen, YELLOW, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), 25)

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            # Создаем солнце
            suns.append(Sun(self.x + GRID_SIZE // 2 - 15, self.y))
            self.cooldown = 300  # 5 секунд при 60 FPS


class Pea:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.damage = 20
        self.rect = pygame.Rect(x, y, 10, 10)

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 5)

    def update(self):
        self.x += self.speed
        self.rect.x = self.x

        # Удаляем горошину, если она вышла за экран
        if self.x > SCREEN_WIDTH:
            peas.remove(self)
            return

        # Проверяем столкновение с зомби
        for zombie in zombies:
            if self.rect.colliderect(zombie.rect):
                zombie.health -= self.damage
                if self in peas:
                    peas.remove(self)
                break


class Zombie:
    def __init__(self, row):
        self.x = SCREEN_WIDTH
        self.y = LAWN_TOP + row * GRID_SIZE
        self.speed = 1
        self.health = 100
        self.row = row
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def draw(self):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        # Рисуем здоровье
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 10, GRID_SIZE, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, GRID_SIZE * (self.health / 100), 5))

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

        # Проверяем столкновение с растениями
        for plant in plants:
            if self.rect.colliderect(plant.rect) and self.y == plant.y:
                plant.health -= 0.5
                if plant.health <= 0:
                    plants.remove(plant)
                return

        # Удаляем зомби, если он дошел до конца
        if self.x < 0:
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # Удаляем зомби, если его здоровье закончилось
        if self.health <= 0:
            zombies.remove(self)


class Sun:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.rect = pygame.Rect(x, y, 30, 30)
        self.fall_y = y + random.randint(50, 200)
        self.collected = False

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x + 15, self.y + 15), 15)

    def update(self):
        if self.y < self.fall_y:
            self.y += self.speed
            self.rect.y = self.y

        # Проверяем, было ли солнце собрано
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.collected = True
            return True
        return False


# Игровые объекты
plants = []
zombies = []
peas = []
suns = []

# Игровые переменные
sun_count = 50
selected_plant = None  # 'peashooter' или 'sunflower'
zombie_spawn_timer = 0

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            # Проверяем, было ли нажатие на панель выбора растений
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Выбор гороха (стоит 100 солнц)
            if 10 <= mouse_x <= 60 and 10 <= mouse_y <= 60 and sun_count >= 100:
                selected_plant = 'peashooter'

            # Выбор подсолнуха (стоит 50 солнц)
            elif 70 <= mouse_x <= 120 and 10 <= mouse_y <= 60 and sun_count >= 50:
                selected_plant = 'sunflower'

            # Размещение растения на поле
            elif LAWN_LEFT <= mouse_x <= LAWN_LEFT + GRID_WIDTH * GRID_SIZE and \
                    LAWN_TOP <= mouse_y <= LAWN_TOP + GRID_HEIGHT * GRID_SIZE:
                grid_x = (mouse_x - LAWN_LEFT) // GRID_SIZE
                grid_y = (mouse_y - LAWN_TOP) // GRID_SIZE
                plant_x = LAWN_LEFT + grid_x * GRID_SIZE
                plant_y = LAWN_TOP + grid_y * GRID_SIZE

                # Проверяем, свободна ли клетка
                cell_free = True
                for plant in plants:
                    if plant.x == plant_x and plant.y == plant_y:
                        cell_free = False
                        break

                if cell_free and selected_plant:
                    if selected_plant == 'peashooter' and sun_count >= 100:
                        plants.append(PeaShooter(plant_x, plant_y))
                        sun_count -= 100
                        selected_plant = None
                    elif selected_plant == 'sunflower' and sun_count >= 50:
                        plants.append(Sunflower(plant_x, plant_y))
                        sun_count -= 50
                        selected_plant = None

    # Обновление объектов
    for plant in plants[:]:
        plant.update()

    for pea in peas[:]:
        pea.update()

    for zombie in zombies[:]:
        zombie.update()

    # Сбор солнца
    for sun in suns[:]:
        if sun.update():
            sun_count += 25
            suns.remove(sun)

    # Спавн зомби
    zombie_spawn_timer += 1
    if zombie_spawn_timer >= 300:  # Каждые 5 секунд
        row = random.randint(0, GRID_HEIGHT - 1)
        zombies.append(Zombie(row))
        zombie_spawn_timer = 0

    # Спавн солнца с неба
    if random.random() < 0.005:  # 0.5% шанс каждый кадр
        suns.append(Sun(random.randint(LAWN_LEFT, LAWN_LEFT + GRID_WIDTH * GRID_SIZE - 30), 0))

    # Отрисовка
    screen.fill(BLACK)

    # Рисуем газон
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(LAWN_LEFT + x * GRID_SIZE, LAWN_TOP + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, (0, 100, 0) if (x + y) % 2 == 0 else (0, 120, 0), rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)

    # Рисуем панель выбора растений
    pygame.draw.rect(screen, BROWN, (10, 10, 50, 50))  # Горох
    pygame.draw.rect(screen, GREEN, (15, 15, 40, 40))
    font = pygame.font.SysFont(None, 20)
    text = font.render("100", True, WHITE)
    screen.blit(text, (10, 65))

    pygame.draw.rect(screen, BROWN, (70, 10, 50, 50))  # Подсолнух
    pygame.draw.rect(screen, YELLOW, (75, 15, 40, 40))
    text = font.render("50", True, WHITE)
    screen.blit(text, (70, 65))

    # Рисуем счетчик солнца
    pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH - 100, 10, 80, 30))
    text = font.render(f"{sun_count}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH - 90, 15))

    # Рисуем растения
    for plant in plants:
        plant.draw()

    # Рисуем горошины
    for pea in peas:
        pea.draw()

    # Рисуем зомби
    for zombie in zombies:
        zombie.draw()

    # Рисуем солнце
    for sun in suns:
        sun.draw()

    # Рисуем выбранное растение (превью)
    if selected_plant:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if selected_plant == 'peashooter':
            pygame.draw.rect(screen, (0, 200, 0, 150),
                             (mouse_x - GRID_SIZE // 2, mouse_y - GRID_SIZE // 2, GRID_SIZE, GRID_SIZE))
        elif selected_plant == 'sunflower':
            pygame.draw.rect(screen, (200, 200, 0, 150),
                             (mouse_x - GRID_SIZE // 2, mouse_y - GRID_SIZE // 2, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
